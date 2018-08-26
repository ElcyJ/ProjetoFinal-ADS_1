import functools

from flaskr.models.profile import *
from flaskr.index import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():

    profileDAO = ProfileDAO()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        db, conn = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            db.execute('SELECT id FROM user WHERE username = %s', (username,))
            registros = db.fetchall()
            users = []
            for registro in registros:
                user = {
                    'id': registro[0],
                }
                users.append(user)

            if len(users)>0:
                error = 'User {} os already registered.'.format(username)
            elif error is None:
                db.execute(
                'INSERT INTO user (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
                )
                conn.commit()
                db.execute('SELECT * FROM user WHERE username = %s', (username,))
                user = db.fetchone()

                profileDAO.save_profile(bio, user[0])


                return redirect(url_for('auth.login'))

            flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, conn = get_db()
        error = None
        db.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = db.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index.main'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, conn = get_db()
        db.execute(
            'SELECT * FROM user WHERE id = %s', (user_id)
        )
        g.user = db.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.main'))
