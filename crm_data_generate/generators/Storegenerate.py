import random
import csv

class Storegenerate:
    def store_generate(self):
        f_path = 'C:/crm_data_generate/random_choice_data/stores.csv'
        with open(f_path,'r',encoding='utf-8') as file:
            csvreader = csv.reader(file)
            self.csv_list_stores = [n[i] for n in csvreader for i in range(len(n))]
        f_path2 = 'C:/crm_data_generate/random_choice_data/stores_address.csv'
        with open(f_path2,'r',encoding='utf-8') as file2:
            csvreader2 = csv.reader(file2)
            self.csv_list_stadress = [n[i] for n in csvreader2 for i in range(len(n))] 
        
        return [random.choice(self.csv_list_stores),random.choice(self.csv_list_stadress),random.randint(1,10)]
