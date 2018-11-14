#/usr/bin/env 
# output_test.py

import os, sys, csv

with open('output_file.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    ids = [ ]
    for row in reader:
        ids.append(row['id'])
for i in ids:
    print(i)