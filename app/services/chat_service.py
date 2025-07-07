import os
import requests
from managers.knowledge_manager import KnowledgeManager
from collections import defaultdict

class ChatService:
    """
    Contém a lógica de negócio principal para processar as mensagens
    do usuário e gerar respostas com o LLM com gestão de memória.
    """
    def __init__(self):
        self.knowledge_manager = KnowledgeManager(
            persona_path='prompts/persona.md',
            knowledge_dir='knowledge'
        )
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
        # Dicionário para armazenar o histórico de conversas por sessão
        self.session_histories = defaultdict(list)

    def _get_context_topic(self, question: str) -> str:
        """Identifica o tópico (nome do arquivo) relevante para a pergunta."""
        question_lower = question.lower()
        context_map = {
            'bolsa_familia': ['bolsa', 'família', 'cadúnico', 'nis', 'cras'],
            'emissao_rg': ['rg', 'identidade', 'cin', 'documento'],
            'sus_agendamento': ['sus', 'consulta', 'médico', 'agendar', 'ubs', 'posto']
        }
        for topic, keywords in context_map.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        return ""

    def get_response(self, user_question: str, session_id: str) -> str:
        """
        Processa a pergunta do utilizador, considerando o histórico da sessão,
        e chama a API do Gemini para obter a resposta.
        """
        if not self.api_key or "SUA_CHAVE" in self.api_key:
            return "Erro: A chave da API do Gemini não foi configurada no ficheiro .env."

        # Recupera o histórico da sessão atual
        history = self.session_histories[session_id]

        persona_prompt = self.knowledge_manager.get_persona_prompt()
        topic = self._get_context_topic(user_question)
        
        # Se um novo tópico for identificado, o contexto é o conhecimento específico.
        # Se não, o contexto é vazio (para perguntas de acompanhamento).
        specific_knowledge = self.knowledge_manager.get_knowledge(topic) if topic else ""

        # Lógica de fallback
        if not specific_knowledge and not history:
             return "Desculpe, não entendi sobre qual serviço você está falando. Eu posso ajudar com Bolsa Família, Emissão de RG ou Agendamento de Consultas no SUS."

        # Formata o histórico para incluir no prompt
        formatted_history = "\n".join([f"Usuário: {h['user']}\nAssistente: {h['bot']}" for h in history])

        # Monta o prompt final com persona, histórico e conhecimento específico (se houver)
        final_prompt = (
            f"{persona_prompt}\n\n"
            f"## CONTEXTO DA CONVERSA ANTERIOR:\n{formatted_history}\n\n"
            f"## BASE DE CONHECIMENTO PARA A PERGUNTA ATUAL:\n***\n{specific_knowledge}\n***\n\n"
            f"Pergunta do Utilizador: \"{user_question}\""
        )

        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": final_prompt}]}]}

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            json_response = response.json()
            bot_response = json_response['candidates'][0]['content']['parts'][0]['text'].strip()

            # Adiciona a interação atual ao histórico da sessão
            self.session_histories[session_id].append({"user": user_question, "bot": bot_response})
            # Limita o histórico às últimas 3 interações para não sobrecarregar o prompt
            if len(self.session_histories[session_id]) > 3:
                self.session_histories[session_id].pop(0)

            return bot_response
        except requests.exceptions.RequestException as e:
            print(f"Erro de comunicação com a API: {e}")
            return "Desculpe, estou com problemas técnicos para me conectar ao sistema. Tente novamente mais tarde."
        except (KeyError, IndexError) as e:
            print(f"Erro ao processar a resposta da API: {e}")
            return "Desculpe, o sistema retornou uma resposta inesperada."