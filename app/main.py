import os
import uuid
from flask import Flask, request, jsonify, render_template, session
from services.chat_service import ChatService

# Cria a instância da aplicação Flask
app = Flask(__name__, template_folder='.')
# É necessário uma secret key para a gestão de sessões do Flask
app.secret_key = os.urandom(24)

# Inicializa a camada de serviço que contém toda a lógica
chat_service = ChatService()

@app.before_request
def make_session_permanent():
    # Garante que a sessão não expire
    session.permanent = True
    # Cria um ID de sessão único se não existir
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        # LOG para mostrar a criação de uma nova sessão
        print(f"--- Nova sessão criada com ID: {session['session_id']} ---")

@app.route('/')
def index():
    """Serve a página inicial do frontend (interface do chat)."""
    return render_template('static/index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint que recebe as mensagens do usuário e retorna a resposta do bot.
    Agora passa o ID da sessão para o serviço.
    """
    user_message = request.json.get('message')
    session_id = session.get('session_id')

    # LOG para mostrar qual sessão está a ser usada em cada pedido
    print(f"Pedido recebido para a sessão ID: {session_id}")

    if not user_message:
        return jsonify({"error": "Mensagem não encontrada na requisição"}), 400
    
    if not session_id:
        return jsonify({"error": "ID de sessão não encontrado"}), 400

    # Delega o processamento da mensagem e o ID da sessão para a camada de serviço
    bot_response = chat_service.get_response(user_message, session_id)
    
    return jsonify({"reply": bot_response})