import csv
import pandas as pd

with open('December.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
	    print(lines)
    

df = pd.read_csv('bijlage.csv', delimiter=';', decimal=',')  # 'bijlage.txt' in your case
sellerRating_median = df['sellerRating'].median()
print('Seller rating median: {}'.format(sellerRating_median)