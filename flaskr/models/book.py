from flaskr.db import get_db


class Book():

  def __init__(self, isbn, title, author, year):
    self.isbn = isbn
    self.title = title
    self.author = author
    self.year = year

class BookDAO():


    def get_books(self):
        db, conn = get_db()
        db.execute(
                'SELECT * FROM books'
        )

        registros = db.fetchall()
        books = []
        for registro in registros:
            book = {
                'isbn': registro[0],
                'title': registro[1],
                'author': registro[2],
                'year': registro[3]
            }
            books.append(book)

        return books

    def get_book(self, isbn):
        db, conn = get_db()
        db.execute(
            'SELECT * FROM books where isbn = %s', (isbn)
        )
        b = db.fetchone()

        book = Book(b[0], b[1], b[2], b[3])

        return book


    def filter_book(self, content, type, order):
        db, conn = get_db()
        registros = None

        if type == "titulo":
            db.execute(
                '''SELECT * FROM books where title like %s order by title '''+ order, ("%"+content+"%")
            )
            registros = db.fetchall()
        if type == "autor":
            db.execute(
                '''SELECT * FROM books where author like %s order by author '''+ order, ("%"+content+"%")
            )
            registros = db.fetchall()
        if type == "ano":
            db.execute(
                '''SELECT * FROM books where year like %s order by year '''+ order, ("%"+content+"%")
            )
            registros = db.fetchall()
        if type == "isbn":
            db.execute(
                '''SELECT * FROM books where ISBN like %s order by ISBN '''+ order, ("%"+content+"%")
            )
            registros = db.fetchall()

        books = []
        for registro in registros:
            book = {
                'isbn': registro[0],
                'title': registro[1],
                'author': registro[2],
                'year': registro[3]
            }
            books.append(book)

        return books
