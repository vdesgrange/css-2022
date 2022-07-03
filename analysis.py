import csv
from statistics import mean, stdev
import os

cwd = os.getcwd ()


def average(filen = "data/max_avg_spread_example_1000_ER.csv"):

    os.chdir('data')

    N = int(filen.split('_')[-2])

    with open(filen, mode ='r')as file:
   
        # reading the CSV file
        avg = []
        csvFile = csv.reader(file)
        
        # displaying the contents of the CSV file
        for lines in csvFile:
                avg.append(float(lines[0]))

    os.chdir(cwd)

    return N, mean(avg), stdev(avg)



def calculate_avg(file_list):

    for f in file_list:
        print(average(f))


if __name__ == "__main__":

    calculate_avg(os.listdir('data'))



