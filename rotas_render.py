from modelo_config_bd.config import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/nova_partida')
def nova_partida():
    return render_template('criarpartida.html')