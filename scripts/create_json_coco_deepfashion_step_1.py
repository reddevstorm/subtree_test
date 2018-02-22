import os
import json
import shutil

import sys
sys.path.append("..")

DIR_ROOT = os.getcwd()
DIR_DEEP = os.path.join(DIR_ROOT, "dataset/deepfashion")
DIR_COCO = os.path.join(DIR_ROOT, "dataset/coco")
DIR_ALL = os.path.join(DIR_ROOT, "dataset/all")

# Deepfashion dataset
FILE_DEEPFASHION_TRAIN_JSON = os.path.join(DIR_ROOT, DIR_DEEP, "annotations", "instances_train2017.json")
FILE_DEEPFASHION_VAL_JSON = os.path.join(DIR_ROOT, DIR_DEEP, "annotations", "instances_val2017.json")
DIR_ROOT_DEEPFASHION_IMAGES = os.path.join(DIR_ROOT, DIR_DEEP, "images")

# COCO dataset
FILE_COCO_TRAIN_JSON = os.path.join(DIR_ROOT, DIR_COCO, "annotations", "instances_train2017.json")
FILE_COCO_VAL_JSON = os.path.join(DIR_ROOT, DIR_COCO, "annotations", "instances_val2017.json")
DIR_ROOT_COCO_IMAGES_TRAIN2017 = os.path.join(DIR_ROOT, DIR_COCO, "images/train2017")
DIR_ROOT_COCO_IMAGES_VAL2017 = os.path.join(DIR_ROOT, DIR_COCO, "images/val2017")

# new dataset
DIR_ALL_ANNOTATIONS = os.path.join(DIR_ALL, "annotations")
DIR_ALL_IMAGES_TRAIN2017 = os.path.join(DIR_ALL, "images/train2017")
DIR_ALL_IMAGES_VAL2017 = os.path.join(DIR_ALL, "images/val2017")
FILE_ALL_TRAIN_JSON = os.path.join(DIR_ALL_ANNOTATIONS, "instances_train2017.json")
FILE_ALL_VAL_JSON = os.path.join(DIR_ALL_ANNOTATIONS, "instances_val2017.json")
FILE_DEEP_TRAIN_JSON = os.path.join(DIR_ALL_ANNOTATIONS, "deep_train2017.json")
FILE_DEEP_VAL_JSON = os.path.join(DIR_ALL_ANNOTATIONS, "deep_val2017.json")

if not os.path.exists(DIR_ALL_ANNOTATIONS):
    os.makedirs(DIR_ALL_ANNOTATIONS)
    
if not os.path.exists(DIR_ALL_IMAGES_TRAIN2017):
    os.makedirs(DIR_ALL_IMAGES_TRAIN2017)

if not os.path.exists(DIR_ALL_IMAGES_VAL2017):
    os.makedirs(DIR_ALL_IMAGES_VAL2017)


coco_train = json.load(open(FILE_COCO_TRAIN_JSON))
coco_val = json.load(open(FILE_COCO_VAL_JSON))
deep_train = json.load(open(FILE_DEEPFASHION_TRAIN_JSON))
deep_val = json.load(open(FILE_DEEPFASHION_VAL_JSON))


import random

coco_train_anno = coco_train['annotations']
deep_train_anno = deep_train['annotations']
all_train_anno = coco_train_anno+deep_train_anno

coco_val_anno = coco_val['annotations']
deep_val_anno = deep_val['annotations']
all_val_anno = coco_val_anno+deep_val_anno

coco_train_img = coco_train['images']
deep_train_img = deep_train['images']
all_train_img = coco_train_img+deep_train_img

# random.shuffle(all_train_img)

coco_val_img = coco_val['images']
deep_val_img = deep_val['images']
all_val_img = coco_val_img+deep_val_img

# random.shuffle(all_val_img)

coco_cate = coco_train['categories']
deep_cate = deep_train['categories']
all_cate = coco_cate+deep_cate

all_info = coco_train['info']
all_licenses = coco_train['licenses']


print('start - make json file')
train_data = {}
train_data['annotations'] = all_train_anno
train_data['categories'] = all_cate
train_data['images'] = all_train_img
with open(FILE_ALL_TRAIN_JSON, 'w') as outfile:
    json.dump(train_data, outfile)
    
    
val_data = {}
val_data['annotations'] = all_val_anno
val_data['categories'] = all_cate
val_data['images'] = all_val_img
with open(FILE_ALL_VAL_JSON, 'w') as outfile:
    json.dump(val_data, outfile)


deep_train_data = {}
deep_train_data['annotations'] = deep_train_anno
deep_train_data['categories'] = all_cate
deep_train_data['images'] = deep_train_img
with open(FILE_DEEP_TRAIN_JSON, 'w') as outfile:
    json.dump(deep_train_data, outfile)
    
deep_val_data = {}
deep_val_data['annotations'] = deep_val_anno
deep_val_data['categories'] = all_cate
deep_val_data['images'] = deep_val_img
with open(FILE_DEEP_VAL_JSON, 'w') as outfile:
    json.dump(deep_val_data, outfile)
    
print('end - make json file')



import shutil
from shutil import copyfile

for img_data in coco_train_img:
    img_name = img_data['file_name']
    img_path = os.path.join(DIR_ROOT_COCO_IMAGES_TRAIN2017, img_name)
    new_img_path = os.path.join(DIR_ALL_IMAGES_TRAIN2017, img_name)
    if not os.path.exists(new_img_path):
        if not os.path.exists(img_path):
            print("not found", img_path)
        else:
            copyfile(img_path, new_img_path)
#     if os.path.exists(img_path):
#         shutil.move(img_path, new_img_path)
        
print("Completed - COCO_IMAGES_TRAIN2017")    

for img_data in coco_val_img:
    img_name = img_data['file_name']
    img_path = os.path.join(DIR_ROOT_COCO_IMAGES_VAL2017, img_name)
    new_img_path = os.path.join(DIR_ALL_IMAGES_VAL2017, img_name)
#     if os.path.exists(img_path):
#         shutil.move(img_path, new_img_path)
    if not os.path.exists(new_img_path):
        if not os.path.exists(img_path):
            print("not found", img_path)
        else:
            copyfile(img_path, new_img_path)
            
print("Completed - COCO_IMAGES_VAL2017")    
        
for img_data in deep_train_img:
    img_name = img_data['file_name']
    img_path = os.path.join(DIR_ROOT_DEEPFASHION_IMAGES, img_name)
    new_img_path = os.path.join(DIR_ALL_IMAGES_TRAIN2017, img_name)
#     if os.path.exists(img_path):
#         shutil.move(img_path, new_img_path)
    if not os.path.exists(new_img_path):
        if not os.path.exists(img_path):
            print("not found", img_path)
        else:
            copyfile(img_path, new_img_path)
            
print("Completed - DEEPFASHION_IMAGES_TRAIN2017")    
        
for img_data in deep_val_img:
    img_name = img_data['file_name']
    img_path = os.path.join(DIR_ROOT_DEEPFASHION_IMAGES, img_name)
    new_img_path = os.path.join(DIR_ALL_IMAGES_VAL2017, img_name)
#     if os.path.exists(img_path):
#         shutil.move(img_path, new_img_path)
    if not os.path.exists(new_img_path):
        if not os.path.exists(img_path):
            print("not found", img_path)
        else:
            copyfile(img_path, new_img_path)
            
print("Completed - DEEPFASHION_IMAGES_VAL2017")    