import os
import json
from pathlib import Path
import xml.etree.ElementTree as ET

# Labels of dataset
DATA_LABELS = {'face', 'face_mask'}
# Map from labels to label ids
LABEL_MAP = {k: v+1 for v, k in enumerate(DATA_LABELS)}

# TRAIN and TEST folder
TRAIN_FOLDER = Path('./Datasets/FaceMask Dataset/train/')
TEST_FOLDER = Path('./Datasets/FaceMask Dataset/val/')

TRAIN_PATH = './Datasets/FaceMask Dataset/train/'
TEST_PATH = './Datasets/FaceMask Dataset/val/'

# Split to check which type is data belong to
SPLIT = ['TRAIN', 'TEST']

# Lists for seperating data
TRAIN_IMAGES = list()
TRAIN_XML = list()
TEST_IMAGES = list()
TEST_XML = list()

# List to contain objects info : bboxes, labels, difficulites
TRAIN_OBJECTS = list()
TEST_OBJECTS = list()

# Split data in to images list and annotations list
def split_image_xml(origin_folder, image_list, xml_list, split):
    split = split.upper()
    assert split in SPLIT

    train_removed = 0
    test_removed = 0

    for file in origin_folder.iterdir():
        name = file.name
        xml_path = ''
        img_path = ''

        if name[-3:] != 'xml':
            if split == 'TRAIN':
                xml_path = os.path.join(TRAIN_PATH, name[:-3] + 'xml')
                img_path = os.path.join(TRAIN_PATH, name)
            else:
                xml_path = os.path.join(TEST_PATH, name[:-3] + 'xml')
                img_path = os.path.join(TEST_PATH, name)

            if is_valid(xml_path):
                xml_list.append(xml_path)
                image_list.append(img_path)
            else:
                if split == 'TRAIN':
                    train_removed += 1
                else:
                    test_removed += 1
    print('{} DATA REMOVED: {}'.format(split, train_removed if split == 'TRAIN' else test_removed))
    return

# Remove some noise and fault data from the dataset
def is_valid(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    features = list()
    
    for child in root:
        features.append(child.tag)

    # Check whether xml file contains size of image or not
    if 'size' not in features or 'object' not in features:
        return False

    else:
        # Check whether width or height of image = 0 or not
        for child in root:
            if child.tag == 'size':
                width = int(child.find('width').text) 
                height = int(child.find('height').text)
                depth = int(child.find('depth').text)

                if width <= 0 or height <= 0 or width is None or height is None:
                    return False
    return True


# Parsing annotation from xml files to dictionaries
def parse_annotation(xml_list, split):
    for path in xml_list:
        split = split.upper()
        assert split.upper() in SPLIT

        tree = ET.parse(path)
        root = tree.getroot()

        boxes = list()
        labels = list()
        difficulties = list()

        width = height = depth = 0

        for child in root:
            if child.tag == 'size':
                width = int(child.find('width').text) 
                height = int(child.find('height').text)
                depth = int(child.find('depth').text)

            if child.tag == 'object':
                label = child.find('name').text
                if label not in DATA_LABELS:
                    continue

                difficult = int(child.find('difficult').text)
                bbox = child.find('bndbox')
                
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text) 
                xmax = int(bbox.find('xmax').text) 
                ymax = int(bbox.find('ymax').text) 
                
                precision = 4
                xmin_normalized = round(xmin / width, precision)
                ymin_normalized = round(ymin / height, precision)
                xmax_normalized = round(xmax / width, precision)
                ymax_normalized = round(ymax / height, precision)

                labels.append(LABEL_MAP[label])
                difficulties.append(difficult)
                boxes.append([xmin_normalized, ymin_normalized, xmax_normalized, ymax_normalized])

        if split == 'TRAIN':
            TRAIN_OBJECTS.append({'boxes': boxes, 'labels': labels, 'difficulties': difficulties})
        elif split == 'TEST':
            TEST_OBJECTS.append({'boxes': boxes, 'labels': labels, 'difficulties': difficulties})
    return {'boxes': boxes, 'labels': labels, 'difficulties': difficulties}


def create_json_data_list(output_folder):
    with open(os.path.join(output_folder, 'TRAIN_IMAGES.json'), 'w') as j:
        json.dump(TRAIN_IMAGES, j)
    with open(os.path.join(output_folder, 'TRAIN_OBJECTS.json'), 'w') as j:
        json.dump(TRAIN_OBJECTS, j)

    with open(os.path.join(output_folder, 'TEST_IMAGES.json'), 'w') as j:
        json.dump(TEST_IMAGES, j)
    with open(os.path.join(output_folder, 'TEST_OBJECTS.json'), 'w') as j:
        json.dump(TEST_OBJECTS, j)

    
