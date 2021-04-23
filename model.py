"""Models for project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()



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
    org_name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(25), nullable=True)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    contributor = db.relationship('User', backref='resources')

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



class Wapo(db.Model):
    """ WaPo dataset table """
    __tablename__ = 'data'

    data_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    date = db.Column(db.Date, nullable=False)
    manner_of_death = db.Column(db.String(50), nullable=False)
    allegedly_armed = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    race = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    signs_of_mental_illness = db.Column(db.Boolean, nullable=True)
    alleged_threat_level = db.Column(db.String(50), nullable=True)
    allegedly_fleeing = db.Column(db.String(50), nullable=True)
    body_camera = db.Column(db.Boolean, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    # is_geocoding_exact = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Wapo data_id = {self.data_id} date = {self.date} manner_of_death = {self.manner_of_death} age = {self.age} gender = {self.gender} race = {self.race} city = {self.city} state = {self.state}>'



def test_data():
    """Sample data to run tests with"""

    User.query.delete()
    Resource.query.delete()


    #sample users
    bjorn = User(username="bjorno", 
                password="woofwoof626", 
                email="haulinauss@gmail.com", 
                city="Columbus", 
                state="Ohio")
    forest = User(username="forito", 
                password="awoowoo29", 
                email="maneater@yahoo.com", 
                city="Detroit", 
                state="Michigan")
    rue = User(username="rueyruerue", 
                password="Pigsnort918", 
                email="sunsouttonguesout@gmail.com", 
                city="Detroit", 
                state="Michigan")
    sawyer = User(username="sawybean", 
                password="BORK1016", 
                email="doesyourfacehanglow@yahoo.com", 
                city="Kalamazoo", 
                state="Michigan")
    harvey = User(username="harvard", 
                password="MOWWwww42", 
                email="wheresmywetfood@harvard.edu", 
                city="Canton", 
                state="Ohio")

    #sample resource data
    dwb = Resource(org_name="Detroit Will Breathe", 
                    url="https://detroitwillbreathe.info/", 
                    email="detroitwillbreathe@protonmail.com", 
                    phone="(313) 473-9658", 
                    city="Detroit",
                    state="Michigan")
    aptp = Resource(org_name="Anti Police-Terror Project", 
                    url="http://www.antipoliceterrorproject.org/", 
                    email="aptpinfo@gmail.com", 
                    phone="(123) 456-7890",
                    city="Oakland",
                    state="California")
    cpa = Resource(org_name="Coalition for Police Accountability",
                    url="https://www.coalitionforpoliceaccountability.com/",
                    email="rashidah@coalitionforpoliceaccountability.com",
                    phone="(510) 306-0253",
                    city="Oakland",
                    state="California")
    cuapb = Resource(org_name="Communities United Against Police Brutality", 
                    url="https://www.cuapb.org/",
                    email="cuapb.mpls@gmail.com",
                    phone="(612) 874-7867",
                    city="Minneapolis",
                    state="Minnesota")
    capcr = Resource(org_name="Coalition Against Police Crimes & Repression",
                    url="https://www.capcr-stl.org/",
                    email="capcr2050@gmail.com",
                    phone="(314) 332-1262 ",
                    city="St. Louis",
                    state="Missouri")
   

    db.session.add_all([bjorn, forest, rue, sawyer, harvey, dwb, aptp, cpa, cuapb, capcr])
    db.session.commit()


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
