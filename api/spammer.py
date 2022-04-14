from threading import Thread
import schedule
import smtplib
from data import db_session
import sqlalchemy
from flask import render_template
import time
from datetime import datetime
from data.users import User
from data.balance_changes import BalanceChanges

class Spammer:
    def __init__(self):
        schedule.every(24).hours.do(self.send_emails)
        while True:
            schedule.run_pending()
            time.sleep(1)


    def send_emails(self):
        print(1)
        self.server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        self.address = "spammer.noreply@mail.ru"
        self.server.login(self.address, 'hkV2AH1txBPhFh2D7nZa')
        for user in db_session.create_session().query(User).filter(User.email_flag):
            if (datetime.now() - \
                    db_session.create_session().query(BalanceChanges).filter(BalanceChanges.user_id ==
                                                                                         user.id).order_by(BalanceChanges.date.desc()).first().date).total_seconds() > 172800:
                self.server.sendmail(self.address, user.email, str((datetime.now() - \
                    db_session.create_session().query(BalanceChanges).filter(BalanceChanges.user_id ==
                                                                                         user.id).order_by(BalanceChanges.date.desc()).first().date).total_seconds()))
        self.server.quit()
