import pandas as pd
import matplotlib.pyplot as plt
from db_api import *

def ave (pt1, pt2):
    return (pt1 + pt2)/2

def diff(pt1, pt2):
    if abs(pt1 - pt2) > 3:
        return True
    return False

def interpolate (x,y):
    marker = diff(x[1], y[1])

    if marker:
        if abs(x[0] - x[1]) > abs(y[0] - y[1]):
            x[1] = ave(x[1], y[1])
        else:
            y[1] = ave(x[1], y[1])

engine = create_engine()
tmp_df_0 = get_values(engine, "dlsu_cherrytomato_0", "0", "temperature")
tmp_df_1 = get_values(engine, "dlsu_cherrytomato_0", "1", "temperature")



ax = tmp_df_0.plot(x='datetime', y='value', kind='line')
tmp_df_1.plot(x='datetime', y='value', kind='line', ax=ax)
plt.savefig("graph.jpg")


# create_pred_table("interpolated-0")


# Find the values that needs to be interpolated


# Plot the values first 

# Copy that row, insert edit type as old_value, replace that row with the updated value
