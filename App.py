import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

class App:

    def __init__(self, SRC, OUT):
        self.file_ = None
        self.type = None
        self.file_name = None
        self.date = None
        self.user = None
        self.tempz = None
        self.tempy = None
        self.tempx = None
        self.unique_col = []
        self.src = SRC
        self.out = OUT
        self.filelist = []
        self.list_files()
        self.flag = True
        self.dict = {}
        self.data = {
        }
        self.values_important = [20, 220, 420, 620, 820, 1020, 1220, 1420, 1620, 1820, 2020]
        self.df = pd.DataFrame(self.data)
        self.create_df("ID", "File_name", "Operator", "Date", "Temp", "TempX", "TempY", "TempZ", "Type",
                       20, 220, 420, 620, 820, 1020, 1220, 1420, 1620, 1820, 2020)

    def unique_columns(self):
        self.unique_col = sorted(set(self.unique_col))

    def create_df(self, *columns):
        if columns:
            for column in columns:
                self.df[column] = 1

    def insert_df(self, dicts):
        # self.df.shape - gives the number of rows
        self.df.loc[self.df.shape[0], [a for a in self.df.keys()]] = [dicts[key] for key in self.df.columns]
        self.df = self.df.astype(object)

    def init(self):
        for item in self.filelist:
            self.start(item)

    def list_files(self):
        files = os.listdir(self.src)
        time_sorted_list = files
        for item in time_sorted_list:
            if not os.path.isdir(item):
                self.filelist.append(item)

    def create_dir(self):
        if not os.path.isdir(self.out):
            os.mkdir(self.out)

    def Add_to_Df(self):
        print(self.df)

    def cleanstr(self, text):
        return text.strip().replace("'", "")

    def convert_to_float(self, value):
        return float((value.strip()).replace("'", ""))

    def start(self, file_):
        self.user = ""
        self.date = ""
        self.file_ = file_
        a = self.src + file_
        a_new = self.out + file_
        self.create_dir()
        i = 0
        with open(a, 'r') as file:
            for line in file:
                i += 1
                if i > 13 and i < 47:
                    w = line.strip()
                    if i == 14:
                        a1, b, c, d, e, f, g, h, j = [value for value in w.split(",")]
        lines_to_save = []

        with open(a, 'r') as file2:
            list_of_lines = []
            for line_number2, line2 in enumerate(file2, start=1):
                list_of_lines.append(line2)
            for l1 in range(0, len(list_of_lines) - 1):
                if l1 == 49:
                    x = list_of_lines[l1]
                if l1 == 50:
                    x = x + list_of_lines[l1]
                if l1 == 51:
                    x = x + list_of_lines[l1]
                    x = x.replace("\n", ", ")
                    y = list(x.split(","))
                    self.tempx = self.convert_to_float(y[12])
                    self.tempy = self.convert_to_float(y[13])
                    self.tempz = self.convert_to_float(y[14])
                    self.user = self.cleanstr(y[15])
                    self.date = self.cleanstr(y[16])
                    self.file_name = y[18]
                    match = re.search(r'\((.)', y[18])
                    self.type = match.group(1)


            dict = {}
            for l1 in range(0, len(list_of_lines) - 1):
                # Check if the line number is between 13 and 47 (inclusive)
                if (l1 > 12) and (l1 < 46):
                    z = list(list_of_lines[l1].split(","))
                    dict[int(z[0])] = float(z[3]) - float(z[4])
                    dict['Temp'] = float(z[5])

                if l1 == 47:
                    dict['ID'] = "-"
                    dict['File_name'] = self.file_name
                    dict['Operator'] = self.user
                    dict['Date'] = self.date
                    dict['TempX'] = self.tempx
                    dict['TempY'] = self.tempy
                    dict['TempZ'] = self.tempz
                    dict['TempZ'] = self.tempz
                    dict['Type'] = self.type
                    self.insert_df(dict)

    def df_to_csv(self, link):
        self.df.to_csv(link, sep=';')

    def get_dataframe(self):
        #for element in self.df['Date']:
            #print(len(element))
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%b-%Y')
        #print(self.df['Date'])
        return self.df
