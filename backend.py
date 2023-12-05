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

@app.route('/cadastrar_partida', methods=['POST'])
def cadastrar_partida():
    try:
        dados_partida = request.json
        mestre_id = dados_partida.get('mestre_id')
        limite_jogadores = dados_partida.get('limite_jogadores')

        mestre = Usuario.query.filter_by(email=mestre_id).first()
        if not mestre:
            return jsonify({'mensagem': 'Mestre não encontrado.'}), 404

        nova_partida = Partida(mestre_id=mestre_id, limite_jogadores=limite_jogadores)

        db.session.add(nova_partida)
        db.session.commit()

        return jsonify({'mensagem': 'Partida cadastrada com sucesso.'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': f'Erro ao cadastrar a partida: {str(e)}'}), 500

    finally:
        db.session.close()

@app.route('/partidas_disponiveis', methods=['GET'])
def partidas_disponiveis():
    try:
        partidas_disponiveis = Partida.query.filter(Partida.limite_jogadores > db.func.count(partida_jogador.jogador_id)).group_by(Partida.id).all()

        resultados_json = []
        for partida in partidas_disponiveis:
            resultado = {
                'id': partida.id,
                'mestre_id': partida.mestre_id,
                'limite_jogadores': partida.limite_jogadores,
                'jogadores_atuais': len(partida.jogadores),
            }
            resultados_json.append(resultado)

        return jsonify({'partidas_disponiveis': resultados_json})

    except Exception as e:
        return jsonify({'mensagem': f'Erro ao obter partidas disponíveis: {str(e)}'}), 500


app.run(debug=True,host='0.0.0.0')