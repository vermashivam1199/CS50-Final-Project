from project import phones, data_extracter, AMAZON_SMARTPHONES_LINK, setup, csv_maker
import csv
import os

def test_phones():
    phones(AMAZON_SMARTPHONES_LINK, setup())

def test_data_extractor():
    data_extracter(setup())

def test_csv():
    list_of_dict = [{
                        'test1':'1'
                        ,'test2':'2'
                        ,'test3':'3'
                    }]
    csv_maker(list_of_dict, 'test.csv')
    
    with open("test.csv", "r") as file:
        reader = csv.DictReader(file)
        for csv_row, lis_row in zip(reader, list_of_dict):
            assert csv_row['test1'] == lis_row['test1']
            assert csv_row['test2'] == lis_row['test2']
            assert csv_row['test3'] == lis_row['test3']
    os.remove("test.csv")
