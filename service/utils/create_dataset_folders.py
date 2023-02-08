import pathlib
import re
import os
import shutil

data_dir = pathlib.Path("../data/cars")

for image in list(data_dir.glob('*.jpg')):
    x = re.search("\_20[0-9]{2}.*", str(image))
    if x is None:
        x = re.split("\_19[0-9]{2}.*", str(image))
    else:
        x = re.split("\_20[0-9]{2}.*", str(image))
    x = re.split("data\\\\cars\\\\", str(x[0]))
    if os.path.exists("../data/cars/"+ str(x[1])):
        new_directory = os.path.join("../data/cars/", x[1])
        x = re.split("data\\\\cars\\\\", str(image))
        shutil.move(image, new_directory + "/" + x[1])
    else:
        new_directory = os.path.join("../data/cars/", x[1])
        os.mkdir(new_directory)
        x = re.split("data\\\\cars\\\\", str(image))
        shutil.move(image, new_directory + "/" + x[1])