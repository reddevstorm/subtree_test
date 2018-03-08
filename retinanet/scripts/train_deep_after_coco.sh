keras_retinanet/bin/train.py \
--batch-size 1 --epochs 50 --steps 10 \
--snapshot-path /Users/luke/Documents/ml_models/ \
--weights /Users/luke/Documents/ml_models/resnet50_coco_best_v1.2.2.h5 \
csv \
dataset/deepfashion/instances_train2017.csv \
dataset/deepfashion/categories2017.csv