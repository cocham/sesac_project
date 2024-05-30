import random

class Birthgenerate:
    def generate_birth(self):
        y = random.randint(1940,2024)
        m = random.randint(1,12)
        d = random.randint(1,28)   
        return f"{y}-{m:02d}-{d:02d}"