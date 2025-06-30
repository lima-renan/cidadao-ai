import os
import requests
from managers.knowledge_manager import KnowledgeManager

class ChatService:
    """
    Contém a lógica de negócio principal para processar as mensagens
    do utilizador e gerar respostas com o LLM.
    """
    def __init__(self):
        """
        Inicializa o serviço, instanciando o KnowledgeManager e configurando
        as informações da API do Gemini.
        """
        self.knowledge_manager = KnowledgeManager(
            persona_path='prompts/persona.md',
            knowledge_dir='knowledge'
        )
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"

    def _get_context_topic(self, question: str) -> str:
        """
        Analisa a pergunta do utilizador para identificar o tópico relevante.
        Esta é a lógica de roteamento de contexto.
        """
        question_lower = question.lower()
        
        # Mapeamento de palavras-chave para os nomes dos ficheiros de conhecimento (tópicos)
        context_map = {
            'bolsa_familia': ['bolsa', 'família', 'cadúnico', 'nis', 'cras'],
            'emissao_rg': ['rg', 'identidade', 'cin', 'documento'],
            'sus_agendamento': ['sus', 'consulta', 'médico', 'agendar', 'ubs', 'posto']
        }

        # Retorna o primeiro tópico que corresponde a uma palavra-chave
        for topic, keywords in context_map.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        return ""

    def get_response(self, user_question: str) -> str:
        """
        Processa a pergunta do utilizador, monta o prompt final com o contexto
        correto e chama a API do Gemini para obter a resposta.
        """
        if not self.api_key or "SUA_CHAVE" in self.api_key:
            return "Erro de configuração: A chave da API do Gemini não foi definida no ficheiro .env."

        # Obtém os componentes do prompt através do KnowledgeManager
        persona_prompt = self.knowledge_manager.get_persona_prompt()
        topic = self._get_context_topic(user_question)
        specific_knowledge = self.knowledge_manager.get_knowledge(topic)

        # Se nenhum tópico for identificado, retorna uma mensagem de fallback
        if not specific_knowledge:
            return "Desculpe, não entendi sobre qual serviço você está falando. Eu posso ajudar com Bolsa Família, Emissão de RG ou Agendamento de Consultas no SUS."

        # Monta o prompt final que será enviado para o LLM
        final_prompt = (
            f"{persona_prompt}\n\n"
            f"## SEÇÃO 2: BASE DE CONHECIMENTO\n***\n{specific_knowledge}\n***\n\n"
            f"Pergunta do Utilizador: \"{user_question}\""
        )
        
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": final_prompt}]}]}

        # Tenta comunicar com a API e trata possíveis erros
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            json_response = response.json()
            return json_response['candidates'][0]['content']['parts'][0]['text'].strip()
        except requests.exceptions.RequestException as e:
            print(f"Erro de comunicação com a API: {e}")
            return "Desculpe, estou com problemas técnicos para me conectar ao sistema. Tente novamente mais tarde."
        except (KeyError, IndexError) as e:
            print(f"Erro ao processar a resposta da API: {e}")
            return "Desculpe, o sistema retornou uma resposta inesperada."