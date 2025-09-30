import os
import json
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'autou-email-classifier-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# OpenAI configuration
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Initialize OpenAI client with error handling
try:
    client = OpenAI(api_key=openai_api_key)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    raise

# Upload configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_text(text):
    """Pré-processa o texto removendo ruídos e normalizando"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and excessive numbers
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stop words in Portuguese and English
    try:
        stop_words_pt = set(stopwords.words('portuguese'))
        stop_words_en = set(stopwords.words('english'))
        stop_words = stop_words_pt.union(stop_words_en)
    except:
        stop_words = set(['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'suas', 'numa', 'pelos', 'pelas', 'esse', 'esses', 'pelas', 'estava', 'foram', 'tinha', 'têm', 'seja', 'eram', 'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'i', 'at', 'be', 'this', 'have', 'from', 'or', 'one', 'had', 'by', 'word', 'but', 'not', 'what', 'all', 'were', 'we', 'when', 'your', 'can', 'said', 'there', 'each', 'which', 'their', 'time', 'will', 'about', 'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her', 'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'go', 'no', 'way', 'could', 'my', 'than', 'first', 'been', 'call', 'who', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part'])
    
    # Filter tokens
    filtered_tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    return ' '.join(filtered_tokens)

def extract_text_from_pdf(file_path):
    """Extrai texto de arquivo PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Check if text extraction was successful
            if len(text.strip()) == 0:
                raise Exception("O PDF não contém texto extraível. Pode ser baseado em imagens ou ter proteção. Tente converter para TXT ou usar um PDF com texto selecionável.")
            
            return text
    except Exception as e:
        if "não contém texto extraível" in str(e):
            raise e
        else:
            raise Exception(f"Erro ao ler PDF: {str(e)}")

def extract_text_from_txt(file_path):
    """Extrai texto de arquivo TXT"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo de texto: {str(e)}")

def classify_email_with_ai(email_content):
    """Classifica email usando OpenAI e gera resposta automática"""
    try:
        # Preprocess the text
        processed_content = preprocess_text(email_content)
        
        # Prompt for classification
        classification_prompt = f"""
        Analise o seguinte email e classifique-o em uma das duas categorias:

        PRODUTIVO: Emails que requerem uma ação ou resposta específica (solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema, pedidos de informação, reclamações, solicitações de serviços, etc.)

        IMPRODUTIVO: Emails que não necessitam de uma ação imediata (mensagens de felicitações, agradecimentos, mensagens sociais, spam, etc.)

        Email para análise:
        {email_content[:1000]}

        Responda APENAS com uma das palavras: PRODUTIVO ou IMPRODUTIVO
        """

        classification_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em classificação de emails corporativos. Seja preciso e objetivo."},
                {"role": "user", "content": classification_prompt}
            ],
            max_tokens=10,
            temperature=0.1
        )

        # Check if content is not None
        content = classification_response.choices[0].message.content
        if content is None:
            classification = "IMPRODUTIVO"  # Default fallback
        else:
            classification = content.strip().upper()
        
        # Ensure classification is valid
        if classification not in ['PRODUTIVO', 'IMPRODUTIVO']:
            classification = 'PRODUTIVO'  # Default to productive for safety

        # Prompt for response generation
        if classification == 'PRODUTIVO':
            response_prompt = f"""
            Baseado no email classificado como PRODUTIVO abaixo, gere uma resposta automática profissional e útil.
            
            A resposta deve:
            - Ser cordial e profissional
            - Demonstrar que o email foi recebido e analisado
            - Indicar próximos passos ou prazos quando aplicável
            - Ter entre 2-4 linhas
            - Usar linguagem formal corporativa
            
            Email original:
            {email_content[:800]}
            
            Gere apenas a resposta, sem explicações adicionais:
            """
        else:
            response_prompt = f"""
            Baseado no email classificado como IMPRODUTIVO abaixo, gere uma resposta automática cordial e apropriada.
            
            A resposta deve:
            - Ser cordial e educada
            - Agradecer pela mensagem
            - Ser breve (1-2 linhas)
            - Usar linguagem formal mas calorosa
            
            Email original:
            {email_content[:800]}
            
            Gere apenas a resposta, sem explicações adicionais:
            """

        response_generation = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em gerar respostas automáticas profissionais para emails corporativos."},
                {"role": "user", "content": response_prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )

        # Check if content is not None
        response_content = response_generation.choices[0].message.content
        if response_content is None:
            suggested_response = "Obrigado pelo seu email. Entraremos em contato em breve."
        else:
            suggested_response = response_content.strip()

        return {
            'classification': classification,
            'suggested_response': suggested_response
        }

    except Exception as e:
        print(f"Erro na classificação: {str(e)}")
        return {
            'classification': 'PRODUTIVO',
            'suggested_response': 'Obrigado pelo seu email. Recebemos sua mensagem e retornaremos em breve.',
            'error': str(e)
        }

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint para upload e processamento de arquivos"""
    try:
        # Check if file was sent
        if 'file' not in request.files and 'email_text' not in request.form:
            return jsonify({'error': 'Nenhum arquivo ou texto fornecido'}), 400

        email_content = ""

        # Process sent file
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and file.filename != '':
                if not allowed_file(file.filename):
                    return jsonify({'error': 'Tipo de arquivo não permitido. Use apenas .txt ou .pdf'}), 400

                # Ensure filename is not None before using secure_filename
                filename = secure_filename(file.filename or 'arquivo')
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                try:
                    if filename.lower().endswith('.pdf'):
                        email_content = extract_text_from_pdf(file_path)
                    else:
                        email_content = extract_text_from_txt(file_path)
                finally:
                    # Clean up file after processing
                    if os.path.exists(file_path):
                        os.remove(file_path)

        # Process direct text
        elif 'email_text' in request.form:
            email_content = request.form['email_text'].strip()

        if not email_content or len(email_content.strip()) < 10:
            return jsonify({'error': 'Conteúdo do email muito curto ou vazio'}), 400

        # Classificar email
        result = classify_email_with_ai(email_content)
        
        # Add text statistics converting to string
        result['char_count'] = str(len(email_content))
        result['word_count'] = str(len(email_content.split()))

        return jsonify(result)

    except Exception as e:
        print(f"Erro no processamento: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Endpoint para verificação de saúde da aplicação"""
    return jsonify({'status': 'healthy', 'service': 'AutoU Email Classifier'})

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Run application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)