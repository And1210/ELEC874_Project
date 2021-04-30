from texture_transfer import texture_transfer
from deep_dream import generate_textures
from mask_output_images import mask_images
import os
import sys
import shutil

def run_transfer(INPUT_IMG, FORMAT, MODIFIER, CUR_SEGMENT):
    CLASS_PATH = '/home/andrew/ELEC874/Project/FWLBP/ground_truth/{}/'.format(CUR_SEGMENT)
    layers = generate_textures(INPUT_IMG, FORMAT, MODIFIER=MODIFIER)
    mask_images(BASE_IMG="inputs/{}{}".format(INPUT_IMG, FORMAT), IMG_DIR="outputs/{}_{}/".format(INPUT_IMG, MODIFIER))
    texture_transfer(IMG_CLASS_PATH=CLASS_PATH, IMGS_PATH="/home/andrew/ELEC874/Project/deep-dream/outputs/{}{}/".format(INPUT_IMG, "_"+MODIFIER), OUTPUT_PATH='/home/andrew/ELEC874/Project/tests/{}{}'.format(INPUT_IMG, FORMAT), INPUT_IMG=INPUT_IMG, LAYERS=layers, FORMAT=FORMAT, MODIFIER=MODIFIER)

def main(NAME, FORMAT):
    PATH = '../tests/{}/'.format(NAME)
    dir_imgs = os.listdir(PATH)
    
    for f in dir_imgs:
        if (FORMAT not in f):
            print("Couldn't read file {}".format(f))
            continue
        
        cur = f.replace(FORMAT, '')
        input_name = "{}_{}".format(NAME, cur)
        
        shutil.copy(PATH+f, 'inputs/{}{}'.format(input_name, FORMAT))
        run_transfer(input_name, FORMAT, 'strong1', cur)

if (len(sys.argv) != 2):
    print('Error, missing argument')
    exit(1)
    
main(sys.argv[1], '.jpg')