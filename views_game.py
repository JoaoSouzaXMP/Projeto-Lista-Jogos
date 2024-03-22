from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from main import app
from models import Jogo,Imagem
from helpers import recupera_imagem,deletar_arquivo,FormularioJogo
import time

@app.route('/')
def index():
    return render_template('lista.html', titulo='JOGOS', url_atual=url_for('index') , jogos=Jogo.exibir())

@app.route('/novojogo')
def novojogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novojogo')))
    form = FormularioJogo()
    return render_template('novojogo.html', titulo='NOVO JOGO', url_atual=url_for('novojogo'), form=form)

@app.route('/cadastrarjogo', methods=['POST'])
def cadastrarjogo():
    form = FormularioJogo()
    if not form.validate_on_submit():
        flash('Caracteres inválidos ')
        return redirect(url_for('novojogo'))
    novo_jogo = Jogo(form.nome.data,form.categoria.data,form.console.data)
    if Jogo.consultarnome(novo_jogo): 
        flash('Jogo já existe!')
        return redirect(url_for('novojogo'))
    else:
        Jogo.adicionar(novo_jogo)
        row = Jogo.consultarnome(novo_jogo)
        arquivo = request.files['arquivo']
        Imagem.salvar(row[0],arquivo)
        # upload_path = app.config['UPLOAD_PATH']
        # timestamp = time.time()
        # arquivo.save(f'{upload_path}/capa{row[0]}-{timestamp}.jpg')
        flash('Jogo Cadastrado com Sucesso!')
        return redirect(url_for('index'))
    
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    else:
        jogo = Jogo.consultarid(id)
        form = FormularioJogo()
        id,form.nome.data,form.categoria.data,form.console.data = jogo
        capa_jogo = Imagem.recuperar(id)
        # capa_jogo = recupera_imagem(id)
        return render_template('editar.html', titulo='EDITANDO JOGO', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        Jogo.atualizar(request.form['id'],form.nome.data,form.categoria.data,form.console.data)
        Imagem.editar(request.form['id'],request.files['arquivo'])
        # upload_path = app.config['UPLOAD_PATH']
        # timestamp = time.time()
        # deletar_arquivo(request.form['id'])
        # arquivo.save(f'{upload_path}/capa{request.form['id']}-{timestamp}.jpg')
        flash('Jogo Atualizado com Sucesso!')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Jogo.deletar(id)
    flash('Jogo Deletado com Sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

