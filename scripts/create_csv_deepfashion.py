import os
import sys
import random
import numpy as np
import keras
from numpy import array

import sys
sys.path.append("..")


print('----------------------------------------')
print('start')

# Root directory of the project
ROOT_DIR = os.getcwd()

# Root directory of the project
DIR_ROOT = os.getcwd()
DIR_DEEPFASHION = "dataset/deepfashion"
DIR_ROOT_DEEPFASHION = os.path.join(DIR_ROOT, DIR_DEEPFASHION)
DIR_ROOT_DEEPFASHION_IMAGE = os.path.join(DIR_ROOT, DIR_DEEPFASHION, "images")
DIR_DEEPFASHION_IMAGE = "images"
FILE_TRAIN_CSV = os.path.join(DIR_DEEPFASHION, "instances_train2017.csv")
FILE_VAL_CSV = os.path.join(DIR_DEEPFASHION, "instances_val2017.csv")
FILE_CATEGORIES_CSV = os.path.join(DIR_DEEPFASHION, "categories2017.csv")

if not os.path.exists(os.path.join(DIR_DEEPFASHION, DIR_DEEPFASHION_IMAGE)):
    os.makedirs(os.path.join(DIR_DEEPFASHION, DIR_DEEPFASHION_IMAGE))
    
    
START_CATEGORY_ID = 0


# path 설정
path_list_category_cloth = os.path.join(DIR_DEEPFASHION, "Anno", "list_category_cloth.txt");

# create category object
categories = []
categories_dic = {}
with open(path_list_category_cloth) as file_list_category_cloth:
    # 첫번째, 두번째 줄은 데이타의 정보를 나타내므로 skip 처리.
    next(file_list_category_cloth)
    next(file_list_category_cloth)
    for index, line in enumerate(file_list_category_cloth):
        name = line.strip()[:-1].strip()
        id = index+1+START_CATEGORY_ID
        categories.append([name, id])
        categories_dic[id] = name

dataset_classes = np.asarray(categories)


from PIL import Image
import shutil
from shutil import copyfile

# path 설정
path_list_bbox = os.path.join(DIR_DEEPFASHION, "Anno", "list_bbox.txt");
path_list_category_img = os.path.join(DIR_DEEPFASHION, "Anno", "list_category_img.txt"); 

# create annotations object
dataset_annotations = []
print('start parsing ~')

# 'img/Sheer_Pleated-Front_Blouse/img_00000001.jpg' '072' '079' '232' '273' 'Blouse'

with open(path_list_bbox) as file_path_list_bbox:
    with open(path_list_category_img) as file_path_list_category_img:
        # 첫번째, 두번째 줄은 데이타의 정보를 나타내므로 skip 처리.
        next(file_path_list_bbox)
        next(file_path_list_bbox)
        next(file_path_list_category_img)
        next(file_path_list_category_img)        
        print('skip 2 line (data num, data type)')
        for index, (line_bbox, line_image) in enumerate(zip(file_path_list_bbox, file_path_list_category_img)):
            # each rows
            line_image = line_image.split()
            line_bbox = line_bbox.split()
            image_path = os.path.join(DIR_DEEPFASHION, line_image[0])
            
            image_format = line_image[0].split('/')[-1].split('.')[1]
            image_name = str(index+100000000000+1).zfill(12)+'.'+image_format
            new_global_image_path = os.path.join(DIR_ROOT_DEEPFASHION_IMAGE, image_name)
            new_local_image_path = os.path.join(DIR_DEEPFASHION_IMAGE, image_name)
            
            category_id = int(line_image[1])+START_CATEGORY_ID
            
            # 이미지 파일 유무 확인
            #if not os.path.exists(image_path):
            #    continue
            
            # image경로를 통하여 같은 데이타인지 확인
            if line_image[0] != line_bbox[0]:
                print('error image path')
                continue
                
            # get image size        
            image_size = Image.open(image_path).size
            if image_size[0]==0 or image_size[1]==0:
                print('error image size')
                continue
            
            # coco dataset과 동일한 local 경로로 파일 이동 또는 복사한다
            # move file
            # shutil.move(image_path, new_global_image_path)
            # copy file
            if not os.path.exists(new_global_image_path):
                copyfile(image_path, new_global_image_path)
                
            dataset_annotations.append([new_local_image_path, line_bbox[1], line_bbox[2], line_bbox[3], line_bbox[4], categories_dic[int(category_id)]])
            
print('end parsing ~')


dataset_annotations = np.asarray(dataset_annotations)

print('class 개수 - ',len(dataset_classes))
print('image 개수 - ',len(dataset_annotations))



np.random.shuffle(dataset_annotations)

# 80%는 train set으로 20%는 test set으로 분류
threshold = int(dataset_annotations.shape[0] * 0.8)
train_annotations = dataset_annotations[:threshold,]
test_annotations = dataset_annotations[threshold:,]

print("train 개수 - ", train_annotations.shape[0])
print("test 개수 - ", test_annotations.shape[0])

print("train 샘플 - ", train_annotations[0][5])
print("test 샘플 - ", test_annotations[0][5])


np.savetxt(FILE_TRAIN_CSV, train_annotations, delimiter=",", fmt="%s") 
print('saved instances_train2017.csv')
np.savetxt(FILE_VAL_CSV, test_annotations, delimiter=",", fmt="%s") 
print('saved instances_val2017.csv')
np.savetxt(FILE_CATEGORIES_CSV, dataset_classes, delimiter=",", fmt="%s")
print('saved categories2017.csv')

print('----------------------------------------')
print('done')
