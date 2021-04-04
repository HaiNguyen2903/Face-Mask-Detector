from utils import *
from prepocessing import *

folder = './Datasets/FaceMask Dataset/'
create_json_data_list(folder)

print(len(TRAIN_IMAGES), len(TRAIN_OBJECTS))
print(len(TEST_IMAGES), len(TEST_OBJECTS))
