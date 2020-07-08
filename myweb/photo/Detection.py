from segmentation import detect
import os
import cv2 as cv
import sys
ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)


def setup(model_path='D:\\Gproject\\Codes\\GFollow2020\\Segmentation\\logs\\Segment_model.h5'):
    config = detect.InferenceConfig()
    model = detect.load_model(model_path, config)
    return model


def result(img_path, save_path, conf=0.8):
    model = setup()
    img = cv.imread(img_path)
    img_name = img_path.split('//')[-1]
    r = detect.prediction(model, img)

    idx = 0
    for i in range(len(r['scores'])):
        if r['scores'][i] > conf:
            idx += 1
        else:
            break
    img_result = detect.get_overlay(
        img, r['rois'][:idx], r['masks'][..., :idx], r['class_ids'][:idx], ['BG', 'Calc', 'Mass'])

    cv.imwrite(save_path+'//'+img_name, img_result)
    print('save path : ', save_path+'//'+img_name)
