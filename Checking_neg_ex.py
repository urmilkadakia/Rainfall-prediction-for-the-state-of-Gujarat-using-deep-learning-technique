import csv

neg =0
ex = 0
wrong = 0
with open('RAIN2016.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    # skipping header row
    next(reader)
    for row in reader:
         if float(row[11]) < 0:
             print('Neg', row)
             neg = neg + 1
         if float(row[11]) > 100:
             print('Ex', row)
             ex = ex +1
        #if float(row[11]) == 1023:
         #   print(row)
          #  wrong = wrong + 1
print(neg, ex)