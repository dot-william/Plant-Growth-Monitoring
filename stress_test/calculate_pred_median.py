import pandas as pd
from datetime import datetime
import datetime as dt
import time
from db_api import *
from config import Config

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

# This function finds the missing dates from a certain list of dates
def find_missing_dates(existing_dates, all_dates):
    missing_dates = []
    current_date = dt.date.today()
    date_now = current_date.strftime('%Y-%m-%d')
    for date in all_dates:
        # Excludes date today
        if date not in existing_dates and date != date_now:
            missing_dates.append(date)
    return missing_dates

# Function that computes median prediction 
def compute_median():
    expt_num = int(Config.experiment_num)
    append_str_median = "_median"
    
    data_types = ["pred_leaf_count", "pred_flower_count", "pred_fruit_count"]
    connection = create_engine()

    preds_df = get_all_preds(connection, Config.predictions_table)
    medians_df = get_all_preds(connection, Config.pred_median_table)
    preds_df = sort_by_date(preds_df)
    
    # Filter with just the desired data types
    count_df = preds_df[(preds_df["type"] == data_types[0]) | (preds_df["type"] == data_types[1]) | (preds_df["type"] == data_types[2])]
    
    count_date_list = get_list_dates(count_df)
    median_date_list = get_list_dates(medians_df)

    # Find the dates whose medians are not calculated yet
    date_list =  find_missing_dates(median_date_list, count_date_list)

    temp_df = count_df.copy()
    temp_df['datetime'] = pd.to_datetime(temp_df['datetime'])
    
    vals = []
    for date in date_list:
        # Get values from sepecific date
        specific_date_counts = count_df[temp_df['datetime'].dt.normalize() == date]
        for pred_type in data_types:
            prediction = specific_date_counts[(specific_date_counts["type"] == pred_type)]
            median = prediction["value"].median()
            val = make_dict(date, expt_num, pred_type+append_str_median, median)
            vals.append(val)
    return vals

# Computes median on a given date
def compute_median_today(date):
    expt_num = 0
    append_str_median = "_median"
    # append_str_mean = "_mean"
    
    data_types = ["pred_leaf_count", "pred_flower_count", "pred_fruit_count"]
    connection = create_engine()
    df1 = get_pred_type_date(connection, Config.predictions_table, data_types[0], date)
    df2 = get_pred_type_date(connection, Config.predictions_table, data_types[1], date)
    df3 = get_pred_type_date(connection, Config.predictions_table, data_types[2], date)
    preds_df = pd.concat([df1, df2, df3], ignore_index=True)
    

    vals = []

    if preds_df.empty:
        now = dt.datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{formatted_datetime}] No data to currently process.")
    else: 
        for pred_type in data_types:
            prediction = preds_df[(preds_df["type"] == pred_type)]
            median = prediction["value"].median()
            # mean = prediction["value"].mean()
            val = make_dict(date, expt_num, pred_type+append_str_median, median)
            vals.append(val)
            # val = make_dict(date, expt_num, pred_type+append_str_mean, mean)
            # vals.append(val)
    return vals

def get_specific_pred(pred_type):
    connection = create_engine()
    preds_df = get_all_preds(connection, Config.predictions_table)
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


# Main function

now = dt.datetime.now()
current_date = dt.date.today()
date_now = current_date.strftime('%Y-%m-%d')

start_time = time.time()
median_vals = compute_median_today("2023-07-20")
end_time = time.time()
perf = end_time - start_time

df1 = pd.DataFrame(median_vals)

print("DF1!!!", df1.head())
print("peroformance: ", perf)

