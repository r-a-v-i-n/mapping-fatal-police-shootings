"""CRUD operations."""

from model import db, User, Resource, connect_to_db


# Functions start here!
def create_user(username, password, email, city, state):
    """Create and return a new user."""

    user = User(username=username, password=password, email=email, city=city, state=state)

    db.session.add(user)
    db.session.commit()

    return user


def create_org(org_name, url, email, phone, city, state, user_id):
    """Create and return a new resource/donation option."""

    org = Resource(org_name=org_name, url=url, email=email, phone=phone, city=city, state=state, user_id=user_ud)

    db.session.add(org)
    db.session.commit()

    return org


def list_resources():
    """Return all resources."""
    return Resource.query.all()


def get_resource_by_loc(city, state):
    get_resource = Resource.query.get(city, state)
    return get_resource.city, get_resource.state
    




if __name__ == '__main__':
    from server import app
    connect_to_db(app)