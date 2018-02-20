#!/bin/sh
python keras_retinanet/bin/train.py --batch-size 1 --epochs 30 --steps 10000 csv dataset/deepfashion/instances_train2017.csv dataset/deepfashion/categories2017.csv
