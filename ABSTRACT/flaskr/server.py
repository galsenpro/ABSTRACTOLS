#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys
reload(sys)
#Pour les caractères accentués
sys.setdefaultencoding("utf-8")

from PIL import Image
from StringIO import StringIO
from flask import abort
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response

from datetime import date
app = Flask(__name__)
#app.debug = True
app.secret_key = 'passer'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # la session dure une heure
  
@app.route('/')
def index():
    if 'pseudo' in session:
        #flash ("C'est un plaisir de se revoir, {pseudo} !".format(pseudo=session['pseudo']))
        return render_template('index.html')
    else:
        session['pseudo'] = 'Luc'
        flash("Bonjour, c'est votre première visite ?")
        return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != 'secret':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Utilisateur connecté :  '+ request.form['username'])
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    flash('Vous n\'êtes pas encore connecté ! ')
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/envoi/', methods=['GET', 'POST'])
def envoi():
    if request.method == 'POST':
        return "Vous avez envoyé : {msg}".format(msg=request.form['msg'])
    return """
            <form action="" method="post"><input type="text" name="msg" />
                <input type="submit" value="Envoyer" /></form>
            """
@app.route('/contacte/') # on n'autorise pas la méthode POST
def contacte():
    if request.args.get('msg') is not None:
        return "Vous avez envoyé : {msg}".format(msg=request.args['msg'])
    return '<form action="" method="get"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'

@app.route('/discussion/page/<int:num_page>')
def discussion(num_page):
    return 'Affichage de la page n°{num} de la discussion.'.format(num=num_page)


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    error = None
    if request.method == 'POST':
        if request.form['msg'] != 'message' or \
                request.form['nom'] != 'dieng':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('http://localhost:5000/'))
    return render_template('contact.html', error=error)







@app.context_processor
def passer_titre():
    return dict(titre="Mon titre !")

@app.route('/coucou')
def dire_coucou():
    return 'Coucou !'

@app.route('/la')
def ici():
    return "Le chemin de 'ici' est : " + request.path

@app.route('/contactget/', methods=['GET'])
def contact_formulaire():
    # afficher le formulaire
    mail = "jean@bon.fr"
    tel = "01 23 45 67 89"
    return "Mail: {} --- Tel: {}".format(mail, tel)

@app.route('/contacter', methods=['POST'])
def contact_traiter_donnees():
    # traiter les données reçues
    # afficher : "Merci de m'avoir laissé un message !"
    return "Coucou ABSTRACT!" + request.path

@app.route('/f_python')
@app.route('/forum/python')
@app.route('/truc')
def forum_python():
    return 'contenu forum python'

@app.route('/discussion/page/<int:num_page>')
def mon_chat(num_page):
    num_page = int(num_page)
    premier_msg = 1 + 50 * (num_page - 1)
    dernier_msg = premier_msg + 50
    return 'affichage des messages {} à {}'.format(premier_msg, dernier_msg)

@app.route('/afficher')
@app.route('/afficher/mon_nom_est_<nom>_et_mon_prenom_<prenom>')
def afficher(nom=None, prenom=None):
    if nom is None or prenom is None:
        return "Entrez votre nom et votre prénom comme il le faut dans l'url"
    return "Vous vous appelez {} {} !".format(prenom, nom)

@app.route('/image')
def genere_image():
    mon_image = StringIO()
    Image.new("RGB", (300,300), "#92C41D").save(mon_image, 'BMP')
    return mon_image.getvalue()

@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def ma_page_erreur(error):
    return "Ma jolie page {}".format(error.code), error.code

@app.route('/google')
def redirection_google():
    return redirect('http://www.google.fr')
from flask import redirect

@app.route('/profil')
def profil():
    if utilisateur_non_identifie:
        return redirect('/login')
    return "Vous êtes bien identifié, voici la page demandée : ..."

if __name__ == '__main__':
    app.run(debug=True)
