import matlab.engine
import cv2
import numpy as np
import os
from deep_dream import get_cmd
import subprocess
import shutil

MATLAB_PATH = '/home/andrew/ELEC874/Project/FWLBP/'
OUTPUT_PATH = '/home/andrew/ELEC874/Project/tests/sidewalk.jpg'

IMG_CLASS_PATH = '/home/andrew/ELEC874/Project/FWLBP/ground_truth/cement/'
IMGS_PATH = '/home/andrew/ELEC874/Project/deep-dream/outputs/carla_29_sidewalk_strong1/'

LAYERS = ['conv1_7x7_s2','conv2_3x3_reduce','conv2_3x3','inception_3a_1x1','inception_3a_5x5_reduce','inception_3a_3x3_reduce','inception_3a_pool_proj','inception_3a_5x5','inception_3a_3x3','inception_3b_3x3_reduce','inception_3b_1x1','inception_3b_5x5_reduce','inception_3b_pool_proj','inception_3b_3x3','inception_3b_5x5','inception_4a_1x1','inception_4a_3x3_reduce','inception_4a_5x5_reduce','inception_4a_pool_proj','inception_4a_3x3','inception_4a_5x5','inception_4b_5x5_reduce','inception_4b_1x1','inception_4b_3x3_reduce','inception_4b_pool_proj','loss1_conv','inception_4b_5x5','inception_4b_3x3','loss1_fc_1','inception_4c_5x5_reduce','inception_4c_1x1','inception_4c_3x3_reduce','inception_4c_pool_proj','inception_4c_5x5','inception_4c_3x3','loss1_classifier_1','inception_4d_3x3_reduce','inception_4d_1x1','inception_4d_5x5_reduce','inception_4d_pool_proj','inception_4d_3x3','inception_4d_5x5','inception_4e_1x1','inception_4e_5x5_reduce','inception_4e_3x3_reduce','loss2_conv','inception_4e_pool_proj','inception_4e_5x5','inception_4e_3x3','loss2_fc_1','inception_5a_1x1','inception_5a_5x5_reduce','inception_5a_3x3_reduce','inception_5a_pool_proj','loss2_classifier_1','inception_5a_5x5','inception_5a_3x3','inception_5b_3x3_reduce','inception_5b_5x5_reduce','inception_5b_1x1','inception_5b_pool_proj','inception_5b_3x3','inception_5b_5x5', 'classifier']
FORMAT='.jpg'
MODIFIER='strong1'
INPUT_IMG = 'carla_29_sidewalk'

IMG_SIZE = (512, 512)

eng = matlab.engine.start_matlab()
eng.cd(MATLAB_PATH)

def texture_transfer(OUTPUT_PATH=OUTPUT_PATH, IMG_CLASS_PATH=IMG_CLASS_PATH, IMGS_PATH=IMGS_PATH, IMG_SIZE=IMG_SIZE, INPUT_IMG=INPUT_IMG, LAYERS=LAYERS, FORMAT=FORMAT, MODIFIER=MODIFIER):
    weights = eng.get_class_weights(IMGS_PATH, IMG_CLASS_PATH, nargout=1)
    weights = list(weights._data)
    print(len(weights))
    
    print('Generating Top-5 Layer Match Dream...')
    weights_scored = [{'val':weights[i], 'id':i} for i in range(len(weights))]
    weights_scored = sorted(weights_scored, key=lambda x: x['val'], reverse=True)
    layers = ""
    count = 0
    for w in weights_scored[0:5]:
        layers += LAYERS[w['id']]
        if (count < 4):
            layers += ','
        count += 1
    shutil.copy("inputs/{}{}".format(INPUT_IMG, FORMAT), "inputs/{}_top5{}".format(INPUT_IMG, FORMAT))
    cmd = get_cmd(INPUT_IMG+"_top5", FORMAT, layers, MODIFIER, False)
    print(cmd)
    try:
        subprocess.check_call(cmd.split())
    except subprocess.CalledProcessError:
        print("Error in top-5 layers to image generation")
    
    print('Generating weighted averaged image')
    output_image = np.zeros((IMG_SIZE[0], IMG_SIZE[1], 3), np.float64)
    dir_imgs = sorted(os.listdir(IMGS_PATH))
    count = 0
    for f in dir_imgs:
        img = cv2.imread(IMGS_PATH+f)
        output_image += weights[count]*img
    #    for i in range(IMG_SIZE[0]):
    #        for j in range(IMG_SIZE[1]):
    #            for k in range(3):
    #                output_image[i,j,k] += weights[count]*img[i,j,k]
        count += 1
    
    cv2.imwrite(OUTPUT_PATH, output_image)
    
if __name__ == '__main__':
    texture_transfer()