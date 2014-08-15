import hashlib
import time
import db

from simpleemail import mail


class Assistant(object):
    def __init__(self):
        self.map = {}

    def add_to_queue(self, user, url):
        key = hashlib.md5(user.login + str(time.time())).hexdigest()
        self.map[key] = user
        text = 'To finish registration go to http://localhost:5000{0}?key={1}'.\
            format(url, key)
        mail.send_message(user.email, 'Registration', text)

    def register(self, key):
        user = self.map.get(key)
        print user
        if user:
            db.session.add(user)
            db.session.commit()
            del self.map[key]
