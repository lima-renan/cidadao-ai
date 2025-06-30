import os

class KnowledgeManager:
    """
    Esta classe é responsável por ler e gerir todos os ficheiros de texto
    que formam a base de conhecimento e a persona do chatbot.
    """
    def __init__(self, persona_path: str, knowledge_dir: str):
        """
        Args:
            persona_path (str): O caminho para o ficheiro da persona.
            knowledge_dir (str): O caminho para o diretório com os ficheiros de conhecimento.
        """
        self.persona_prompt = self._load_file(persona_path)
        self.knowledge_base = self._load_knowledge_from_dir(knowledge_dir)

    def _load_file(self, filepath: str) -> str:
        """
        Método auxiliar para ler o conteúdo de um único ficheiro.
        Retorna uma string vazia se o ficheiro não for encontrado.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"ERRO: Ficheiro de conhecimento não encontrado em '{filepath}'")
            return ""

    def _load_knowledge_from_dir(self, dir_path: str) -> dict:
        """
        Carrega todos os ficheiros .md de um diretório e armazena-os
        num dicionário. A chave é o nome do ficheiro (sem .md).
        """
        knowledge = {}
        try:
            for filename in os.listdir(dir_path):
                if filename.endswith(".md"):
                    topic_key = filename.replace(".md", "")
                    content = self._load_file(os.path.join(dir_path, filename))
                    knowledge[topic_key] = content
            return knowledge
        except FileNotFoundError:
            print(f"ERRO: Diretório de conhecimento '{dir_path}' não encontrado.")
            return {}

    def get_persona_prompt(self) -> str:
        """Retorna o prompt da persona carregado."""
        return self.persona_prompt

    def get_knowledge(self, topic: str) -> str:
        """Retorna o conhecimento de um tópico específico."""
        return self.knowledge_base.get(topic, "")