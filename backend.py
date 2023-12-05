from modelo_config_bd.config import *
from modelo_config_bd.modelo import *
from rotas_render import *

@app.route('/cadastrar_usuario_json', methods=['POST'])
def cadastrar_usuario_json():
    dados_usuario = request.get_json()

    if 'nome' in dados_usuario and 'senha' in dados_usuario and 'email' in dados_usuario:
        nome = dados_usuario['nome']
        senha = dados_usuario['senha']
        email = dados_usuario['email']

        sucesso, mensagem_erro = cadastrar_usuario(nome, senha, email)

        if sucesso:
            return jsonify({'mensagem': 'Usuário cadastrado com sucesso'})
        else:
            return jsonify({'mensagem': f'Erro ao cadastrar usuário: {mensagem_erro}'}), 500
    else:
        return jsonify({'mensagem': 'Campos inválidos'}), 400
    
@app.route('/login_json', methods=['POST'])
def login_json():
    dados_login = request.get_json()

    if 'email' in dados_login:
        email = dados_login['email']
        senha = dados_login['senha']

        if verificar_existencia_usuario(email,senha):
            return login_usuario(email,senha)
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    else:
        return jsonify({'mensagem': 'Campo "email" ausente'}), 400

app.run(debug=True,host='0.0.0.0')