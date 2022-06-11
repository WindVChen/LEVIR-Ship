import warnings
import skimage
from skimage import io
import os
from glob import glob
from tqdm import tqdm
import numpy as np
import cv2
from numba import jit
import concurrent.futures

warnings.filterwarnings('ignore')

# @jit(nopython=True)
def customBlur(imgFile):
    size = 512
    targetPath = r'.\train\degrade'  # save path
    labelFile = imgFile.replace('png', 'txt').replace('images', 'labels')
    if os.path.exists(labelFile):
        img = io.imread(imgFile)
        label = np.loadtxt(labelFile, ndmin=2)
        dst = img.copy()
        centers = label.copy()
        for j in range(len(centers)):
            centers[j, 1] = label[j, 1] * size
            centers[j, 2] = label[j, 2] * size
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                minDis = 130 * 130
                for center in centers:
                    distance = (i - center[2]) ** 2 + (j - center[1]) ** 2
                    if distance < minDis:
                        minDis = distance
                # boxSize = (int(0.05* (minDis ** 0.5))) // 2 + 1
                boxSize = (int(1.03** (minDis ** 0.5))) // 2  # You can change the degradation configuration here
                # boxSize = int(((minDis**0.5)/5+1))//2
                dst[i, j,0] = img[max(i - boxSize, 0):min(i + boxSize + 1, size), max(j - boxSize, 0):min(j + boxSize + 1, size),0].mean()
                dst[i, j, 1] = img[max(i - boxSize, 0):min(i + boxSize + 1, size),
                               max(j - boxSize, 0):min(j + boxSize + 1, size), 1].mean()
                dst[i, j, 2] = img[max(i - boxSize, 0):min(i + boxSize + 1, size),
                               max(j - boxSize, 0):min(j + boxSize + 1, size), 2].mean()
        io.imsave(os.path.join(targetPath, os.path.basename(imgFile)), dst)
    else:
        img = cv2.imread(imgFile)
        dst = cv2.blur(img, (20, 20))
        cv2.imwrite(os.path.join(targetPath, os.path.basename(imgFile)), dst)

if __name__=='__main__':
    sourcePath = r'.\train\images'  # source path
    with concurrent.futures.ProcessPoolExecutor(1) as executor:  # set 1 to other number for speedup
        imgfiles=glob(os.path.join(sourcePath, '*.png'))
        for i in tqdm(zip(imgfiles, executor.map(customBlur, imgfiles)),total=1):
            pass
