# import cv2
import numpy as np
from pathlib import Path
import os

pathlist = Path("./data/cars").glob('**/*.jpg')

def generatePositiveSamples():
    f = open("./data/cars/info.dat", "w")
    for path in pathlist:
        path_in_str = str(path)
        print(path_in_str)

def create_pos_n_neg():
    for file_type in ["./data/cars"]:
        print(file_type)
        for img in os.listdir(file_type):
            if file_type == "pos":
                line = file_type+"/"+img+" 1 0 0 50 50\n"
                with open("info.dat","a") as f:
                    f.write(line)
            elif file_type == "Negative":
                    line = file_type+"/"+img+"\n"
                    with open("bg.txt","a") as f:
                        f.write(line)

create_pos_n_neg()