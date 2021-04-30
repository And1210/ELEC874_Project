import os
import cv2

BASE_IMG = "inputs/carla_29_sidewalk.jpg"
IMG_DIR = "outputs/carla_29_sidewalk_strong1/"
IMG_SHAPE = (512, 512)

def mask_image(mask, img):    
    out = img
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            if (sum(mask[i][j]==[0, 0, 0])==len(mask[i][j])):
                out[i][j] = [0, 0, 0]
    return out

def mask_images(BASE_IMG=BASE_IMG, IMG_DIR=IMG_DIR, IMG_SHAPE=IMG_SHAPE):
    dir_imgs = os.listdir(IMG_DIR)
    
    base_img = cv2.imread(BASE_IMG)
    base_img = cv2.resize(base_img, IMG_SHAPE, interpolation=cv2.INTER_NEAREST)
    progress = 0
    for f in dir_imgs:
        print("Masking image {}".format(f))
        img = cv2.imread(IMG_DIR+f)
        img = mask_image(base_img, img)
        cv2.imwrite(IMG_DIR+f, img)
        progress += 1
        print("Successfully masked, {}% complete".format(100*progress/len(dir_imgs)))
        
if __name__ == '__main__':
    mask_images()