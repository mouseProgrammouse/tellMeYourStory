from app import db

class User(db.Model):
    """
    User's data
    :param str password: encrypted password for the user
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, unique = True)
    login = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120))
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))

    def is_active(self):
        """ True, as all users are active. """
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        """ False, as all users are not anonymous """
        return False

    def get_id(self):
        """ Return the id to satisfy Flask-Login's requirements. """
        return self.id

    def __repr__(self):
        """ Return printable representation of an object (only login) """
        return '<User %s>' % (self.login)


class Posts(db.Model):
    """
    Post's data
    :param user_id: author's id
    :param pub_date: date of the last save
    :param img: route to image on server
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    img = db.Column(db.String(140))

    def __repr__(self):
        return '<Post title: %s ; Text: %s>' % (self.title, self.text)