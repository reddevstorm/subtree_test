#!/bin/bash

# http://cocodataset.org/#download
# 2017 dataset

mkdir -p dataset/coco
mkdir -p dataset/coco/images

wget http://images.cocodataset.org/zips/train2017.zip -O dataset/coco/images/train2017.zip
wget http://images.cocodataset.org/zips/val2017.zip -O dataset/coco/images/val2017.zip

wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip -O dataset/coco/annotations_trainval2017.zip

unzip dataset/coco/images/train2017.zip -d dataset/coco/images/
rm dataset/coco/images/train2017.zip

unzip dataset/coco/images/val2017.zip -d dataset/coco/images/
rm dataset/coco/images/val2017.zip

unzip dataset/coco/annotations_trainval2017.zip -d dataset/coco/
rm dataset/coco/annotations_trainval2017.zip