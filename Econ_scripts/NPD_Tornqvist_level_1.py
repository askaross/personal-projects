#coding utf-8

import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

root = r"F:\FlatData\NPD\CategoryMakerTronq"
output_root = r"F:\FlatData\NPD\CategoryMakerTronq\Level1"
column_names = ["outletFlag", "outletCode", "transactionWeek", "itemCode", "generationCode",
                "Amount", "Quantity", "category6", "itemName", "makerCode", "makerName"]
identifiers = ["outletFlag", "outletCode", "itemCode", "generationCode", "category6", "makerCode"]
groupings = ["outletFlag", "outletCode", "category6", "makerCode"]

for roots, dirs, filenames in os.walk(root):
    for file in filenames:
        date = datetime.strptime(file[19:27], "%Y%m%d")
        date_dt = date - relativedelta(days=364)
        if date < datetime(2012, 12, 26, 0, 0):
            print("skipping (date): {}".format(file))
            pass
        else:
            try:
            	dt = pd.read_csv(os.path.join(root, "edit_JANMAKER_W001_"+date_dt.strftime("%Y%m%d")+".csv"), header=None, names=column_names, encoding="utf-8")
            except:
                print("skipping (non-existence): {}".format(file))
                pass

            else:
                print("opening: {}".format(file))

                input = pd.read_csv(os.path.join(root, file), header=None, names=column_names, encoding="utf-8")
                temp = input.groupby(groupings)["Amount"].sum()
                input = input.merge(temp.to_frame().reset_index(), on=groupings, how="inner")

                input["Share"] = input["Amount_x"] / input["Amount_y"]
                input["UnitPrice"] = input["Amount_x"] / input["Quantity"]

                temp_dt = dt.groupby(groupings)["Amount"].sum()
                dt = dt.merge(temp_dt.to_frame().reset_index(), on=groupings, how="inner")

                dt["Share"] = dt["Amount_x"] / dt["Amount_y"]
                dt["UnitPrice"] = dt["Amount_x"] / dt["Quantity"]

                input = input.merge(dt, how="inner", on=identifiers)

                input["ln(p/p_dt)"] = np.log(input["UnitPrice_x"] / input["UnitPrice_y"])
                input["wt"] = (input["Share_x"] + input["Share_y"])/2
                input["w*ln(p)"] = input["ln(p/p_dt)"] * input["wt"]
                input = input.groupby(["outletFlag", "outletCode", "category6", "makerCode"])["Amount_x_x", "w*ln(p)"].sum()
                input = input.reset_index()

                input.to_csv(os.path.join(output_root, file), header=False, encoding="utf-8", index=False)
