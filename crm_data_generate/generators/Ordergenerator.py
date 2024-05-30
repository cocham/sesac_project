import random
import csv
import uuid
from datetime import datetime, timedelta

# StoreId,UserId는 csv파일에서 읽어와야됨.

class Ordergenerator:
    def read_user(self):
        u = []
        with open('output_user.csv','r',encoding='utf-8') as file:
            freader = csv.reader(file)
            next(freader) #헤더제거
            for row in freader:
                u.append(row[0])
        return u
    
    def read_store(self):
        s = []
        with open('output_store.csv','r',encoding='utf-8') as file:
            freader = csv.reader(file)
            next(freader) #헤더제거
            for row in freader:
                s.append(row[0])
        return s

    def order_generate(self):
        st = datetime(2023,1,1)
        et = datetime(2024,5,1)
        rt = random.randint(0,(et-st).total_seconds())
        id = str(uuid.uuid4())
        order_at = str(st + timedelta(seconds = rt))
        user_id = random.choice(self.read_user())
        store_id = random.choice(self.read_store())
        order = (id,order_at,user_id,store_id)
        return order