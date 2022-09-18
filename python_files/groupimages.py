# Attribution: https://youtu.be/p5rp_mkkXro
import os
from operator import itemgetter
import pandas as pd

EXTENSIONS = ['.png', '.jpg']
PATH_NAME = "/home/student/Test_Images"
# PATH_NAME = r"C:\Users\willi\Desktop\_Thesis\Test_images"

# Gets date value from the string
def get_date(date):
    return date[:4], date[4:6], date[6:8]

def get_time(time):
    time_str = time[:2] + ':' + time[2:4] + ':' + time[4:6]
    return time_str 

# Procedure for parsing filenames
def image_datetime(filename):
    # Example filename: "IMG_IMG_20211218_100625.jpg"
    date = filename.split("_")[1]
    time = filename.split("_")[2].split(".")[0] # split time and file extension
    return date, time

# Finding files with specified extensions
def get_files_list(root_dir, E):
    file_list, file_list_parsed, timestamps = [], [], []

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            print(filename)
            #If png is in filename
            if any(ext in filename for ext in E):
                file_list.append(os.path.join(root, filename))
                img_date, img_time = image_datetime(filename)
                file_list_parsed.append((img_date, img_time))
                d = {}
                d['Year'], d['Month'], d['Day'] = get_date(img_date)
                d['Time'] = get_time(img_time)
                timestamps.append(dict(d))

    return file_list, file_list_parsed, timestamps

# Main function
my_images, my_images_parsed, timestamps = get_files_list(PATH_NAME, EXTENSIONS)

my_images_parsed = sorted(my_images_parsed, key=itemgetter(0,1)) # sort by date then time
print(my_images_parsed, len(my_images_parsed))
print(pd.DataFrame(timestamps))