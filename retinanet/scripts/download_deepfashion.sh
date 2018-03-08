#!/bin/bash

# http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html

mkdir -p dataset/deepfashion/Anno
mkdir -p dataset/deepfashion/Eval
mkdir -p dataset/deepfashion/img

# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AABpzYsttt7DIQmb2PckgbPXa/Anno/list_attr_cloth.txt?dl=0 -O dataset/deepfashion/Anno/list_attr_cloth.txt
# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AADYszB-Pv6mgwtiPEtQkHTva/Anno/list_attr_img.txt?dl=0 -O dataset/deepfashion/Anno/list_attr_img.txt
# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AADr1hf3nsOZEV3sOTZ1-m98a/Anno/list_bbox.txt?dl=0 -O dataset/deepfashion/Anno/list_bbox.txt
# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AACiFqyjpb21GyVwLNBATFQXa/Anno/list_category_cloth.txt?dl=0 -O dataset/deepfashion/Anno/list_category_cloth.txt
# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AAD3Mm6b2e9vkVdb35OfCA3fa/Anno/list_category_img.txt?dl=0 -O dataset/deepfashion/Anno/list_category_img.txt
# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AAARD4rdUT8oBQsjl4HuYAXha/Anno/list_landmarks.txt?dl=0 -O dataset/deepfashion/Anno/list_landmarks.txt

# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AACTJyCl9bprY90Z3frUZ-H-a/Eval/list_eval_partition.txt?dl=0 -O dataset/deepfashion/Eval/list_eval_partition.txt

# wget https://www.dropbox.com/sh/ryl8efwispnjw21/AABKePZxbIrUHD0RjFLGA9q1a/README.txt?dl=0 -O dataset/deepfashion/README.txt

# wget -c https://www.dropbox.com/sh/ryl8efwispnjw21/AACpZU-UKs_snxFH5Bp8RwOwa/Img/img.zip?dl=0 -O dataset/deepfashion/img.zip


wget https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/list_attr_cloth.txt -O dataset/deepfashion/Anno/list_attr_cloth.txt
wget https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/list_attr_img.txt -O dataset/deepfashion/Anno/list_attr_img.txt
wget https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/list_bbox.txt -O dataset/deepfashion/Anno/list_bbox.txt
wget https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/list_category_cloth.txt -O dataset/deepfashion/Anno/list_category_cloth.txt
wget https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/list_category_img.txt -O dataset/deepfashion/Anno/list_category_img.txt
wget https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/list_landmarks.txt -O dataset/deepfashion/Anno/list_landmarks.txt
wget https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/list_eval_partition.txt -O dataset/deepfashion/Eval/list_eval_partition.txt

wget -c https://s3.ap-northeast-2.amazonaws.com/f-machine-learning-dataset/datasets/deepfashion/AttributePrediction/img.zip

unzip dataset/deepfashion/img.zip -d dataset/deepfashion
rm dataset/deepfashion/img.zip

unzip dataset/deepfashion/img.zip -d dataset/deepfashion
rm dataset/deepfashion/img.zip