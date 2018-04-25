#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response, url_for

from flask import send_file
from werkzeug import secure_filename
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'

DOSSIER_UPS = '/home/adama/NetBeansProjects/ABSTRACT1_0/flaskr/ups/'

@app.route('/')
def index():
    if not session.get('logged_in'):
        flash('Merci de vous connecter d\'abord !')
        return redirect(url_for('login'))
    else:
        if 'pseudo' in session:
            #flash ("C'est un plaisir de se revoir, {pseudo} !".format(pseudo=session['pseudo']))
            return render_template('index.html')
        else:
            session['pseudo'] = 'Luc'
            #flash("Bonjour, c'est votre première visite ?")
            return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != 'adama.dieng@orange.com':
            error = 'Invalid username'
        elif request.form['password'] != 'secret':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Utilisateur connecté :  '+ request.form['email'])
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    flash('Vous n\'êtes pas encore connecté ! ')
    session.pop('logged_in', None)
    return redirect(url_for('index'))

def extension_ok(nomfic):
    """ Renvoie True si le fichier possède une extension d'image valide. """
    return '.' in nomfic and nomfic.rsplit('.', 1)[1] in ('png', 'jpg', 'jpeg', 'gif', 'bmp')

@app.route('/up/', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        flash('Merci de vous connecter d\'abord !')
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            if request.form['pw'] == 'up': # on vérifie que le mot de passe est bon
                f = request.files['fic']
                if f: # on vérifie qu'un fichier a bien été envoyé
                    if extension_ok(f.filename): # on vérifie que son extension est valide
                        nom = secure_filename(f.filename)
                        f.save(DOSSIER_UPS + nom)
                        flash(u'Image envoyée ! Voici <a href="{lien}">son lien</a>.'.format(lien=url_for('upped', nom=nom)), 'success')
                    else:
                        flash(u'Ce fichier ne porte pas une extension autorisée !', 'error')
                else:
                    flash(u'Vous avez oublié le fichier !', 'error')
            else:
                flash(u'Mot de passe incorrect', 'error')
        return render_template('up_up.html')

@app.route('/up/view/')
def liste_upped():
    if not session.get('logged_in'):
        flash('Merci de vous connecter d\'abord !')
        return redirect(url_for('index'))
    else:
        images = [img for img in os.listdir(DOSSIER_UPS) if extension_ok(img)] # la liste des images dans le dossier
        return render_template('up_liste.html', images=images)

@app.route('/up/view/<nom>')
def upped(nom):
    if not session.get('logged_in'):
        flash('Merci de vous connecter d\'abord !')
        return redirect(url_for('index'))
    else:
        nom = secure_filename(nom)
        if os.path.isfile(DOSSIER_UPS + nom): # si le fichier existe
            return send_file(DOSSIER_UPS + nom, as_attachment=True) # on l'envoie
        else:
            flash(u'Fichier {nom} inexistant.'.format(nom=nom), 'error')
            return redirect(url_for('liste_upped')) # sinon on redirige vers la liste des images, avec un message d'erreur

@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def ma_page_erreur(error):
    error = error.code
    return render_template('404.html',error = error)

@app.route('/dashboard/')
def redirection_google():
    return redirect('http://localhost:3000/')
from flask import redirect

if __name__ == '__main__':
    app.run(debug=True)
