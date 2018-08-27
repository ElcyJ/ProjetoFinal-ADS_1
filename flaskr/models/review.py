from flaskr.db import get_db


class Review():

  def __init__(self, rate, commentary, book_id, user_id):
    self.rate = rate
    self.commentary = commentary
    self.book_id = book_id
    self.user_id = user_id

class ReviewDAO():

    def get_reviews(self, book_id):
        db, conn = get_db()
        db2, conn2 = get_db()

        db.execute(
        'SELECT * FROM reviews where book_id = %s ',(book_id)
        )

        registros = db.fetchall()
        reviews = []
        for registro in registros:
            db2.execute(
            'SELECT username FROM user where id = %s ',(registro[4])
             )

            review = {
                'rate': registro[1],
                'commentary': registro[2],
                'user_id' : registro[4],
                'username' : db2.fetchone()[0]
            }


            reviews.append(review)

        return reviews


    def save_review(self, rate, commentary, book_id, user_id):
        db, conn = get_db()
        review = Review(rate, commentary, book_id, user_id)

        db.execute(
        'INSERT INTO reviews (rate, commentary, book_id, user_id) VALUES (%s, %s, %s, %s)',
        (review.rate, review.commentary, review.book_id, review.user_id)
        )
        conn.commit()

        return review

    def isValid(self, book_id, user_id):
        db, conn = get_db()

        db.execute(
        'SELECT * FROM reviews where book_id = %s and user_id = %s ',(book_id, user_id)
        )

        if len(db.fetchall())>0 :
            return False
        else:
            return True
