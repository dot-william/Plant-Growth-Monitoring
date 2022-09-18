import os
from operator import itemgetter
EXTENSIONS = ['.png', '.jpg']
PATH_NAME = "/home/student/Test_Images"
# PATH_NAME = r"C:\Users\willi\Desktop\_Thesis\Test_images"
# Procedure for parsing filenames
def image_timestamp(filename):
    # Example filename: "IMG_IMG_20211218_100625.jpg"

    date = filename.split("_")[1]
    time = filename.split("_")[2].split(".")[0] # split time and file extension
    return date, time

# Finding files with specified extensions
def get_files_list(root_dir, E):
    file_list, file_list_parsed = [], []

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            print(filename)
            #If png is in filename
            if any(ext in filename for ext in E):
                
                file_list.append(os.path.join(root, filename))
                file_list_parsed.append(image_timestamp(filename))

    return file_list, file_list_parsed

my_images, my_images_parsed = get_files_list(PATH_NAME, EXTENSIONS)
sorted(my_images_parsed, key=itemgetter(0,1)) # sort to be sure that the images are in chronological order
print(my_images_parsed, len(my_images_parsed))
