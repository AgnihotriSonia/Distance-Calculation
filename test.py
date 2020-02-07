import csv
import collections

input_data = 'test_input.csv'
def readfile(filepath):
    hybrid_type = []
    lat =[]
    lng = []
    with open(filepath,'r') as input:
        csvreader = csv.reader(input, delimiter= ',', quotechar = '"')
        next(csvreader, None)
        for row in csvreader:
            hybrid = row[1]
            hybrid_type.append(hybrid)
    return hybrid_type

print(readfile(input_data))

