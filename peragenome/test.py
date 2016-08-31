import csv_handler as csv

with open("test/test.csv", 'r+') as f:
    csv.swap_columns_by_title("1","2",f)

