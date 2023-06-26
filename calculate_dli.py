# Import necessary libraries
import pandas as pd
from datetime import datetime
import datetime as dt
import time
from db_api import *
from config import Config

# Returns desired light intensity
def get_intensity_from_dict(light_intensities, sensor_idx):
    desired_intensity = []
    for intensity in light_intensities:
        if intensity["index"] == sensor_idx:
            desired_intensity.append(intensity)           
    return desired_intensity

# Computes the time difference between current intensity and previous intensity
def compute_time_difference(intensity, prev_intensity):
    difference = intensity - prev_intensity 
    return difference.seconds

# Computes ppfd based on lux, where 1 lux = 0.09 umol/m2s (based on online calculator: https://www.waveformlighting.com/horticulture/convert-lux-to-ppfd-online-calculator)
def compute_ppfd(lux):
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

# Drops NaN values (which were configured in the broker to be -1)
def drop_NaNs(specific_light_intensities):
    specific_light_intensities = specific_light_intensities.drop(specific_light_intensities[specific_light_intensities.value == -1].index)
    specific_light_intensities = specific_light_intensities.reset_index(drop=True)
    return specific_light_intensities

# Returns the list of dates in a dataframe
def get_list_dates(intensity_df):
    copy_df = intensity_df.copy()
    copy_df['datetime'] = pd.to_datetime(copy_df['datetime'])
    temp_list = copy_df["datetime"].map(pd.Timestamp.date).unique()
    date_list = []
    for date in temp_list:
        date_str= date.strftime('%Y-%m-%d')
        date_list.append(date_str)
    
    return date_list

# Converts DF to dictionary
def make_dict(date, expt_num, data_type, sensor_idx, integral):
    dli = integral/1000000
    dli_dict = {
        'datetime': date,
        'expt_num': expt_num,
        'type': data_type,
        'index': sensor_idx,
        'value': dli
    }
    return dli_dict

# Returns specific light intensity
def get_specific_li(index):
    connection = create_engine()
    sensor_df = get_all_values(connection, Config.sensors_table)
    filename = "li" + str(index) + ".csv"
    specific_light_intensities = sensor_df.loc[(sensor_df['type'] == 'light_intensity') & (sensor_df['index'] == index) ]
    specific_light_intensities.to_csv(filename)

# This function finds the missing dates from a certain list of dates
def find_missing_dates(existing_dates, all_dates):
    missing_dates = []
    current_date = dt.date.today()
    date_now = current_date.strftime('%Y-%m-%d')
    for date in all_dates:
        if date not in existing_dates and date != date_now:
            missing_dates.append(date)
    return missing_dates

# Function that computes all DLI of the whole DB
def compute_dli():
    expt_num = 0
    data_type = "dli"

    # Initialize connection to DB
    connection = create_engine()
    sensor_df = get_all_values(connection, Config.sensors_table)
    dli_df =  get_all_values(connection, Config.dli_table)

    # Filter to only light intensities
    intensity_df = sensor_df.loc[(sensor_df['type'] == 'light_intensity')]

    intensity_df = drop_NaNs(intensity_df)


    # Get unique indices
    light_intensity_indices = intensity_df['index'].unique()

    # Initialize variables
    datetime_temp = []
    dli_vals = []
    integral = 0 

    # Copy df to convert to datetime
    temp_df = intensity_df.copy()
    temp_df['datetime'] = pd.to_datetime(temp_df['datetime'])

    # Get list of dates
    intensity_dates = get_list_dates(intensity_df)
    dli_dates = get_list_dates(dli_df) 
   
    date_list = find_missing_dates(dli_dates, intensity_dates)
    
    for date in date_list:

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

            for i in range(len(desired_intensities)):
                date_time = convert_str_datetime(desired_intensities[i]["datetime"])
                datetime_temp.append(date_time)
                ppfd = compute_ppfd(desired_intensities[i]["value"])
                
                # Do not count the first element of the day
                if i > 0:
                    seconds_difference = compute_time_difference(datetime_temp[i], datetime_temp[i-1])
                    integral = integral + (ppfd * seconds_difference)
        
            dli_val = make_dict(date, expt_num, data_type, index, integral)
            dli_vals.append(dli_val)
    return dli_vals


# Computes DLI on a given date
def compute_dli_today(date):
    expt_num = 0
    data_type = "dli"

    # Initialize connection to DB
    connection = create_engine()
    sensor_df = get_all_values(connection, "dlsu_cherrytomato_0")

    # Filter to only light intensities
    intensity_df = sensor_df.loc[(sensor_df['type'] == 'light_intensity')]
    intensity_df = drop_NaNs(intensity_df)

    # Filter to only light intensities
    intensity_df = sensor_df.loc[(sensor_df['type'] == 'light_intensity')]
    intensity_df = drop_NaNs(intensity_df)

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

    # Get values based on date 
    specific_date_intensities = intensity_df[temp_df['datetime'].dt.normalize() == date]

    # Convert to dictionary
    intensities = df_to_dicts(specific_date_intensities)

    if specific_date_intensities.empty:
        now = dt.datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{formatted_datetime}] No data to currently process.")
    else:
        # Iterate data through indices
        for index in light_intensity_indices:
            # Get desired intensities based on index
            desired_intensities = get_intensity_from_dict(intensities, index)

            # Reinitialize variables
            integral = 0
            i = 0
            datetime_temp = []

            for i in range(len(desired_intensities)):
                date_time = convert_str_datetime(desired_intensities[i]["datetime"])
                datetime_temp.append(date_time)
                ppfd = compute_ppfd(desired_intensities[i]["value"])

                # Do not count the first element of the day
                if i > 0:               
                    seconds_difference = compute_time_difference(datetime_temp[i], datetime_temp[i-1])
                    integral = integral + (ppfd * seconds_difference)

            dli_val = make_dict(date, expt_num, data_type, index, integral)
            dli_vals.append(dli_val)
    return dli_vals

# Function that computes all DLI of the whole DB
def compute_all_dli():
    expt_num = 0
    data_type = "dli"

    # Initialize connection to DB
    connection = create_engine()
    sensor_df = get_all_values(connection, "dlsu_cherrytomato_0")

    # Filter to only light intensities
    intensity_df = sensor_df.loc[(sensor_df['type'] == 'light_intensity')]

    intensity_df = drop_NaNs(intensity_df)


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

    for date in date_list:

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

            for i in range(len(desired_intensities)):
                date_time = convert_str_datetime(desired_intensities[i]["datetime"])
                datetime_temp.append(date_time)
                ppfd = compute_ppfd(desired_intensities[i]["value"])
                
                # Do not count the first element of the day
                if i > 0:
                    seconds_difference = compute_time_difference(datetime_temp[i], datetime_temp[i-1])
                    integral = integral + (ppfd * seconds_difference)
        
            dli_val = make_dict(date, expt_num, data_type, index, integral)
            dli_vals.append(dli_val)
    return dli_vals

# Compute DLI to see what are the missing DLI in the scenario the program isn't ran for days
create_dli_table(Config.dli_table)
vals = compute_dli()


if len(vals) == 0:
    print("DLI calculations are already up to date.")
else:
    insert_dli(Config.dli_table, vals)
    print("Database has been updated with latest DLI.")


# Main function
if __name__ == '__main__':
    try:
        # Compute DLI to see what are the missing DLI in the scenario the program isn't ran for days
        create_dli_table(Config.dli_table)
        vals = compute_dli()
        insert_dli(Config.dli_table, vals)
        new_df = pd.DataFrame(vals)

        if len(vals) == 0:
            print("DLI calculations are already up to date.")
        else:
            print("Database has been updated with latest DLI.")

        print("Running DLI calculator program...")
        while True:
            now = dt.datetime.now()
            if now.hour == 23 and now.minute == 50:
                current_date = dt.date.today()
                date_now = current_date.strftime('%Y-%m-%d')
                dli_vals = compute_dli_today(date_now)
                
                if len(dli_vals) != 0:
                    insert_dli(Config.dli_table, dli_vals)
            time.sleep(60) 
    except KeyboardInterrupt:
        print("Exited.")

