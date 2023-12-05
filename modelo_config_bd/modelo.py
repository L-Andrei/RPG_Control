from modelo_config_bd.config import *

class Usuario(db.Model):
    nome = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)

    def obter_usuario(email):
        usuario = Usuario.query.get(email)
        if usuario:
            return jsonify({
                'nome': usuario.nome,
                'email': usuario.email
            })
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
        
def cadastrar_usuario(nome, senha, email):
    novo_usuario = Usuario(nome=nome, senha=senha, email=email)

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
    finally:
        db.session.close()

def verificar_existencia_usuario(email,senha):
    usuario = Usuario.query.filter_by(email=email, senha=senha).first()
    return usuario is not None
    
def login_usuario(email,senha):
    usuario = Usuario.query.filter_by(email=email,senha=senha).first()
    print('a')
    if usuario:
        data = jsonify({'email': usuario.email, 'nome': usuario.nome})
        return data
    else:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mestre_id = db.Column(db.Integer, db.ForeignKey('usuario.email'), nullable=False)
    mestre = db.relationship('Usuario', foreign_keys=[mestre_id])
    jogadores = db.relationship('Usuario', secondary='partida_jogador', backref='partidas')
    limite_jogadores = db.Column(db.Integer, nullable=False, default=5)

def adicionar_jogador_a_partida(partida_id, jogador_email):
    try:
        # Verifique se a partida existe
        partida = Partida.query.get(partida_id)
        if not partida:
            return jsonify({'mensagem': 'Partida não encontrada'}), 404

        # Verifique se o jogador existe
        jogador = Usuario.query.get(jogador_email)
        if not jogador:
            return jsonify({'mensagem': 'Jogador não encontrado'}), 404

        # Verifique se o jogador já está na partida
        if jogador in partida.jogadores:
            return jsonify({'mensagem': 'Jogador já está na partida'}), 400

        # Verifique se a partida atingiu o limite de jogadores
        if len(partida.jogadores) >= partida.limite_jogadores:
            return jsonify({'mensagem': 'A partida atingiu o limite de jogadores'}), 400

        # Adicione o jogador à partida
        partida_jogador = PartidaJogador(partida_id=partida_id, jogador_id=jogador_email)
        db.session.add(partida_jogador)
        db.session.commit()

        return jsonify({'mensagem': f'Jogador {jogador_email} adicionado à partida {partida_id}'}), 200

    except Exception as e:
        return jsonify({'mensagem': f'Erro ao adicionar jogador à partida: {str(e)}'}), 500


def cadastrar_partida(mestre_id, limite_jogadores):
        mestre = Usuario.query.filter_by(email=mestre_id).first()

        if not mestre:
            return False, "Mestre não encontrado."
        nova_partida = Partida(mestre_id=mestre_id, limite_jogadores=limite_jogadores)

        try:
            db.session.add(nova_partida)
            db.session.commit()
            return True, "Partida cadastrada com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao cadastrar a partida: {str(e)}"
        finally:
            db.session.close()

    

class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vida = db.Column(db.Integer, nullable=False)
    mana = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.email'), nullable=False)
    

def criar_personagem(usuario_email, vida, mana, level):
        usuario = Usuario.query.get(usuario_email)

        if usuario:
            novo_personagem = Personagem(vida=vida, mana=mana, level=level, usuario=usuario)
            db.session.add(novo_personagem)
            db.session.commit()
            return jsonify({'mensagem': 'Personagem criado com sucesso'})
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404

class PartidaJogador(db.Model):
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'), primary_key=True)
    jogador_id = db.Column(db.String(50), db.ForeignKey('usuario.email'), primary_key=True)

with app.app_context():
    db.create_all()

