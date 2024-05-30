import random
import uuid
from generators.Itemgenerate import Itemgenerate

class Datagerator_item:
    numbers = 1
    data = []
    def __init__(self,numbers):
        self.numbers = numbers
        self.item_gen = Itemgenerate()

    def generate_item(self):
        self.data = []
        for _ in range(self.numbers):
            id = str(uuid.uuid4())
            random_item = self.item_gen.generate_items()
            name = ' '.join(random_item[:2])
            type = random_item[1]
            unitprice = random_item[2]
            a_item = (id,name,type,unitprice)
            self.data.append(a_item)
        return self.data