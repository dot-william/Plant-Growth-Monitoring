import sys
import time
import logging
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
import os
import shutil
import datetime as dt
import time
from db_api import *

def process_txt_files(filename):
    path = filename
    cols = ['class', 'x','y','w','h']
    df = pd.read_csv(path, sep=' ', names=cols)
    
    flower_count = (df['class'] == 0).sum()
    leaf_count = (df['class'] == 1).sum()
    fruit_count = (df['class'] == 2).sum()
    return leaf_count, flower_count, fruit_count

def create_pred_dict(leaf_count, flower_count, fruit_count, filename_date):
    d_leaf = {}
    d_flower = {}
    d_fruit = {}
    expt_num = 0

    d_leaf["datetime"] = getDatetime(filename_date)
    d_leaf["expt_num"] = expt_num
    d_leaf["type"] = "pred_leaf_count"
    d_leaf["value"] = leaf_count
    
    d_flower["datetime"] = getDatetime(filename_date)
    d_flower["expt_num"] = expt_num
    d_flower["type"] = "pred_flower_count"
    d_flower["value"] = flower_count
    

    d_fruit["datetime"] = getDatetime(filename_date)
    d_fruit["expt_num"] = expt_num
    d_fruit["type"] = "pred_fruit_count"
    d_fruit["value"] = fruit_count
    

    return d_leaf, d_flower, d_fruit

def create_folders():
    today = dt.datetime.today()
    present_date = Path(today.strftime("%Y_%m_%d"))

    output_processed_path = Path("Outputs_Processed")
    
    # If directory does not exists
    if not os.path.isdir(output_processed_path):
        os.mkdir(output_processed_path)
        print("Created directory successfully")
    
    os.makedirs(output_processed_path / present_date, exist_ok=True) # Make forlder if doesn't exist
    return output_processed_path, present_date 

def countOutput(output_processed_path, present_date_path):
    # path = ".\Outputs"
    path = Path("Outputs")
    dirlist = os.listdir(path)
    results = []
    if  dirlist == []:
        print("No files found in directory")
    else:
        # To append result to array dictionaries
        try:
            for root, directories, filenames in os.walk(path):
                for filename in filenames:
                    if ".txt" in filename:
                        path = os.path.join(root, filename)
                        leaf_count, flower_count, fruit_count = process_txt_files(path)

                        d_leaf, d_flower, d_fruit = create_pred_dict(leaf_count, flower_count, fruit_count, filename)
                        
                        date_str, time_str = split_datetime(filename)
                        # d_leaf['filename'] = filename
                        # d_flower['filename'] = filename
                        # d_fruit['filename'] = filename

                        
                        # d_leaf['path'] = os.path.join(root, filename)
                        # d_flower['path'] = os.path.join(root, filename)
                        # d_fruit['path'] = os.path.join(root, filename)
                        results.append(d_leaf)
                        results.append(d_flower)
                        results.append(d_fruit)

                        # Move from path to dest
                        shutil.move(path, output_processed_path / present_date_path / filename)
                       
        except:
            print("An error has occured when trying to count outputs.")

    return results

def split_datetime(filename):
    filename = filename.split(".") # if .txt is being read
    split_datetime = filename[0].split("_")
    # Format date
    date_str = split_datetime[1]
    date_str = date_str[:4] + "-" + date_str[4:6] + "-" + date_str[6:]

    # Format time
    time_str = split_datetime[2]
    time_str = time_str[:2] + ":" + time_str[2:] + ":00"

    return date_str, time_str

def getDatetime(filename):
    '''
    This function parses the string to get the datetime and returns date format, assumes the filename format is IMG_DATE_TIME
    '''
    try:
        date_str, time_str = split_datetime(filename)
        date_time = date_str + " " + time_str
        # print(date_str, time_str)
        date_object = dt.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        # print(date_object)
    except Exception as e:
        print("An error has occured when trying to parse dates. Check filename of outputs.", e)
    
    return date_object

def perform_count_dl_output():
    # Create necessary folders to store the output
    output_processed_path, present_date_path = create_folders()
    result = countOutput(output_processed_path, present_date_path)
    # Store df to db
    if (len(result) > 0):
        print("Len of df:", len(result))
        df = pd.DataFrame(result)
        insert_predictions_data("pred_table_0", result)
        print(df.head())
        print("Stored to db")
            
    else:
        print("Nothing was stored to the DB")

# Watchdog Specific functions
# def on_created(event):
#     print("A file was created")
#     # perform_count_dl_output()

# def on_deleted(event):
#     print("Deleted")

# def on_modified(event):
#     countOutput()
#     print("modified")
#     # Check all the folders in the directory


# def on_moved(event):
#     print("Moved")


if __name__ == "__main__":

#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
    path = Path("Outputs")
    # Always process path file
    # event_handler = FileSystemEventHandler()
    

#     # event_handler.on_any_event = on_any_event
    # event_handler.on_created = on_created
    # event_handler.on_deleted = on_deleted
    # event_handler.on_modified = on_modified
    # event_handler.on_moved = on_moved


    # observer = Observer()
    # observer.schedule(event_handler, path, recursive=True)
    minute_interval = range(0,60,1)

    # observer.start()
    try:
        print("Monitoring.")
        while True:
            current_time = dt.datetime.now().time()
            if current_time.minute in minute_interval:
                print(f"[TIME {current_time.hour}:{current_time.minute}] Counting text file...")
                perform_count_dl_output()
            time.sleep(1)
    except KeyboardInterrupt:
        # observer.stop()
        print("Exited.")
    # observer.join()