import random
import json
import uuid

class Itemgenerate:
    def __init__(self):
        self.id_gen = str(uuid.uuid4())
        file_path = 'C:/crm_data_generate/random_choice_data/items.json'
        with open(file_path,'r') as file:
            file = file.read()
            self.item = json.loads(file)

        self.category = list(map(str,self.item.keys())) #['Coffee', 'Juice', 'Cake']
        self.item_type = {}
        for i in range(len(self.category)):
            self.item_type.update({self.category[i]:[v for v in self.item[self.category[i]]]})
        
        self.price_dict = {}
        for j in range(len(self.category)):
            self.price_dict.update(self.item[self.category[j]])

    def generate_items(self):
        r = [k for k in self.price_dict.keys()]
        item = random.choice(r)
        return [item,''.join([k for k,v in self.item_type.items() for i in range(len(v)) if v[i] == item]),str(self.price_dict[item])]