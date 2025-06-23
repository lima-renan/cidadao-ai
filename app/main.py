import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='.')

def get_knowledge_base():
    """Carrega a base de conhecimento do arquivo markdown."""
    try:
        with open('prompt_knowledge_base.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Erro: Arquivo de conhecimento não encontrado."

KNOWLEDGE_BASE = get_knowledge_base()

def get_llm_response(user_question: str) -> str:
    """
    Formata o prompt e chama a API do Gemini Pro para obter uma resposta.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    prompt = f"{KNOWLEDGE_BASE}\n\nPergunta do Usuário: \"{user_question}\""

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    if not api_key or "SUA_CHAVE" in api_key:
        return "Erro de configuração: A chave da API do Gemini não foi definida. Por favor, configure o arquivo .env."

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()
        return json_response['candidates'][0]['content']['parts'][0]['text'].strip()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return "Desculpe, estou com problemas técnicos para me conectar ao sistema. Tente novamente mais tarde."
    except (KeyError, IndexError) as e:
        print(f"Erro ao processar a resposta da API: {e}")
        print(f"Resposta recebida: {response.text}")
        return "Desculpe, recebi uma resposta inesperada do sistema. Não consigo processar sua pergunta agora."


@app.route('/')
def index():
    """Serve a página principal do chatbot."""
    return render_template('static/index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para receber a mensagem do usuário e retornar a resposta do bot."""
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Mensagem não encontrada na requisição"}), 400

    bot_response = get_llm_response(user_message)
    return jsonify({"reply": bot_response})
