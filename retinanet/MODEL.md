# 입력 
(None, None, 3)의 이미지

# Network

## 개요
Resnet에서 C3, C4, C5를 이어받아 새로운 Retinanet모델을 생성
1. submodel 생성
    * regression 모델 생성
    * classification 모델 생성
1. pyramid_features 생성 (Focal Loss for Dense Object Detection이 적용되는 부분)
    * resnet에서 전달받은 Conv2D(C3, C4, C5)를 이용하여 새로운 pyramid_features(P3, P4, P5, P6, P7)를 생성
    * C3, C4, C5는 resnet에서 중간중간 생성되는 Conv2D들을 변수에 담아놓은 것
    * P3, P4, P5, P6, P7들은 C3, C4, C5에서 별도로 Conv2D등 layer를 붙여서 생성한 것
1. pyramid 생성
    * submodel과 pyramid_features을 조합하여 생성

C3, C4, C5 -> P3, P4, P5, P6, P7
[P3, P4, P5, P6, P7] + [regression, classification] -> [regression(P3)(P4)(P5)(P6)(P7), classification(P3)(P4)(P5)(P6)(P7)]

## 1.Resnet에서 C3, C4, C5를 이어받아 새로운 Retinanet모델을 생성
* resnet에서 C3, C4, C5를 이어받아 pyramid_features를 생성
* C3, C4, C5는 Conv2D로 순차적으로 연결되어 있는 network를 중간중간 저장하여 놓은 변수이다.
```python
def retinanet(
    inputs,
    backbone,
    num_classes,
    anchor_parameters       = AnchorParameters.default,
    create_pyramid_features = __create_pyramid_features,
    submodels               = None,
    name                    = 'retinanet'
):
    if submodels is None:
        submodels = default_submodels(num_classes, anchor_parameters)

    _, C3, C4, C5 = backbone.outputs  # we ignore C2

    # compute pyramid features as per https://arxiv.org/abs/1708.02002
    features = create_pyramid_features(C3, C4, C5)

    # for all pyramid levels, run available submodels
    pyramid = __build_pyramid(submodels, features)
    anchors = __build_anchors(anchor_parameters, features)

    return keras.models.Model(inputs=inputs, outputs=[anchors] + pyramid, name=name)

def resnet_retinanet(num_classes, backbone=50, inputs=None, **kwargs):
    allowed_backbones = [50, 101, 152]
    if backbone not in allowed_backbones:
        raise ValueError('Backbone (\'{}\') not in allowed backbones ({}).'.format(backbone, allowed_backbones))

    # choose default input
    if inputs is None:
        inputs = keras.layers.Input(shape=(None, None, 3))

    # create the resnet backbone
    if backbone == 50:
        resnet = keras_resnet.models.ResNet50(inputs, include_top=False, freeze_bn=True)
    elif backbone == 101:
        resnet = keras_resnet.models.ResNet101(inputs, include_top=False, freeze_bn=True)
    elif backbone == 152:
        resnet = keras_resnet.models.ResNet152(inputs, include_top=False, freeze_bn=True)

    # create the full model
    model = retinanet.retinanet_bbox(inputs=inputs, num_classes=num_classes, backbone=resnet, **kwargs)

    return model
```

### create_pyramid_features

### build_pyramid

### build_anchors

### default_regression_model
```
inputs  = keras.layers.Input(shape=(None, None, 256))

outputs = inputs
+ keras.layers.Conv2D(filters=256, activation='relu', name='pyramid_regression_0', **options)(outputs)
+ keras.layers.Conv2D(filters=256, activation='relu', name='pyramid_regression_1', **options)(outputs)
+ keras.layers.Conv2D(filters=256, activation='relu', name='pyramid_regression_2', **options)(outputs)
+ keras.layers.Conv2D(filters=256, activation='relu', name='pyramid_regression_3', **options)(outputs)
```
* input - width, height가 정해지지 않은 256 채널
* output - input에서 Conv2D(256 filter) 4개를 추가한다

### default_classification_model


## 2.Retinanet에서 output도출
```python
def retinanet_bbox(inputs, num_classes, nms=True, name='retinanet-bbox', *args, **kwargs):
    model = retinanet(inputs=inputs, num_classes=num_classes, *args, **kwargs)

    # we expect the anchors, regression and classification values as first output
    anchors        = model.outputs[0]
    regression     = model.outputs[1]
    classification = model.outputs[2]

    # apply predicted regression to anchors
    boxes      = layers.RegressBoxes(name='boxes')([anchors, regression])
    detections = keras.layers.Concatenate(axis=2)([boxes, classification] + model.outputs[3:])

    # additionally apply non maximum suppression
    if nms:
        detections = layers.NonMaximumSuppression(name='nms')([boxes, classification, detections])

    # construct the model
    return keras.models.Model(inputs=inputs, outputs=model.outputs[1:] + [detections], name=name)
```






## AnchorParameters
```
AnchorParameters.default = AnchorParameters(
    sizes   = [32, 64, 128, 256, 512],
    strides = [8, 16, 32, 64, 128],
    ratios  = np.array([0.5, 1, 2], keras.backend.floatx()),
    scales  = np.array([2 ** 0, 2 ** (1.0 / 3.0), 2 ** (2.0 / 3.0)], keras.backend.floatx()),
)
```