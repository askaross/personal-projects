#coding:utf-8

import csv
import os

root = r"F:\FlatData\L.POINT\phase2_2\source"

class multiCSVManager():
    ##Class to open multiple files and write to them line by line

    def __init__(self, dir: str, date: str):
        self.dir = dir
        self.date = date
        self.valid_categories = {"A", "B", "C", "D", "E"}  #Used to flag unexpected categories

    def __enter__(self):
        #Initialize categories
        self.categories = {} #Type: dict [category]: file, csv.writer()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #After writing, all files are closed, then categories are cleared
        for file, csv_writer in self.categories.values():
            print("closing file: {}".format(file.name))
            file.close()

        self.categories.clear()

    def csvWriter(self, filename: str):
        if filename not in self.categories:
            #Unexpected category flag
            if filename not in self.valid_categories:
                print("UNKNOWN CATEGORY: {}".format(filename))

            filepath = os.path.join(self.dir, filename+"_"+self.date+".csv")
            print("opening file: {}".format(filepath))
            file = open(filepath, "w", newline='')

            self.categories[filename] = file, csv.writer(file)
        return self.categories[filename][1]

if __name__ == "__main__":
    #Iterate over all folders in the root
    for roots, dirs, filenames in os.walk(root):
        for d in dirs:
            directory = os.path.join(root, d)
            #Within each folder, create a file for each specific category with date (format: category_date.csv)
            with multiCSVManager(directory, d) as file_manager:
                for file in os.listdir(directory):
                    #Check if valid file
                    if not file.endswith(".tar.gz") and file !=  "_SUCCESS":

                        with open(os.path.join(directory, file), "r") as file_pipe:
                            reader_pipe = csv.reader(file_pipe, delimiter="|")

                            try:
                                for row in reader_pipe:
                                    csv_filename = row[2][2]
                                    writer = file_manager.csvWriter(csv_filename)
                                    writer.writerow(row)
                            except UnicodeDecodeError:
                                writer = file_manager.csv_writer("ERROR")
                                writer.writerow(file)
