# input code to pull from dataset

from model import User, Resource, Vote, Wapo
import pandas

df = pandas.read_csv('data.csv', index_col = 'data_id')
print(df)


#   #   function if using import csv
# def print_csv_data(filename):
#     """Prints data from a .csv file.

#     Inputs:
#     - filename: string, name of the .csv file to be read

#     Returns None.
#     """

#     with open(filename, 'test.csv') as csv_file:
#         reader = csv.reader(csv_file)
#         for row in reader:
#             print(', '.join(row))
#     csv_file.close()


# stretch goal - pull from updating dataset in WaPo (not MVP)