import csv
import os

# Navigeer naar de "data" folder met de satellietbeelden
os.chdir(r'C:\git_repositories\DDD-Python-2021\data')

# See: https://thepythonguru.com/python-how-to-read-and-write-csv-files/
with open('inleeslocaties.csv', 'r') as f:
    csv_reader = csv.reader(f)

    for line in csv_reader:
        print(line)
        print(line[0])
        print(line[1])
        print(line[2])