# -*- coding: utf-8 -*-
import sys
import os.path

par_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       os.path.pardir)
sys.path.append(par_dir)

from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash
from flask_wtf import CsrfProtect

from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user

from simpleemail import models, db, mail, registration
from simpleemail.forms import RegisterForm, LoginForm, SubscribeForm
from simpleemail.forms import UnsubscribeForm, SendForm

# configuration
#DATABASE = '/tmp/simple_email.db'
DEBUG = True
SECRET_KEY = 'secret key for development'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

CsrfProtect(app)
login_manger = LoginManager(app)
assistant = registration.Assistant()


@login_manger.user_loader
def load_user(user_id):
    return db.user_get_by_id(int(user_id))


@app.route('/')
def index():
    print current_user.is_anonymous()
    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            login = form.login.data
            password = form.password.data
            print login, password
            user = db.user_get_by_login_and_password(login, password)
            print user  # None
            if user:
                login_user(user)
                return redirect(url_for('my_subscribes'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print 'validate'
            login = form.login.data
            if not db.user_is_login_free(login):
                return redirect(url_for('register'))
            password = form.password.data
            email = form.email.data
            channel_name = form.channel_name.data
            user = models.User(login, password, email)
            channel = models.Channel(channel_name)
            user.channel = channel
            assistant.add_to_queue(user, url_for('validate_email'))
            return redirect(url_for('index'))
    return render_template('registration.html', form=form)


@app.route('/validate')
def validate_email():
    key = request.args['key']
    assistant.register(key)
    return redirect(url_for('log_in'))


@app.route('/my_subscribes')
@login_required
def my_subscribes():
    form = UnsubscribeForm()
    subscribes = current_user.subscribes
    return render_template('my_subscribes.html', form=form,
                           subscribes=subscribes)


@app.route('/channel_list')
@login_required
def channel_list():
    subscribe_form = SubscribeForm()
    unsubscribe_form = UnsubscribeForm()
    channels = db.channels_get_all()
    return render_template('channel_list.html', channels=channels,
                           user=current_user, s_form=subscribe_form,
                           u_form=unsubscribe_form)


@app.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        channel = db.channel_get_by_id(form.channel_id.data)
        current_user.subscribe(channel)
        print current_user.subscribes
        db.session.commit()
    return redirect(url_for('channel_list'))


@app.route('/unsubscribe', methods=['POST'])
@login_required
def unsubscribe():
    form = UnsubscribeForm()
    if form.validate_on_submit():
        current_user.unsubscribe(form.channel_id.data)
        db.session.commit()
        return redirect(url_for(form.return_to.data))


@app.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    form = SendForm()
    if form.validate_on_submit():
        text = unicode(form.text.data)
        subject = current_user.channel.name
        print current_user.channel.users
        for user in current_user.channel.users:
            print user.email
            mail.send_message(user.email, subject, text)
    return render_template('send.html', form=form)


@app.route('/debug')
#@login_required
def debug():
    db.tst()
    return 'debug'


if __name__ == '__main__':
    #db.create_db()
    app.run()
