"""
OpenAI service for email classification and response generation.
"""
from openai import OpenAI
from typing import Dict, Any
import json

class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def classify_email(self, preprocessed_content: str) -> Dict[str, Any]:
        """Classify email using OpenAI API"""
        classification_prompt = f"""
        Analise o seguinte conteúdo de email e classifique-o como PRODUTIVO ou IMPRODUTIVO:

        PRODUTIVO: Emails que requerem ação, resposta ou acompanhamento (ex: dúvidas técnicas, solicitações, problemas, suporte)
        IMPRODUTIVO: Emails sociais ou informativos que não requerem ação (ex: agradecimentos, felicitações, informes gerais)

        Conteúdo do email: {preprocessed_content}

        Responda APENAS em formato JSON:
        {{
            "categoria": "PRODUTIVO" ou "IMPRODUTIVO",
            "justificativa": "explicação breve da classificação"
        }}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user", 
                "content": classification_prompt
            }],
            max_tokens=150,
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        if not content:
            raise Exception("Empty response from OpenAI")
        
        content = content.strip()
        if not content:
            raise Exception("Empty content after strip")
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Content received: {repr(content)}")
            # Fallback response
            return {
                "categoria": "PRODUTIVO",
                "justificativa": "Classificação padrão devido a erro no processamento"
            }
    
    def generate_response(self, email_content: str, category: str) -> str:
        """Generate appropriate response based on email category"""
        if category == "PRODUTIVO":
            response_prompt = f"""
            Baseado neste email produtivo, gere uma resposta profissional CURTA:

            Email: {email_content[:500]}

            IMPORTANTE: A resposta deve ter EXATAMENTE 2 a 5 linhas.
            Resposta deve ser:
            - Profissional e cordial
            - Agradecendo pelo contato
            - Confirmando recebimento
            - Indicando próximos passos
            - MÁXIMO 5 linhas, MÍNIMO 2 linhas

            Formato: Resposta direta sem introduções ou explicações extras.
            """
        else:  # IMPRODUTIVO
            response_prompt = f"""
            Gere uma resposta educada mas firme para este email não produtivo:

            Email: {email_content[:500]}

            IMPORTANTE: A resposta deve ter EXATAMENTE 2 a 3 linhas.
            Resposta deve ser:
            - Educada mas concisa
            - Redirecionando para canais apropriados
            - Sem prolongar conversas desnecessárias
            - MÁXIMO 3 linhas, MÍNIMO 2 linhas

            Formato: Resposta direta sem introduções ou explicações extras.
            """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user", 
                "content": response_prompt
            }],
            max_tokens=150,
            temperature=0.5
        )
        
        content = response.choices[0].message.content
        if not content:
            raise Exception("Empty response from OpenAI")
            
        return content.strip()