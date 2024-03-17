from flask import render_template, request, redirect, session, flash, url_for
from main import app
from models import Usuario
from helpers import FormularioUsuario
from flask_bcrypt import generate_password_hash,check_password_hash

@app.route('/novousuario')
def novousuario():
    form = FormularioUsuario()
    return render_template('novousuario.html', titulo='NOVO USUARIO', url_atual=url_for('novousuario'), form=form)

@app.route('/cadastrarusuario', methods=['POST'])
def cadastrarusuario():
    form = FormularioUsuario()
    if form.validate_on_submit():
        flash('Caracteres inválidos !')
        return redirect(url_for('cadastrarusuario')) 
    novo_usuario = Usuario(form.nome.data,generate_password_hash(form.senha.data).decode('utf-8'))
    if Usuario.consultarnome(novo_usuario): 
        flash('Nome de Usuario já utilizado!')
        return redirect(url_for('novousuario'))
    else:
        Usuario.adicionar(novo_usuario)
        session['usuario_logado'] = novo_usuario._nome
        flash(f'Usuario {novo_usuario._nome} Cadastrado com Sucesso!')
        return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', url_atual = url_for('login'), proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario()
    user = Usuario(form.nome.data,form.senha.data)
    consulta_usuario = Usuario.consultarnome(user)
    if form.validate_on_submit() or not consulta_usuario:
        flash('Credenciais incorretas 1 !')
        return redirect(url_for('login'))
    senha = check_password_hash(consulta_usuario[2], form.senha.data)
    if consulta_usuario and senha:
        session['usuario_logado'] = consulta_usuario[1]
        flash(consulta_usuario[1] + ' logado com sucesso !')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Credenciais incorretas 2 !')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso !')
    return redirect(url_for('index'))

@app.route('/esquecisenha')
def esquecisenha():
    form = FormularioUsuario()
    return render_template('redefinirsenha.html', titulo='REDEFINIR SENHA', url_atual=url_for('esquecisenha'), form=form)

@app.route('/redefinirsenha', methods=['POST'])
def redefinirsenha():
    form = FormularioUsuario()
    user = Usuario(form.nome.data,generate_password_hash(form.senha.data).decode('utf-8'))
    consulta_usuario = Usuario.consultarnome(user)
    if form.validate_on_submit() or not consulta_usuario:
        flash('Credenciais incorretas 1 !')
        return redirect(url_for('esquecisenha'))
    Usuario.redefinirsenha(user)
    flash('Senha alterada com sucesso !')
    return redirect(url_for('login'))