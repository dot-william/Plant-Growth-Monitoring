import cv2
import shutil
import os

from pathlib import Path

from tile import tile_img
from stitch import stitch_labels


def predict_yolo(pred_path:str,  # folder containing all images for inference")
                 label_save_path:str, # folder to save the label txts stitched
                 weight_dir:str, # path to pre-trained model weights
                 save_tiles_path:str="tiled", # temporary folder to store tiled images 
                 conf:float=0.25, # conf threshold of model
                 save_txt:bool=True):
  
  pred_path = Path(pred_path)
  label_save_path = Path(label_save_path)


  pred_imgs = list(pred_path.glob("*.jpg")) # get all images path in pred_path

  

  for img_path in pred_imgs:
    img = cv2.imread(str(img_path))
    HEIGHT, WIDTH = img.shape[:2]

    tile_img(img=img,
            save_path=save_tiles_path)
    
    cmd = f'yolo task=detect mode=predict model={weight_dir} conf=0.25 source={save_tiles_path} save_txt={save_txt} exist_ok=True #hide_labels=True'
    os.system(cmd) # execute command

    if not label_save_path.exists():
      os.makedirs(label_save_path, exist_ok=True)

    master_df = stitch_labels("runs/detect/predict/labels",
                  HEIGHT = HEIGHT,
                  WIDTH=WIDTH)

    master_df.to_csv(str(label_save_path / img_path.name[:-4])+".txt", sep=" ", header=None, index=False) # save stitched labels 

    shutil.rmtree("runs")
