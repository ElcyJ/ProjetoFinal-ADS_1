from flaskr.db import get_db


class Profile():

  def __init__(self, bio, user):
    self.bio = bio
    self.user = user

class ProfileDAO():

    def save_profile(self, bio, user):
        db, conn = get_db()
        profile = Profile(bio, user)

        db.execute(
        'INSERT INTO user_profile (bio, user_id) VALUES (%s, %s)',
        (profile.bio, profile.user)
        )
        conn.commit()

        return profile

    def find_profile_by_user_id(self, id):
        db, conn = get_db()
        db.execute(
            'SELECT * FROM user_profile WHERE user_id = %s', (id)
        )
        p = db.fetchone()

        profile = Profile(p[1],p[2])
        profile.id = p[0];

        return profile

    def find_profiles_by_user_id(self):
        db, conn = get_db()
        db.execute(
            'SELECT * FROM user_profile'
        )
        profiles = db.fetchall()

        return profiles

    def filter_profile(self, conteudo, tipo):
        db, conn = get_db()

        if tipo == '0':
            db.execute(
                'SELECT * FROM user_profile where bio = %s', ("%"+conteudo+"%")
            )
            return db.fetchall()
        else:
            return []
