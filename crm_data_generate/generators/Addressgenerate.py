import random
import csv

class Addressgenerate:
    def addressgenerate(self):
        file_path = 'C:/crm_data_generate/random_choice_data/residence.csv'
        with open (file_path,'r',encoding = 'utf-8') as file:
            csvreader = csv.reader(file)
            self.csv_list_cities = [n[i] for n in csvreader for i in range(len(n))] 

        self.n = ['대로','로','길']
        return f"{random.choice(self.csv_list_cities)} {random.randint(1,100)}{random.choice(self.n)} {random.randint(1,100)}"