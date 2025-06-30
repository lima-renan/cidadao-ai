from flask import Flask, request, jsonify, render_template
from services.chat_service import ChatService

# Cria a instância da aplicação Flask
app = Flask(__name__, template_folder='.')

# Inicializa a camada de serviço que contém toda a lógica
chat_service = ChatService()

@app.route('/')
def index():
    """Serve a página inicial do frontend (interface do chat)."""
    return render_template('static/index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint que recebe as mensagens do utilizador via POST, processa-as
    e retorna a resposta do chatbot em formato JSON.
    """
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Mensagem não encontrada na requisição"}), 400

    # Delega o processamento da mensagem para a camada de serviço
    bot_response = chat_service.get_response(user_message)
    
    return jsonify({"reply": bot_response})