# Attribution: https://youtu.be/p5rp_mkkXro
import os
import shutil
import pandas as pd

EXTENSIONS = ['.png', '.jpg']

# Change path based on machine
PATH_NAME = "/home/student/Test_Images"
DEST_PATH = '/home/student/Images'
# DEST_PATH = r'C:\Users\willi\Desktop\_Thesis\Test_images_2'
# PATH_NAME = r"C:\Users\willi\Desktop\_Thesis\Test_images"
NUM_PLANTS = 9

# This function gets date value from the string
def get_date(date):
    return date[:4], date[4:6], date[6:8]

# this function gets the time from the string
def get_time(time):
    time_str = time[:2] + ':' + time[2:4] + ':' + time[4:6]
    return time_str 

# This function parses the filename to get the date and time
def image_datetime(filename):
    # Example filename: "IMG_IMG_20211218_100625.jpg"
    date = filename.split("_")[1]
    time = filename.split("_")[2].split(".")[0] # split time and file extension
    return date, time

# Finding files with specified extensions
def get_images(root_dir, E):
    img_files = []

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            print(filename)
            #If png is in filename
            if any(ext in filename for ext in E):
                img_date, img_time = image_datetime(filename)
                d = {}
                d['Year'], d['Month'], d['Day'] = get_date(img_date)
                d['Timestamp'] = img_date
                d['Filename'] = filename
                d['Time'] = get_time(img_time)
                d['Path'] = os.path.join(root, filename)
                img_files.append(dict(d))

    return img_files

# Create folders via date (use pandas' unique function when passing)
def create_folders_date(timestamps):
    if len(timestamps) > 0:
        if not os.path.isdir(DEST_PATH):
            os.mkdir(DEST_PATH)
            print("Directory created.")
        for timestamp in timestamps:
            os.mkdir(f'{DEST_PATH}{timestamp}')

# This function creates 9 folders based on the requirements
def create_folders_plants():
    # If directory does not exist yet
    if not os.path.isdir(DEST_PATH):
        os.mkdir(DEST_PATH)
        print("Destination created")

    directory = os.listdir(DEST_PATH)

    # If there are no folders yet
    if len(directory) == 0:
        for i in range(NUM_PLANTS):
            folder_name = "Plant" + "_" + str(i+1)
            path = os.path.join(DEST_PATH, folder_name)
            os.mkdir(path)
        print("Folders created")
    

# This function moves the images to its designated folder
def move_images(data, len_data):
    idx = 0
    for i, (source, filename, this_folder) in enumerate(zip(data['Path'], data['Filename'], data['Timestamp'])):
        idx += 1
        dest_folder = "Plant" + "_" + str(idx)
        destination = os.path.join(DEST_PATH, dest_folder)
        print(f'|{i} Moving image {source} to folder {destination}')
        shutil.move(source, destination)
        if ((i+1) % 9) == 0:
            idx = 0


# Main function
if __name__ == '__main__':
    data = get_images(PATH_NAME, EXTENSIONS)
    img_data = pd.DataFrame(data)
    # If there are images
    if img_data.shape[0] != 0:
        img_data.sort_values(['Timestamp', 'Time'])
        create_folders_plants()
        print(img_data)
        len_img = img_data.shape[0]
        if len_img % 9 == 0:
            move_images(img_data, len_img)
        else:
            print("Moving of image cannot be done yet. Since num of images aren't divisible by 9")
    else:
        print("No images can be moved yet")
    

