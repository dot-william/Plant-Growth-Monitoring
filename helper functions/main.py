import cv2
from pathlib import Path
import os


# from datetime import date
from datetime import datetime
import shutil

import datetime
import time

from predict_yolo import predict_yolo


def main(input_path, processed_path, output_parent_dir):
  # get present date
  today = datetime.datetime.today()
  present_date = Path(today.strftime("%Y_%m_%d"))

  # make output path for predictions
  #output_path = os.path.join(output_parent_dir, present_date)
  os.makedirs(output_parent_dir / present_date, exist_ok=True) # make output folder


  # make output for processed images
  os.makedirs(processed_path / present_date, exist_ok=True)

  pred_path = "dataset/for inference/0121" # folder containing all images for inference"
  weights_dir = "yolov8m_tile.pt"


  predict_yolo(pred_path=str(input_path),
              label_save_path=str(output_parent_dir / present_date), 
              weight_dir=weights_dir)


  # move raw images  to processed
  for img in os.listdir(input_path):
    shutil.move(input_path/img, processed_path/present_date/img)

"""
HOW TO USE

Note: Make sure predict_yolo.py, stitch.py, tile.py, and main.py are in the same folder
 *input_path = path to where raw images will be stored
 *minute_interval = every what minute to check input_path and detect objects
"""


if __name__ == "__main__":
  # input and output directories
  input_path = Path("raw dataset")
  

  output_parent_dir = Path("outputs")
  os.makedirs(output_parent_dir, exist_ok=True) # make folder if it doesnt exist

  processed_path = Path("processed") # folder to store raw images after prediction
  os.makedirs(str(processed_path), exist_ok=True)

  #minute_interval = [0, 8, 10, 15, 17, 20, 27, 34, 37, 40, 50]
  minute_interval = range(0,60,2)

  while True:
      current_time = datetime.datetime.now().time()
      
      if current_time.minute in minute_interval:
        print(f"[TIME {current_time.hour} : {current_time.minute}] Detecting objects...")
        main(input_path, processed_path, output_parent_dir)
        print("Detection done.")
        
          
          
      time.sleep(60) # sleeps for 60 seconds (1 minute) before checking the time again.
