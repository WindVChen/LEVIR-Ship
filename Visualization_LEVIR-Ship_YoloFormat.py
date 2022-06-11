from glob import glob
import cv2
import os
import numpy as np

inputpath = r'.\yolo\train\images'
imgs = glob(inputpath + '/*.png')
for n, i in enumerate(imgs):
    img = cv2.imread(i)
    H, W = img.shape[:2]
    if os.path.exists(i.replace('images', 'labels').replace('png', 'txt')):
        labels = np.loadtxt(i.replace('images', 'labels').replace('png', 'txt'), ndmin=2)
        for j in labels:
            pt1 = (int((j[1] - j[3] / 2) * W), int((j[2] - j[4] / 2) * H))
            pt2 = (int((j[1] + j[3] / 2) * W), int((j[2] + j[4] / 2) * H))
            cv2.rectangle(img, pt2, pt1, (255, 0, 0))
    cv2.putText(img, str(n), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    cv2.imshow("img", img)
    print(i)
    cv2.waitKey(0)
