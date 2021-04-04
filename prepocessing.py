from utils import *

split_image_xml(TRAIN_FOLDER, TRAIN_IMAGES, TRAIN_XML, split = 'TRAIN')
split_image_xml(TEST_FOLDER, TEST_IMAGES, TEST_XML, split = 'TEST')

assert len(TRAIN_IMAGES) == len(TRAIN_XML)

assert len(TEST_IMAGES) == len(TEST_XML)

# remove_fault_data(TRAIN_XML, split = 'TRAIN')
# assert len(TRAIN_IMAGES) == len(TRAIN_XML)

# remove_fault_data(TEST_XML, split = 'TEST')
# assert len(TEST_IMAGES) == len(TEST_XML)

parse_annotation(TRAIN_XML, split = 'TRAIN')
assert len(TRAIN_XML) == len(TRAIN_OBJECTS)
assert len(TRAIN_IMAGES) == len(TRAIN_OBJECTS)

parse_annotation(TEST_XML, split = 'TEST')
assert len(TEST_IMAGES) == len(TEST_OBJECTS)




