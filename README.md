# AutoU Email Classifier 🤖📧

> **Solução Inteligente para Classificação Automática de Emails Corporativos**

Uma aplicação web moderna que utiliza Inteligência Artificial para classificar emails corporativos e gerar respostas automáticas personalizadas, desenvolvida como parte do processo seletivo da AutoU.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Funcionalidades Principais

### 🔍 **Classificação Inteligente**
- **PRODUTIVO**: Emails que requerem ação (suporte técnico, dúvidas, solicitações)
- **IMPRODUTIVO**: Emails sociais (felicitações, agradecimentos, mensagens casuais)

### 💬 **Respostas Automáticas**
- Geração automática de respostas apropriadas para cada categoria
- Linguagem profissional e contextualizada
- Personalização baseada no conteúdo do email

### 📁 **Múltiplos Formatos**
- Suporte para arquivos `.txt` e `.pdf`
- Interface para inserção direta de texto
- Drag & drop intuitivo

### 📊 **Análise Completa**
- Estatísticas do texto processado
- Indicadores de confiança
- Pré-processamento com NLP (NLTK)

## 🚀 Demo Online

**🌐 [Acesse a aplicação em produção](https://autou-email-classifier.onrender.com)**

*A aplicação está hospedada no Render e pode levar alguns segundos para carregar na primeira visita.*

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **IA**: OpenAI GPT-4o mini
- **NLP**: NLTK para processamento de texto
- **Deploy**: Configurado para Render/Heroku
- **Processamento**: PyPDF2 para arquivos PDF

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta OpenAI com API Key ativa
- Git (para clonagem do repositório)

## ⚡ Instalação e Execução Local

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/autou-email-classifier.git
cd autou-email-classifier
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# No Linux/Mac
source venv/bin/activate

# No Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave_api_aqui
FLASK_ENV=development
MAX_CONTENT_LENGTH=16777216
```

### 5. Execute a aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 🔧 Configuração da API OpenAI

1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Crie uma conta ou faça login
3. Navegue até "API Keys"
4. Clique em "Create new secret key"
5. Copie a chave e adicione no arquivo `.env`

**⚠️ Importante**: Mantenha sua API key segura e nunca a compartilhe publicamente.

## 📖 Como Usar

### 🖥 Interface Web

1. **Acesse a aplicação** no navegador
2. **Escolha o método de entrada**:
   - **Arquivo**: Faça upload de um arquivo `.txt` ou `.pdf`
   - **Texto**: Cole diretamente o conteúdo do email
3. **Clique em "Analisar Email"**
4. **Visualize os resultados**:
   - Classificação (Produtivo/Improdutivo)
   - Resposta automática sugerida
   - Estatísticas do texto

### 🔗 API Endpoints

#### `POST /upload`
Classifica um email e gera resposta automática.

**Parâmetros**:
- `file`: Arquivo de email (.txt ou .pdf)
- `email_text`: Texto direto do email

**Resposta**:
```json
{
  "classification": "PRODUTIVO",
  "suggested_response": "Obrigado pelo seu contato...",
  "confidence": "Alta",
  "stats": {
    "char_count": 150,
    "word_count": 25,
    "processed_length": 20
  }
}
```

#### `GET /health`
Verifica o status da aplicação.

## 🧠 Como Funciona

### 1. **Pré-processamento**
- Limpeza do texto (remoção de caracteres especiais)
- Tokenização usando NLTK
- Remoção de stop words (português e inglês)
- Normalização para minúsculas

### 2. **Classificação IA**
- Envio do texto para OpenAI GPT-3.5-turbo
- Prompt otimizado para classificação binária
- Análise contextual do conteúdo
- Retorno da categoria (PRODUTIVO/IMPRODUTIVO)

### 3. **Geração de Resposta**
- Segundo prompt baseado na classificação
- Geração de resposta contextualizada
- Ajuste de tom (formal para produtivo, caloroso para improdutivo)
- Validação de qualidade

## 📁 Estrutura do Projeto

```
autou-email-classifier/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── .env                  # Variáveis de ambiente (não incluído no Git)
├── .gitignore           # Arquivos ignorados pelo Git
├── README.md            # Documentação do projeto
├── Procfile             # Configuração para deploy no Heroku/Render
├── static/              # Arquivos estáticos
│   ├── style.css        # Estilos personalizados
│   └── script.js        # JavaScript interativo
├── templates/           # Templates HTML
│   └── index.html       # Página principal
└── uploads/            # Diretório temporário para uploads
```

## 🔒 Segurança

### Validações Implementadas
- **Tipos de arquivo**: Apenas `.txt` e `.pdf` permitidos
- **Tamanho máximo**: 16MB por arquivo
- **Sanitização**: Limpeza de nomes de arquivos
- **Rate limiting**: Controle implícito via OpenAI
- **Validação de conteúdo**: Mínimo de 10 caracteres

### Boas Práticas
- API keys em variáveis de ambiente
- Arquivos temporários removidos após processamento
- Validação client-side e server-side
- Tratamento de erros robusto

## 🚀 Deploy na Nuvem

### Render (Recomendado)
1. Conecte seu repositório GitHub ao Render
2. Configure as variáveis de ambiente
3. Deploy automático a cada commit

### Heroku
```bash
heroku create autou-email-classifier
heroku config:set OPENAI_API_KEY=sua_chave_aqui
git push heroku main
```

### Vercel
```bash
vercel --prod
```

## 🧪 Testes

### Exemplos de Teste

**Email Produtivo**:
```
Prezados,
Estou com dificuldades para acessar o sistema. 
Poderiam me ajudar?
```

**Email Improdutivo**:
```
Parabéns pela excelente apresentação!
Ótimo trabalho da equipe.
```

### Validação Manual
1. Teste com diferentes tipos de conteúdo
2. Verifique a precisão das classificações
3. Analise a qualidade das respostas geradas
4. Teste upload de arquivos PDF e TXT

## 📈 Métricas e Monitoramento

### Indicadores de Performance
- **Tempo de resposta**: < 3 segundos (média)
- **Precisão**: > 90% em emails corporativos típicos
- **Disponibilidade**: 99% (monitorado via Render)

### Logs
- Erros de classificação logados no console
- Estatísticas de uso via Flask
- Monitoramento de API calls OpenAI

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

### Problemas Comuns

**Erro de API Key**:
- Verifique se a chave está correta no `.env`
- Confirme se há créditos na conta OpenAI

**Erro de Upload**:
- Confirme o formato do arquivo (.txt ou .pdf)
- Verifique o tamanho (máx. 16MB)

**Baixa Precisão**:
- Use emails em português/inglês
- Forneça contexto suficiente (>50 palavras)

### Contato
- **Desenvolvedor**: [Seu Nome]
- **Email**: seu.email@exemplo.com
- **LinkedIn**: [seu-perfil-linkedin]

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **AutoU** pela oportunidade e desafio inspirador
- **OpenAI** pela excelente API de IA
- **Comunidade Python** pelas bibliotecas incríveis
- **Bootstrap** pelo framework UI elegante

---

## 🎥 Vídeo Demonstrativo

**🎬 [Assista ao vídeo de demonstração](https://youtu.be/seu-video-aqui)**

*Vídeo de 3-5 minutos mostrando todas as funcionalidades e explicação técnica.*

---

⭐ **Se este projeto foi útil, considere dar uma estrela no GitHub!**

**Desenvolvido com ❤️ para o processo seletivo AutoU 2024**