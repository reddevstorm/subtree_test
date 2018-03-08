#!/bin/sh
nohup cmd & python keras_retinanet/bin/train.py --batch-size 1 --epochs 10 --steps 50000 csv /Users/edwin/Documents/works/AI/datasets/deepfashion/instances_train2017.csv /Users/edwin/Documents/works/AI/datasets/deepfashion/categories2017.csv

