from modelo_config_bd.config import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')