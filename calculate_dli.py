# Import necessary libraries
import pandas as pd
from datetime import datetime
import datetime as dt
import numpy as np

from db_api import *

# Functions

def get_interval():
    # Convert data[n]
    pass


# Returns desired light intensity
def get_intensity_from_dict(light_intensities, sensor_idx):
    desired_intensity = []
    for intensity in light_intensities:
        if intensity["index"] == sensor_idx:
            desired_intensity.append(intensity)           
    return desired_intensity

def remove_intensity_from_dict(desired_intensities, orig_intensities):
    [i for i in test_list if i not in remove_list]

def compute_time_difference(intensity, prev_intensity):
    difference = intensity - prev_intensity 
    # print(intensity, "-", prev_intensity , "=", difference.seconds)
    return difference.seconds

def compute_ppfd(lux):
    # 1 lux = 0.09 umol/m2s (based on online calculator: https://www.waveformlighting.com/horticulture/convert-lux-to-ppfd-online-calculator)
    return lux * 0.09

# Convert df to list of dictionaries
def df_to_dicts(df):
    dict = df.to_dict('records')
    return dict



# Convert column to datetime 
def convert_str_datetime(date_time_str):
    
    try:
        date_time_str = str(date_time_str)
        converted = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except:
        date_obj = datetime.datetime.strptime(date_time_str, '%m/%d/%Y %H:%M')
        date_str = datetime.datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S')
        converted = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    
    return converted

# Get it per date
def perform_per_date():
    pass

# def drop_NaNs(specific_light_intensities):
#     specific_light_intensities = specific_light_intensities.dropna()
#     specific_light_intensities = specific_light_intensities.reset_index(drop=True)
#     return specific_light_intensities

# def check_type(df):
#     print(type(df["value"]))

def drop_NaNs(specific_light_intensities):
    specific_light_intensities = specific_light_intensities.drop(specific_light_intensities[specific_light_intensities.value == -1].index)
    specific_light_intensities = specific_light_intensities.reset_index(drop=True)
    return specific_light_intensities

def get_list_dates(intensity_df):
    copy_df = intensity_df.copy()
    copy_df['datetime'] = pd.to_datetime(copy_df['datetime'])
    temp_list = copy_df["datetime"].map(pd.Timestamp.date).unique()
    date_list = []
    for date in temp_list:
        date_str= date.strftime('%Y-%m-%d')
        date_list.append(date_str)
    
    return date_list


def make_dict(date, expt_num, data_type, sensor_idx, integral):
    dli = integral/1000000
    dli_dict = {
        'datetime': date,
        'expt_num': expt_num,
        'type': data_type,
        'sensor_idx': sensor_idx,
        'value': dli
    }
    return dli_dict

def get_specific_li(index):
    connection = create_engine()
    sensor_df = get_all_values(connection, "dlsu_cherrytomato_0")
    filename = "li" + str(index) + ".csv"
    specific_light_intensities = sensor_df.loc[(sensor_df['type'] == 'light_intensity') & (sensor_df['index'] == index) ]
    specific_light_intensities.to_csv(filename)


def compute_all_dli():
    expt_num = 0
    data_type = "dli"

    # Initialize connection to DB
    connection = create_engine()
    sensor_df = get_all_values(connection, "dlsu_cherrytomato_0")
    # print(sensor_df.head())
    # Filter to only light intensities
    intensity_df = sensor_df.loc[(sensor_df['type'] == 'light_intensity')]
    # print("[BEFORE DROPPING NAN] Len of light_intensities: ", len(intensity_df))
    intensity_df = drop_NaNs(intensity_df)
    # print("[AFTER DROPPING NAN] Len of light_intensities: ", len(intensity_df))

    # Get unique indices
    light_intensity_indices = intensity_df['index'].unique()
    # print("Indices from light intensity:", light_intensity_indices)

    # Initialize variables
    datetime_temp = []
    dli_vals = []
    integral = 0 

    # Copy df to convert to datetime
    temp_df = intensity_df.copy()
    temp_df['datetime'] = pd.to_datetime(temp_df['datetime'])

    # Get list of dates
    date_list = get_list_dates(intensity_df)
    # print("List of dates (len:", len(date_list), "):", date_list)

    for date in date_list:
        # print("Date being processed:", date)
        
        # Get values based on date 
        specific_date_intensities = intensity_df[temp_df['datetime'].dt.normalize() == date]
        
        # Convert to dictionary
        intensities = df_to_dicts(specific_date_intensities)

        # Iterate data through indices
        for index in light_intensity_indices:
            # Get desired intensities based on index
            desired_intensities = get_intensity_from_dict(intensities, index)

            # Reinitialize variables
            integral = 0
            i = 0
            datetime_temp = []

            # print("INDEX BEING PROCESSED", index)
            for i in range(len(desired_intensities)):
                # print("Test: ",desired_intensities[i]["datetime"])
                date_time = convert_str_datetime(desired_intensities[i]["datetime"])
                datetime_temp.append(date_time)
                ppfd = compute_ppfd(desired_intensities[i]["value"])
                
                # Do not count the first element of the day
                if i > 0:
                    # ppfds.append(ppfd)
                    seconds_difference = compute_time_difference(datetime_temp[i], datetime_temp[i-1])
                    # differences.append(seconds_difference)
                    integral = integral + (ppfd * seconds_difference)
        
            dli_val = make_dict(date, expt_num, data_type, index, integral)
            dli_vals.append(dli_val)
    return dli_vals

def store_dli():
    pass

# Program is concurrently running, and it will compute DLI for day
def compute_dli(df):
    # Check if it is the last time of the day 
    
    # Get all light intensity within the day

    # Convert light intensity to ppfd

    # ppfd = df.to_dict()
    # ppfd_list.append(ppfd)
    # Get interval

    # store to sum variable
    # 
    pass

# Get data from db (is pandas df)


if __name__ == '__main__':

    dli_vals = compute_all_dli()
    df_temp = pd.DataFrame(dli_vals)
    print(df_temp.head())
    # df_temp.to_csv("dli_temp.csv")
    # get_specific_li(0)
    # try:
    # except:
    #     print("An unexpected error has occured")
    #     # Email unexpected error

