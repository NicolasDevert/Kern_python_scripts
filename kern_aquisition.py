from Kern_class import Kerns
import os
import time
import csv


ks = Kerns()
file_name = 'C:\\Users\\ndevert\\Documents\\INRA\\repo\\python\\balance_Camille\\mesure_balance.csv'


while True:
    dict = ks.getWeights()
    print(dict)

    if os.path.isfile(file_name):
        with open(file_name, 'a', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(dict.values())
    else:
        with open(file_name, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(dict.keys())
            writer.writerow(dict.values())
    time.sleep(900)