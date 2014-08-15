import hashlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from flask_login import UserMixin

import config

#from simpleemail import db
#import simpleemail.db
Session = sessionmaker()
engine = create_engine('sqlite:///{0}'.format(config.DB_FILE), echo=False)
Session.configure(bind=engine)
#session = Session()

Base = declarative_base()


def create_all():
    Base.metadata.create_all(engine)

# many to many
user_channel = Table('user_channel', Base.metadata,
                     Column('user_id', Integer, ForeignKey('users.id')),
                     Column('channel_id', Integer, ForeignKey('channels.id')))


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password_hash = Column(String)
    email = Column(String)
    channel_id = Column(Integer, ForeignKey('channels.id'))
    subscribes = relationship('Channel', secondary=user_channel,
                              backref='users')
    #channels = []

    def __init__(self, login, password, email):
        self.login = login
        self.password_hash = hashlib.sha1(password).hexdigest()
        self.email = email

    def __repr__(self):
        return "User: id=%s, login=%s, password_hash=%s, " \
               "email=%s, channel=%s" % (self.id, self.login,
                                         self.password_hash, self.email,
                                         self.channel.name)

#    @staticmethod
#    def get(user_id):
#        return simpleemail.db.user_get_by_id(int(user_id))

    def subscribe(self, channel):
        self.subscribes.append(channel)

    def unsubscribe(self, channel_id):
        for i, channel in enumerate(self.subscribes[:]):
            if channel.id == channel_id:
                self.subscribes.pop(i)
                return

    def send_message_to_subscribers(self, text):
        pass


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user = relationship('User', uselist=False, backref='channel')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Channel: id={0}, name={1}'.format(self.id, self.name)
