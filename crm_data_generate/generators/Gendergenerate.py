import random

class Genderganerate:
    def generate_gen(self):
        self.lst = ["Female","male"]
        i = random.randint(0,1)
        return self.lst[i]