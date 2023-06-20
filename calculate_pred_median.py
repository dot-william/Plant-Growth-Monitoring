import pandas as pd
from datetime import datetime
import datetime as dt
import time
from db_api import *

# Converts DF to dictionary
def make_dict(date, expt_num, data_type,  value):
    dli_dict = {
        'datetime': date,
        'expt_num': expt_num,
        'type': data_type,
        'value': value
    }
    return dli_dict


# Returns the list of dates in a dataframe
def get_list_dates(df):
    copy_df = df.copy()
    copy_df['datetime'] = pd.to_datetime(copy_df['datetime'])
    temp_list = copy_df["datetime"].map(pd.Timestamp.date).unique()
    date_list = []
    for date in temp_list:
        date_str= date.strftime('%Y-%m-%d')
        date_list.append(date_str)
    
    return date_list

# Function that computes median given date_list
def compute_median_given_dates(date_list):
    expt_num = 0
    append_str_median = "_median"
    # append_str_mean = "_mean"
    
    data_types = ["pred_leaf_count", "pred_flower_count", "pred_fruit_count"]
    connection = create_engine()
    preds_df = get_all_preds(connection, "pred_table_0")
    
    count_df = preds_df[(preds_df["type"] == data_types[0]) | (preds_df["type"] == data_types[1]) | (preds_df["type"] == data_types[2])]
    
    temp_df = count_df.copy()
    temp_df['datetime'] = pd.to_datetime(temp_df['datetime'])
    
    vals = []
    for date in date_list:
        # Get values from sepecific date
        specific_date_counts = count_df[temp_df['datetime'].dt.normalize() == date]
        for pred_type in data_types:
            prediction = specific_date_counts[(specific_date_counts["type"] == pred_type)]
            median = prediction["value"].median()
            # mean = prediction["value"].mean()
            val = make_dict(date, expt_num, pred_type+append_str_median, median)
            vals.append(val)
            # val = make_dict(date, expt_num, pred_type+append_str_mean, mean)
            # vals.append(val)
    return vals


def compute_all_median():
    expt_num = 0
    append_str_median = "_median"
    # append_str_mean = "_mean"
    
    data_types = ["pred_leaf_count", "pred_flower_count", "pred_fruit_count"]
    connection = create_engine()
    preds_df = get_all_preds(connection, "pred_table_0")
    
    count_df = preds_df[(preds_df["type"] == data_types[0]) | (preds_df["type"] == data_types[1]) | (preds_df["type"] == data_types[2])]
    date_list = get_list_dates(count_df)
    
    temp_df = count_df.copy()
    temp_df['datetime'] = pd.to_datetime(temp_df['datetime'])
    
    vals = []
    for date in date_list:
        # Get values from sepecific date
        specific_date_counts = count_df[temp_df['datetime'].dt.normalize() == date]
        for pred_type in data_types:
            prediction = specific_date_counts[(specific_date_counts["type"] == pred_type)]
            median = prediction["value"].median()
            mean = prediction["value"].mean()
            val = make_dict(date, expt_num, pred_type+append_str_median, median)
            vals.append(val)
            # val = make_dict(date, expt_num, pred_type+append_str_mean, mean)
            # vals.append(val)
    return vals

# Function that computes median of predictions in a given date 
def compute_median(date):
    expt_num = 0
    append_str_median = "_median"
    # append_str_mean = "_mean"
    
    data_types = ["pred_leaf_count", "pred_flower_count", "pred_fruit_count"]
    connection = create_engine()
    preds_df = get_all_preds(connection, "pred_table_0")
    
    count_df = preds_df[(preds_df["type"] == data_types[0]) | (preds_df["type"] == data_types[1]) | (preds_df["type"] == data_types[2])]
    date_list = get_list_dates(count_df)
    
    temp_df = count_df.copy()
    temp_df['datetime'] = pd.to_datetime(temp_df['datetime'])
    
    vals = []
    # Get values from sepecific date
    specific_date_counts = count_df[temp_df['datetime'].dt.normalize() == date]
    for pred_type in data_types:
        prediction = specific_date_counts[(specific_date_counts["type"] == pred_type)]
        median = prediction["value"].median()
        mean = prediction["value"].mean()
        val = make_dict(date, expt_num, pred_type+append_str_median, median)
        vals.append(val)
        # val = make_dict(date, expt_num, pred_type+append_str_mean, mean)
        # vals.append(val)
    return vals



def get_specific_pred(pred_type):
    connection = create_engine()
    preds_df = get_all_preds(connection, "pred_table_0")
    filename = pred_type + ".csv"
    pred_csv= preds_df.loc[(preds_df ['type'] == pred_type)]
    pred_csv = sort_by_date(pred_csv)
    pred_csv.to_csv(filename)

def sort_by_date(preds):
    temp = preds.copy()
    temp["datetime"] = pd.to_datetime(temp["datetime"])
    sorted_preds = temp.sort_values(by='datetime')
    return sorted_preds

def df_to_dicts(df):
    dict = df.to_dict('records')
    return dict

vals = compute_median("2023-04-22")
print(pd.DataFrame(vals))
if __name__ == '__main__':
    try:
        print("Running prediction median calculator program...")
        while True:
            now = dt.datetime.now()
            if now.hour == 23 and now.minute == 50:
                current_date = dt.date.today()
                date_now = current_date.strftime('%Y-%m-%d')
                dli_vals = compute_median(date_now)
                insert_dli("dli_table_0", dli_vals)
                formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{formatted_datetime}] Insert successful")     
            time.sleep(60) 
    except KeyboardInterrupt:
        print("Exited.")