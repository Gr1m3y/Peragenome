import csv_handler as csv


with open("test/test.csv", 'r+') as file:
    csv.edit_field_by_posn(0,0,"RAK", file)
