import requests
import schedule
import time

class Clicker:
    def __init__(self):
        sc = schedule.Scheduler()
        sc.every(10).minutes.do(self.do)
        while True:
            sc.run_pending()
            time.sleep(1)

    def do(self):
        print(2)
        a = requests.get('http://kazinych.herokuapp.com')