import hashlib


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


from simpleemail import config

Session = sessionmaker()
engine = create_engine('sqlite:///{0}'.format(config.DB_FILE), echo=False)
Session.configure(bind=engine)


session = Session()

from models import Channel, User


def channel_get_by_id(channel_id):
    return session.query(Channel).filter(Channel.id == channel_id).first()


def channels_get_all():
    return session.query(Channel).all()


def user_add(username, password, email, channel_name):
    user = User(username, hashlib.sha1(password).hexdigest(), email)
    channel = Channel(channel_name)
    user.channel = channel
    session.add(user)
    session.commit()


def user_get_by_id(user_id):
    return session.query(User).filter(User.id == user_id).first()


def user_get_by_login_and_password(login, password):
    password_hash = hashlib.sha1(password).hexdigest()
    return session.query(User).filter(User.login == login).\
        filter(User.password_hash == password_hash).first()


def user_is_login_free(login):
    return session.query(User).filter(User.login == login).all() == []


def tst():
    #user_add('user1', 'password1', '1@1', 'channel1')
    print session.query(User).all()

