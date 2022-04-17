import schedule
import smtplib
from data import db_session
from flask import render_template
import time
from datetime import datetime
from data.users import User
from data.balance_changes import BalanceChanges
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_login import current_user

class Spammer:
    def __init__(self, app):
        self.app = app
        schedule.every(15).seconds.do(self.send_emails)
        while True:
            schedule.run_pending()
            time.sleep(1)


    def send_emails(self):
        print(1)
        self.server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        self.address = "spammer.noreply@mail.ru"
        self.server.login(self.address, 'hkV2AH1txBPhFh2D7nZa')
        db_sess = db_session.create_session()
        for user in db_session.create_session().query(User).filter(User.email_flag):
            if (datetime.now() - db_sess.query(BalanceChanges).filter(BalanceChanges.user_id == user.id).order_by(BalanceChanges.date.desc()).first().date).total_seconds() > 0:
                dt = (datetime.now() - db_sess.query(BalanceChanges).filter(BalanceChanges.user_id == user.id).order_by(BalanceChanges.date.desc()).first().date).total_seconds()
                msg = MIMEMultipart("alternative")
                msg["Subject"] = "Not spam"
                msg["From"] = "spammer.noreply@mail.ru"
                with self.app.app_context():
                    html_msg = MIMEText(render_template('email.html', name=user.name, time=dt), "html")
                    print(type(html_msg))
                    msg.attach(html_msg)
                self.server.sendmail(self.address, user.email, msg.as_string())
                print(2)
        self.server.quit()