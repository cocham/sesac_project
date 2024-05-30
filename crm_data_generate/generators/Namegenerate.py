import random
import csv

class Namegenerator:
    def __init__(self):
        file_path = 'C:/crm_data_generate/random_choice_data/names.csv'
        with open(file_path,'r',encoding='utf-8') as file:
            csvreader = csv.reader(file)
            self.csv_list_names = [n[i] for n in csvreader for i in range(len(n))]
            
    def generate_name(self):
        return random.choice(self.csv_list_names)