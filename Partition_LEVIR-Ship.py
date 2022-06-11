import numpy as np
import glob
from tqdm import tqdm
from PIL import Image
import os
import random
import shutil

AllImagePath = r".\All_images"
AllLabelPath = r".\All_labels"
targetPath = r'.\save_path'
Size = 512
CLASSES = ['0']
ratio = [6, 2, 2]  # "train val test"

npRatio = np.array(ratio)
if not os.path.exists(os.path.join(targetPath, "train")):
    os.makedirs(os.path.join(targetPath, r"train\images"))
    os.makedirs(os.path.join(targetPath, r"train\labels"))

if not os.path.exists(os.path.join(targetPath, "val")):
    os.makedirs(os.path.join(targetPath, r"val\labels"))
    os.makedirs(os.path.join(targetPath, r"val\images"))

if not os.path.exists(os.path.join(targetPath, "test")):
    os.makedirs(os.path.join(targetPath, r"test\labels"))
    os.makedirs(os.path.join(targetPath, r"test\images"))

negList = []
posList = []
for i in glob.glob(AllLabelPath + r'\*.txt'):
    if os.path.getsize(i):
        posList.append(i)
    else:
        negList.append(i)

random.shuffle(posList)
random.shuffle(negList)

print("Total:", len(glob.glob(AllLabelPath + r'\*.txt')), "Pos:", len(posList), "Neg:", len(negList))

PtrainRatio = npRatio[0] * len(posList) // npRatio.sum()
PvalRatio = npRatio[1] * len(posList) // npRatio.sum()
PtestRatio = len(posList) - PtrainRatio - PvalRatio
print("Positive Ratio:", PtrainRatio, PvalRatio, PtestRatio)

NtrainRatio = npRatio[0] * len(negList) // npRatio.sum()
NvalRatio = npRatio[1] * len(negList) // npRatio.sum()
NtestRatio = len(negList) - NtrainRatio - NvalRatio
print("Negative Ratio:", NtrainRatio, NvalRatio, NtestRatio)

print("Allocate Positive Data...")
for n, i in enumerate(posList):
    if n < PtrainRatio:
        shutil.copy(i, os.path.join(targetPath, "train/labels", os.path.basename(i)))
        shutil.copy(os.path.join(AllImagePath, os.path.basename(i).replace("txt", "png")),
                    os.path.join(targetPath, "train/images", os.path.basename(i)).replace("txt", "png"))
    elif n >= PtrainRatio and n < PtrainRatio + PvalRatio:
        shutil.copy(i, os.path.join(targetPath, "val/labels", os.path.basename(i)))
        shutil.copy(os.path.join(AllImagePath, os.path.basename(i).replace("txt", "png")),
                    os.path.join(targetPath, "val/images", os.path.basename(i)).replace("txt", "png"))
    else:
        shutil.copy(i, os.path.join(targetPath, "test/labels", os.path.basename(i)))
        shutil.copy(os.path.join(AllImagePath, os.path.basename(i).replace("txt", "png")),
                    os.path.join(targetPath, "test/images", os.path.basename(i)).replace("txt", "png"))

print("Allocate Negative Data...")
for n, i in enumerate(negList):
    if n < NtrainRatio:
        shutil.copy(i, os.path.join(targetPath, "train/labels", os.path.basename(i)))
        shutil.copy(os.path.join(AllImagePath, os.path.basename(i).replace("txt", "png")),
                    os.path.join(targetPath, "train/images", os.path.basename(i)).replace("txt", "png"))
    elif n >= NtrainRatio and n < NtrainRatio + NvalRatio:
        shutil.copy(i, os.path.join(targetPath, "val/labels", os.path.basename(i)))
        shutil.copy(os.path.join(AllImagePath, os.path.basename(i).replace("txt", "png")),
                    os.path.join(targetPath, "val/images", os.path.basename(i)).replace("txt", "png"))
    else:
        shutil.copy(i, os.path.join(targetPath, "test/labels", os.path.basename(i)))
        shutil.copy(os.path.join(AllImagePath, os.path.basename(i).replace("txt", "png")),
                    os.path.join(targetPath, "test/images", os.path.basename(i)).replace("txt", "png"))
