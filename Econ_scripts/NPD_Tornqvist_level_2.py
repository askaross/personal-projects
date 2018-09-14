#coding utf-8

import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

root = ""
input_root = ""
output_root = ""
column_names1 = ["outletFlag", "outletCode", "category6", "makerCode", "Amount", "index1"]
column_names2 = ["outletFlag", "outletCode", "transactionWeek", "itemCode", "generationCode",
                "Amount", "Quantity", "category6", "itemName", "makerCode", "makerName"]
identifiers = ["outletFlag", "outletCode", "category6", "makerCode"]
groupings = ["category6", "makerCode"]


for roots, dirs, filenames in os.walk(input_root):
    for file in filenames:
        date = datetime.strptime(file[14:22], "%Y%m%d")
        date_dt = date - relativedelta(days=364)
        if date < datetime(2012, 12, 26, 0, 0):
            print("skipping (date): {}".format(file))
            pass
        else:
            try:
            	dt = pd.read_csv(os.path.join(root, "JANMAKER_W001_"+date_dt.strftime("%Y%m%d")+".csv"), header=None, names=column_names2, encoding="shift-jis")
            except:
                print("skipping (non-existence): {}".format(file))
                pass

            else:
                print("opening: {}".format(file))

                input = pd.read_csv(os.path.join(input_root, file), header=None, names=column_names, encoding="utf-8"):
                temp = input.groupby(groupings)["Amount"].sum()
                input = input.merge(temp.to_frame().reset_index(), on=groupings, how="inner")

                input["Share"] = input["Amount_x"] / input["Amount_y"]

                dt = dt.groupby(identifiers)["Amount"].sum().reset_index
                temp_dt = dt.groupby(groupings)["Amount"].sum()
                dt = dt.merge(temp.to_frame().reset_index(), on=groupings, how="inner")

                dt["Share"] = dt["Amount_x"] / dt["Amount_y"]

                input = input.merge(dt, on=identifiers, how="inner")

                input["wt"] = (input["Share_x"] + input["Share_y"]) / 2
                input["w*index"] = input["wt"] * input["index1"]

                input = input.groupby(groupings)["Amount_x_x", "w*index"].sum()
                input = input.reset_index()

                input.to_csv(os.path.join(output_root, file), header=False, encoding="utf-8", index=False)
