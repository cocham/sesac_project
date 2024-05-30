import csv
import uuid
import random

class OrderItem:
    def read_order(self):
        o = []
        with open('output_order.csv','r',encoding='utf-8') as file:
            freader = csv.reader(file)
            next(freader)
            for row in freader:
                o.append(row[0])
        return o
    
    def read_item(self):
        i = []
        with open('output_item.csv','r',encoding='utf-8') as file:
            freader = csv.reader(file)
            next(freader)
            for row in freader:
                i.append(row[0])
        return i
    
    def orderitem_generate(self):
        id = str(uuid.uuid4())
        order_id = random.choice(self.read_order())
        item_id = random.choice(self.read_item())

        orderitem = (id,order_id,item_id)
        return orderitem