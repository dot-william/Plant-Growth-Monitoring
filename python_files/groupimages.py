import os

EXTENSIONS = ['.png']
PATH_NAME = "/home/student/Test_Images"

def get_files_list(root_dir, E):
    file_list = []

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(ext in filename for ext in E):
                file_list.append(os.path.join(root, filename))
    return file_list

my_images = get_files_list(PATH_NAME, EXTENSIONS)

print(my_images, len(my_images))