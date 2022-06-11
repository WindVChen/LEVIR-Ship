import json
import numpy as np
from glob import glob
import cv2
import os

classname_to_id = {"ship": 1}  # 0 is background


class Yolo2CoCo:
    def __init__(self, image_dir, total_annos):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
        self.image_dir = image_dir
        self.total_annos = total_annos

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w'), ensure_ascii=False, indent=2)

    def to_coco(self, keys):
        self._init_categories()
        for key in keys:
            self.images.append(self._image(key))
            shapes = self.total_annos[key]
            for shape in shapes:
                bboxi = []
                for cor in shape[:-1]:
                    bboxi.append(int(cor))
                label = shape[-1]
                annotation = self._annotation(bboxi, label)
                self.annotations.append(annotation)
                self.ann_id += 1
            self.img_id += 1
        instance = {}
        instance['info'] = 'spytensor created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)

    def _image(self, path):
        image = {}
        # print(path)
        img = cv2.imread(self.image_dir + path)
        image['height'] = img.shape[0]
        image['width'] = img.shape[1]
        image['id'] = self.img_id
        image['file_name'] = path
        return image

    def _annotation(self, shape, label):
        # label = shape[-1]
        points = shape[:4]
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = int(label)
        annotation['segmentation'] = self._get_seg(points)
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = self._get_area(points)
        return annotation

    # COCO format： [x1,y1,w,h]
    def _get_box(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return [min_x, min_y, max_x - min_x, max_y - min_y]

    #  cal area
    def _get_area(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return (max_x - min_x + 1) * (max_y - min_y + 1)

    # segmentation
    def _get_seg(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        h = max_y - min_y
        w = max_x - min_x
        a = []
        a.append([min_x, min_y, min_x, min_y + 0.5 * h, min_x, max_y, min_x + 0.5 * w, max_y, max_x, max_y, max_x,
                  max_y - 0.5 * h, max_x, min_y, max_x - 0.5 * w, min_y])
        return a


if __name__ == '__main__':
    datasetPath = r'D:\TempComputerProgram\ForDRENet\finalDataSet\yolo'  # Levir-Ship Yolo-format dataset path
    saved_coco_path = "./"

    total_yolo_annotations, train_keys, val_keys, test_keys = {}, [], [], []
    "Train"
    for i in glob(datasetPath + "/train/labels/*.txt"):
        key = os.path.basename(i).replace("txt", "png")
        value = np.loadtxt(i, ndmin=2)
        for n, i in enumerate(value):
            i[0] = 1
            i[1] = (i[1] - i[3] / 2) * 512
            i[2] = (i[2] - i[4] / 2) * 512
            i[3] = i[1] + i[3] * 512
            i[4] = i[2] + i[4] * 512
            temp = i[0]
            i[0] = i[1]
            i[1] = i[2]
            i[2] = i[3]
            i[3] = i[4]
            i[4] = temp
            value[n] = i
        train_keys.append(key)
        total_yolo_annotations[key] = value

    "Val"
    for i in glob(datasetPath + "/val/labels/*.txt"):
        key = os.path.basename(i).replace("txt", "png")
        value = np.loadtxt(i, ndmin=2)
        for n, i in enumerate(value):
            i[0] = 1
            i[1] = (i[1] - i[3] / 2) * 512
            i[2] = (i[2] - i[4] / 2) * 512
            i[3] = i[1] + i[3] * 512
            i[4] = i[2] + i[4] * 512
            temp = i[0]
            i[0] = i[1]
            i[1] = i[2]
            i[2] = i[3]
            i[3] = i[4]
            i[4] = temp
            value[n] = i
        val_keys.append(key)
        total_yolo_annotations[key] = value

    "Test"
    for i in glob(datasetPath + "/test/labels/*.txt"):
        key = os.path.basename(i).replace("txt", "png")
        value = np.loadtxt(i, ndmin=2)
        for n, i in enumerate(value):
            i[0] = 1
            i[1] = (i[1] - i[3] / 2) * 512
            i[2] = (i[2] - i[4] / 2) * 512
            i[3] = i[1] + i[3] * 512
            i[4] = i[2] + i[4] * 512
            temp = i[0]
            i[0] = i[1]
            i[1] = i[2]
            i[2] = i[3]
            i[3] = i[4]
            i[4] = temp
            value[n] = i
        test_keys.append(key)
        total_yolo_annotations[key] = value

    print("train_n:", len(train_keys), 'val_n:', len(val_keys), 'test_n:', len(test_keys))

    if not os.path.exists('%scoco/annotations/' % saved_coco_path):
        os.makedirs('%scoco/annotations/' % saved_coco_path)

    "Transform Train Dataset"
    l2c_train = Yolo2CoCo(image_dir=os.path.join(datasetPath, "train/images/"), total_annos=total_yolo_annotations)
    train_instance = l2c_train.to_coco(train_keys)
    l2c_train.save_coco_json(train_instance, '%scoco/annotations/instances_train2017.json' % saved_coco_path)

    "Transform Val Dataset"
    l2c_val = Yolo2CoCo(image_dir=os.path.join(datasetPath, "val/images/"), total_annos=total_yolo_annotations)
    val_instance = l2c_val.to_coco(val_keys)
    l2c_val.save_coco_json(val_instance, '%scoco/annotations/instances_val2017.json' % saved_coco_path)

    "Transform Test Dataset"
    l2c_test = Yolo2CoCo(image_dir=os.path.join(datasetPath, "test/images/"), total_annos=total_yolo_annotations)
    test_instance = l2c_test.to_coco(test_keys)
    l2c_test.save_coco_json(test_instance, '%scoco/annotations/instances_test2017.json' % saved_coco_path)
