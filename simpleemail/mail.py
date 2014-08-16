# -*- coding: utf-8 -*-
import smtplib
import email.mime.text
import time
import thread

import config


class MessageSender(object):
    def __init__(self):
        self.smtp_connection = None
        self.connect()

    def connect(self):
        self.smtp_connection = smtplib.SMTP_SSL(host='smtp.gmail.com',
                                                port=465)
        self.smtp_connection.login(config.SMTP_HOST,
                                   config.SMTP_PASSWORD)

    def send_message(self, sender, to, subject, text):
        sended = False
        msg = email.mime.text.MIMEText(text, _charset='utf-8')
        msg['From'] = sender
        msg['To'] = to
        #msg['Date'] = email.Utils.formatdate(localtime=True)
        msg['Subject'] = subject
        print msg.as_string()
        while not sended:
            try:
                self.smtp_connection.sendmail(sender, to, msg.as_string())
                sended = True
            except smtplib.SMTPServerDisconnected:
                time.sleep(5)
                self.connect()


_ms = MessageSender()


def send_message(to, subject, text):
    thread.start_new_thread(_ms.send_message, ('', to, subject, text))


if __name__ == "__main__":
    s = MessageSender()
    s.send_message('vanya', 'sanchopanca.alone@gmail.com', 'Hi', 'Hi?')
