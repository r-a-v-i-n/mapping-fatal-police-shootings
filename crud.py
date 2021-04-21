"""CRUD operations."""

from model import db, User, Resource, connect_to_db



# USER FUNCTIONS

def create_user(username, password, email, city, state):
    """Create and return a new user."""

    user = User(username=username, password=password, email=email, city=city, state=state)

    db.session.add(user)
    db.session.commit()

    return user


def confirm_current_user(username):
    """Return true or false depending on whether username already exists"""
    
    user = User.query.filter(User.username == username).first()

    if user:
        return True
    
    return False

def find_user_by_username(username):
    """Return user by searching for username."""

    user = User.query.filter(User.username == username).first()

    return user

# not yet implemented, come back to this for /sign_up route
def verify_unique_email(email):
    """Return true or false depending on whether email already has an account attached"""
    
    email = User.query.filter(User.email == email).first()

    if email:
        return True
    
    return False




# RESOURCE FUNCTIONS

def create_org(org_name, url, email, phone, city, state, user_id):
    """Create and return a new resource/donation option."""

    org = Resource(org_name=org_name, url=url, email=email, phone=phone, city=city, state=state, user_id=user_id)

    db.session.add(org)
    db.session.commit()

    return org


def confirm_current_org(org_name):
    """Return true or false depending on whether org/resource already exists"""
    
    org = Resource.query.filter(Resource.org_name == org_name).first()

    if org:
        return True
    
    return False


def list_resources():
    """Return all resources."""
    return Resource.query.all()


def get_resource_by_loc(city, state):
    get_resource = Resource.query.get(city, state)
    return get_resource.city, get_resource.state










if __name__ == '__main__':
    from server import app
    connect_to_db(app)