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

    if usuario:
        session['email'] = email
        return jsonify({'email': usuario.email, 'nome': usuario.nome})
    else:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mestre_id = db.Column(db.Integer, db.ForeignKey('usuario.email'), nullable=False)
    mestre = db.relationship('Usuario', foreign_keys=[mestre_id])
    jogadores = db.relationship('Usuario', secondary='partida_jogador', backref='partidas')
    limite_jogadores = db.Column(db.Integer, nullable=False, default=5)

    def adicionar_jogador(self, jogador_id):
        # Verifique se o jogador existe
        jogador = Usuario.query.filter_by(email=jogador_id).first()

        if not jogador:
            return False, "Jogador não encontrado."

        # Verifique se o número máximo de jogadores foi atingido
        if len(self.jogadores) >= self.limite_jogadores:
            return False, "Número máximo de jogadores atingido."

        # Adicione o jogador à partida
        self.jogadores.append(jogador)

        try:
            db.session.commit()
            return True, "Jogador adicionado à partida com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao adicionar jogador à partida: {str(e)}"
        finally:
            db.session.close()

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

partida_jogador = db.Table('partida_jogador',
                db.Column('partida_id', db.Integer, db.ForeignKey('partida.id'), primary_key=True),
                db.Column('jogador_id', db.Integer, db.ForeignKey('usuario.email'), primary_key=True))

with app.app_context():
    db.create_all()

