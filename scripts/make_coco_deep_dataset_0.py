import os

# Root directory of the project
DIR_ROOT = os.getcwd()
DIR_DEEPFASHION = "dataset/deepfashion"
DIR_ROOT_DEEPFASHION = os.path.join(DIR_ROOT, DIR_DEEPFASHION)
DIR_ROOT_DEEPFASHION_IMAGE = os.path.join(DIR_ROOT, DIR_DEEPFASHION, "images")
DIR_ROOT_DEEPFASHION_ANNOTATIONS = os.path.join(DIR_ROOT, DIR_DEEPFASHION, "annotations")
FILE_TRAIN_JSON = os.path.join(DIR_ROOT_DEEPFASHION_ANNOTATIONS, "instances_train2017.json")
FILE_VAL_JSON = os.path.join(DIR_ROOT_DEEPFASHION_ANNOTATIONS, "instances_val2017.json")

if not os.path.exists(DIR_ROOT_DEEPFASHION_IMAGE):
    os.makedirs(DIR_ROOT_DEEPFASHION_IMAGE)
    
if not os.path.exists(DIR_ROOT_DEEPFASHION_ANNOTATIONS):
    os.makedirs(DIR_ROOT_DEEPFASHION_ANNOTATIONS)
    
print(DIR_ROOT_DEEPFASHION_ANNOTATIONS)




DEEPFASHION_CATEGORY_START_ID = 100
DEEPFASHION_IMAGE_START_ID = 1000000000000
DEEPFASHION_ANNO_START_ID = 1000000000000




# path 설정
path_list_category_cloth = os.path.join(DIR_DEEPFASHION, "Anno", "list_category_cloth.txt");

# supercategory name 설정|
supercategory_names = ["upper-body","lower-body","full-body"]

# create category object
categories = []
with open(path_list_category_cloth) as file_list_category_cloth:
    # 첫번째, 두번째 줄은 데이타의 정보를 나타내므로 skip 처리.
    next(file_list_category_cloth)
    next(file_list_category_cloth)
    for index, line in enumerate(file_list_category_cloth):
        super_category_index = int(line.strip()[-1:].strip().replace(' ', '_'))-1
        category = {}
        category['id'] = DEEPFASHION_CATEGORY_START_ID+index+1
        category['name'] = line.strip()[:-1].strip().replace(' ', '_')
        category['supercategory'] = supercategory_names[super_category_index]
        categories.append(category)

print('categories sample [0] - ', categories[0])



from PIL import Image
import shutil
from shutil import copyfile

# path 설정
path_list_bbox = os.path.join(DIR_DEEPFASHION, "Anno", "list_bbox.txt");
path_list_category_img = os.path.join(DIR_DEEPFASHION, "Anno", "list_category_img.txt"); 

# create annotations object
annotations = []
images = []

print('start parsing')

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
            new_image_path = os.path.join(DIR_ROOT_DEEPFASHION_IMAGE, image_name)
            
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
            # shutil.move(image_path, new_image_path)
            # copy file
            if not os.path.exists(new_image_path):
                copyfile(image_path, new_image_path)
                
            
            # set ids
            annotation_id = DEEPFASHION_ANNO_START_ID+index+1
            #category_id = int(line_image[1:][0])
            category_id = DEEPFASHION_CATEGORY_START_ID+int(line_image[1:][0])
            image_id = DEEPFASHION_IMAGE_START_ID+index+1
            image_local_url = line_image[0]
            
            # bbox
            bbox_x1 = int(line_bbox[1])
            bbox_y1 = int(line_bbox[2])
            bbox_x2 = int(line_bbox[3])
            bbox_y2 = int(line_bbox[4])
            bbox_width = int(bbox_x2-bbox_x1)
            bbox_height = int(bbox_y2-bbox_y1)
            
            # set image object
            image = {}
            image['id'] = image_id
            image['width'] = image_size[0]
            image['height'] = image_size[1]
            image['file_name'] = image_name
            image['coco_url'] = image_path
            image['date_captured'] = ''
            image['flickr_url'] = ''
            image['license'] = 0
            
            # set annotation
            annotation = {}
            annotation['area'] = bbox_width*bbox_height
            annotation['bbox'] = [bbox_x1, bbox_y1, bbox_width, bbox_height]
            annotation['category_id'] = category_id
            annotation['id'] = annotation_id
            annotation['image_id'] = image_id
            annotation['iscrowd'] = 0
            annotation['segmentation'] = []
            
            # add image, annotation
            annotations.append(annotation);
            images.append(image);
            
print('end parsing')

print('sample - annotations[0] : ', annotations[0])
print('sample - image[0] : ', images[0])



import random

# random shuffle
zip_data = list(zip(annotations, images))
random.shuffle(zip_data)
annotations, images = zip(*zip_data)


# create train, val dataset
total = len(annotations)
train_total = int(total*0.9) 

# train dataset
train_annotations = annotations[:train_total]
train_images = images[:train_total]

# val dataset
val_annotations = annotations[train_total:]
val_images = images[train_total:]

print('train dataset - ', len(train_annotations))
print('val dataset - ', len(val_annotations))
if train_annotations[0]['image_id'] != train_images[0]['id']:
    print('suffle error')

if val_annotations[0]['image_id'] != val_images[0]['id']:
    print('suffle error')


import json

print('start - make json file')
train_data = {}
train_data['annotations'] = train_annotations
train_data['categories'] = categories
train_data['images'] = train_images
with open(FILE_TRAIN_JSON, 'w') as outfile:
    json.dump(train_data, outfile)
    
    
val_data = {}
val_data['annotations'] = val_annotations
val_data['categories'] = categories
val_data['images'] = val_images
with open(FILE_VAL_JSON, 'w') as outfile:
    json.dump(val_data, outfile)
    
print('end - make json file')


print(train_data['annotations'][0])
print(train_data['categories'][0])
print(train_data['images'][0])