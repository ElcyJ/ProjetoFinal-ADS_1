import functools

from flaskr.models.book import *
from flaskr.models.review import *


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/main', methods=('GET', 'POST'))

def main():

    bookDAO = BookDAO()

    books = bookDAO.get_books()

    return render_template('index/main.html', books=books)

@bp.route('/search', methods=('GET', 'POST'))

def search():

    bookDAO = BookDAO()

    if request.method == 'GET':
        content = request.args.get('search', '')
        type = request.args.get('type', '')
        order = request.args.get('order', '')

        books = bookDAO.filter_book(content, type, order)

    return render_template('index/main.html', books=books)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/book_details/<isbn>', methods=('GET', 'POST'))
def book_details(isbn):
    bookDAO = BookDAO()
    reviewDAO = ReviewDAO()

    book = bookDAO.get_book(isbn)
    session['isbn'] = book.isbn
    reviews = reviewDAO.get_reviews(book.isbn)

    book.reviewable = reviewDAO.isValid( book.isbn, session.get('user_id'))

    return render_template('index/details.html', book=book, reviews=reviews)

@bp.route('/set_review', methods=('GET', 'POST'))
@login_required
def set_review():
    reviewDAO = ReviewDAO()
    user_id = session.get('user_id')
    book_id = session.get('isbn')

    if request.method == 'POST':
        rate = request.form['rate']
        commentary = request.form['commentary']


    review = reviewDAO.save_review(rate, commentary, book_id, user_id)
    return  book_details(book_id)