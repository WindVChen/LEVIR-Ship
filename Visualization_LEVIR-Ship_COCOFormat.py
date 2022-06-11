from pycocotools.coco import COCO
import cv2
import os
import numpy as np

img_path = r'.\coco\images\train2017'
annFile = r'.\coco\annotations\instances_train2017.json'


def draw_rectangle(coordinates, image, image_name):
    for coordinate in coordinates:
        left = np.rint(coordinate[0])
        right = np.rint(coordinate[1])
        top = np.rint(coordinate[2])
        bottom = np.rint(coordinate[3])
        cv2.rectangle(image,
                      (int(left), int(right)),
                      (int(top), int(bottom)),
                      (0, 255, 0),
                      2)
        # cv2.putText(image, coordinate[4], (int(left), int(right)), cv2.FONT_HERSHEY_PLAIN, 2, color=(0,0,255), thickness=1)
    cv2.imshow("img", image)
    cv2.waitKey(0)

coco = COCO(annFile)

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())

# catIds_1 = coco.getCatIds(catNms=['ship'])
#
# imgIds_1 = coco.getImgIds(catIds=catIds_1)
imgIds_1 = coco.getImgIds(catIds=[])
img_list = os.listdir(img_path)
for i in range(len(img_list)):
    imgIds = imgIds_1[i]
    img = coco.loadImgs(imgIds)[0]
    image_name = img['file_name']
    print(img)

    annIds = coco.getAnnIds(imgIds=img['id'], catIds=[], iscrowd=None)
    anns = coco.loadAnns(annIds)

    coco.showAnns(anns)

    # print(anns)
    coordinates = []
    img_raw = cv2.imread(os.path.join(img_path, image_name))
    for j in range(len(anns)):
        coordinate = []
        coordinate.append(anns[j]['bbox'][0])
        coordinate.append(anns[j]['bbox'][1])
        coordinate.append(anns[j]['bbox'][0] + anns[j]['bbox'][2])
        coordinate.append(anns[j]['bbox'][1] + anns[j]['bbox'][3])
        coordinate.append(coco.loadCats(anns[j]['category_id'])[0]['name'])


        # print(coordinate)
        coordinates.append(coordinate)
    print(coordinates)
    draw_rectangle(coordinates, img_raw, image_name)