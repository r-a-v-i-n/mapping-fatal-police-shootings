"""Models for project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!
class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username} city={self.city} state={self.state}>'


class Resource(db.Model):
    """A resource or place to donate to."""

    __tablename__ = 'resources'

    org_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    org_name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    contributor = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User', backref='resources')

    def __repr__(self):
        return f'<Resources org_id={self.org_id} org_name={self.org_name} city={self.city} state={self.state}>'


class Vote(db.Model):
    """ An upvote or downvote on a resource/donation """
    __tablename__ = 'votes'

    vote_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    org_id = db.Column(db.Integer, db.ForeignKey('resources.org_id'))
    upvote_downvote = db.Column(db.Integer)

    resource = db.relationship('Resource', backref='votes')
    user = db.relationship('User', backref='votes')

    def __repr__(self):
        return f'<Votes user_id = {self.user_id} org_id = {self.org_id} upvote_downvote = {self.upvote_downvote}>'



def connect_to_db(flask_app, db_uri='postgresql:///wapo', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
