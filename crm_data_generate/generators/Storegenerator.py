import uuid
from generators.Storegenerate import Storegenerate
from generators.Addressgenerate import Addressgenerate

class Datagenerator_store:
    numbers = 1
    data = []

    def __init__(self,numbers):
        self.numbers = numbers
        self.store_gen = Storegenerate()
        self.address_gen = Addressgenerate()
    def generate_stores(self):
        self.data = []
        for _ in range(self.numbers):
            id = str(uuid.uuid4())
            s = self.store_gen.store_generate()
            store = s[0]+' '+s[1]+str(s[2])+'호점'
            type = s[0]
            adds = self.address_gen.addressgenerate()
            a_store = (id,store,type,adds)
            self.data.append(a_store)
            
        return self.data