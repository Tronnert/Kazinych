from threading import Thread
import schedule
import smtplib
from data import db_session
import sqlalchemy
from flask import render_template

class Spammer:
    def __init__(self):
        print(1)
        self.server = smtplib.SMTP('smtp.mail.ru', 465)
        self.address = "spammer.noreply@mail.ru"
        self.server.starttls()
        self.server.login(self.address, 'hkV2AH1txBPhFh2D7nZa')
        self.server.sendmail(self.address, "arseniy.kolomeytsev@gmail.com", "test")
        print(1)
        #schedule.every(15).seconds.do(self.send_emails)
        self.server.quit()

    def send_emails(self):

        self.server.sendmail(self.address, "arseniy.kolomeytsev@gmail.com", "test")
        #for user in db_session.query(User).filter(User.email_flag):
