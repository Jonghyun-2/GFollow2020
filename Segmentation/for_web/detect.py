#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings("ignore")


# In[2]:


import os
import sys
import random
import itertools
import colorsys
import cv2 as cv
import os
import numpy as np
from skimage.measure import find_contours

from config import Config
from model import MaskRCNN
from visualize import display_instances


# In[3]:


class InferenceConfig(Config):
    """
    Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "shapes"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 2  # background + 2 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    IMAGE_RESIZE_MODE = "square"
    IMAGE_MIN_DIM = 1024
    IMAGE_MAX_DIM = 1024
    IMAGE_CHANNEL_COUNT = 3
    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 32

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = 200

    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 10


# In[4]:


def load_model(MODEL_DIR,config):
    
    # Recreate the model in inference mode
    model = MaskRCNN(mode="inference", 
                              config=config,
                              model_dir=MODEL_DIR)

    # Get path to saved weights
    # Either set a specific path or find last trained weights

    model_path = os.path.join(MODEL_DIR)
    # model_path = os.path.join(ROOT_DIR, r'/logs')
    # model_path = model.find_last()

    # Load trained weights
    print("Loading weights from ", model_path)
    model.load_weights(model_path, by_name=True)
    return model
def prediction(model, image):
    # 모델 예측
    results = model.detect([image], verbose=1)
    r = results[0]
    return r

def get_overlay(image, boxes, masks, class_ids, class_names,
                      scores=None, title="",
                    show_bbox=True,colors=None, captions=None):
                      
    """
    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
    masks: [height, width, num_instances]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # Number of instances
    N = boxes.shape[0]
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    # If no axis is passed, create one and automatically call show()
#     auto_show = False
#     if not ax:
#         _, ax = plt.subplots(1, figsize=figsize)
#         auto_show = True

    # Generate random colors
    #colors = colors or random_colors(N)
    colors = colors

    # Show area outside image boundaries.
    height, width = image.shape[:2]
#     ax.set_ylim(height + 10, -10)
#     ax.set_xlim(-10, width + 10)
#     ax.axis('off')
#     ax.set_title(title)

    masked_image = image.astype(np.uint8).copy()
    for i in range(N):
        color = (1,1,1)

        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]
        if show_bbox:
#             p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
#                                 alpha=0.7, linestyle="dashed",
#                                 edgecolor=color, facecolor='none')
#             ax.add_patch(p)
            cv.rectangle(masked_image,(x1,y1),(x2,y2),color,10)
            

        # Label
        if not captions:
            class_id = class_ids[i]
            score = scores[i] if scores is not None else None
            label = class_names[class_id]
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        cv.putText(masked_image,caption,(x1, y1 + 8),cv.FONT_HERSHEY_COMPLEX,3,(0,0,0),3)
#         ax.text(x1, y1 + 8, caption,
#                 color='w', size=11, backgroundcolor="none")

        # Mask
        mask = masks[:, :, i]
#         if show_mask:
#             masked_image = apply_mask(masked_image, mask, color)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            masked_image = cv.polylines(masked_image,np.int32([verts]),True,(0,0,0),7)
#             p = Polygon(verts, facecolor="none", edgecolor=color)
#             ax.add_patch(p)
            
#    ax.imshow(masked_image.astype(np.uint8))
#     if auto_show:
#         plt.show()
    return masked_image


# In[5]:





# In[6]:





# In[7]:


# model = load_model(r'../logs/Segment_model.h5',InferenceConfig())
# img = cv.imread(r'E:\DataSet\CBIS-DDSM\Crop_train\Mass-Training_P_01138_RIGHT_CC_full.png')
# ans = prediction(model,img)


# In[8]:


# conf = 0.9
# idx = 0
# for i in range(len(ans['scores'])):
#     if ans['scores'][i] > conf:
#         idx +=1
#     else : break
# print("Conf idx :", idx)
# a = get_overlay(img, ans['rois'][:idx],ans['masks'][...,:idx],ans['class_ids'][:idx],['BG','Calc','Mass'])


# In[ ]:




