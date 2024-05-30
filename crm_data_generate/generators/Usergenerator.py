import csv
import uuid
from datetime import datetime
from generators.Namegenerate import Namegenerator
from generators.Gendergenerate import Genderganerate
from generators.Birthgenerate import Birthgenerate
from generators.Addressgenerate import Addressgenerate

class DataGenerator:
    numbers = 1
    data = []

    def __init__(self,numbers):
        self.numbers = numbers
        self.name_gen = Namegenerator()
        self.gender_gen = Genderganerate()
        self.Birth_gen = Birthgenerate()
        self.Address_gen = Addressgenerate()
        
    def calc_age(self,b):
        return datetime.today().year - int(b[:4]) + 1

    def generate_users(self):
        self.data = []
        for _ in range(self.numbers):
            id = str(uuid.uuid4())
            name = self.name_gen.generate_name()
            gen = self.gender_gen.generate_gen()
            birth = self.Birth_gen.generate_birth()
            age = self.calc_age(birth)
            addr = self.Address_gen.addressgenerate()
            a_user = (id,name,gen,age,birth,addr)
            self.data.append(a_user)
        return self.data