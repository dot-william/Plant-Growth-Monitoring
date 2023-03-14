import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
from datetime import datetime
import os
import numpy as np
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

def create_folders(timestamps):
    if len(timestamps) > 0: 
        output_processed_path = './outputs_processed/'
        
        # If directory does not exists
        if not os.path.isdir(output_processed_path):
            os.mkdir(output_processed_path)
            print("Created directory successfully")
        
        for timestamp in timestamps:
            os.mkdir(f'{output_processed_path}{timestamp}')
            print(f"Created {output_processed_path}{timestamp}")

# def move_file():
#     for i (orig_file, filename, folder) in enumerate(zip(data[]))

def countOutput():
    path = ".\Outputs"
    dirlist = os.listdir(path)
    if  dirlist == []:
        print("No files found in directory")
    else:
        # To append result to array dictionaries
        results = []
        try:
            for root, directories, filenames in os.walk(path):
                for filename in filenames:
                    if ".txt" in filename:
                        path = os.path.join(root, filename)
                        leaf_count, flower_count, fruit_count = process_txt_files(path)

                        d_leaf, d_flower, d_fruit = create_pred_dict(leaf_count, flower_count, fruit_count, filename)
                        
                        date_str, time_str = split_datetime(filename)
                        d_leaf['filename'] = filename
                        d_flower['filename'] = filename
                        d_fruit['filename'] = filename

                        d_leaf['timestamp'] = date_str
                        d_flower['timestamp'] = date_str
                        d_fruit['timestamp'] = date_str
                        
                        d_leaf['path'] = os.path.join(root, filename)
                        d_flower['path'] = os.path.join(root, filename)
                        d_fruit['path'] = os.path.join(root, filename)
                        results.append(d_leaf)
                        results.append(d_flower)
                        results.append(d_fruit)
        except:
            print("An error has occured when trying to coutn outputs.")

    return results

# def create_folders(timestamp):

def on_created(event):
    print("A file was created")
    # files, results = countOutput()
    # # Store to db
    # if(len(results) != 0):
    #     # store to db
    #     df = pd.DataFrame(results)
    #     df2 = pd.DataFrame(files)
    #     print(df.head())
    #     print(df2.head())
    #     print("length: ", len(results))
    
        # dont do anything and wait for the next event

def on_deleted(event):
    print("Deleted")

def on_modified(event):
    countOutput()
    print("modified")
    # Check all the folders in the directory


def on_moved(event):
    print("Moved")

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
        date_object = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    except:
        print("An error has occured when trying to parse dates. Check filename of outputs.")
    
    return date_object


if __name__ == "__main__":

#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
    path = "/home/student/Plant_Images"
    # print(getDatetime("IMG_20230307_1301.txt"))
    # Enter path to the outputs program
    df = countOutput()    
    # print(df["timestamp"].unique())
    # print(df.head())
    # create_folders(df["timestamp"].unique())
    # Always process path file
    # insert_predictions_data("pred_table_0", countOutput())

    event_handler = FileSystemEventHandler()
    

#     # event_handler.on_any_event = on_any_event
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved


    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        print("Monitoring.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Exited.")
    observer.join()

getDatetime("IMG_20230307_1301.txt")