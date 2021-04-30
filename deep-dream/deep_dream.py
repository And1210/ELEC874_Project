import subprocess
import os

INPUT_IMG = 'carla_29_sidewalk'
IMG_TYPE = '.jpg'
LAYERS = ['conv1_7x7_s2','conv2_3x3_reduce','conv2_3x3','inception_3a_1x1','inception_3a_5x5_reduce','inception_3a_3x3_reduce','inception_3a_pool_proj','inception_3a_5x5','inception_3a_3x3','inception_3b_3x3_reduce','inception_3b_1x1','inception_3b_5x5_reduce','inception_3b_pool_proj','inception_3b_3x3','inception_3b_5x5','inception_4a_1x1','inception_4a_3x3_reduce','inception_4a_5x5_reduce','inception_4a_pool_proj','inception_4a_3x3','inception_4a_5x5','inception_4b_5x5_reduce','inception_4b_1x1','inception_4b_3x3_reduce','inception_4b_pool_proj','loss1_conv','inception_4b_5x5','inception_4b_3x3','loss1_fc_1','inception_4c_5x5_reduce','inception_4c_1x1','inception_4c_3x3_reduce','inception_4c_pool_proj','inception_4c_5x5','inception_4c_3x3','loss1_classifier_1','inception_4d_3x3_reduce','inception_4d_1x1','inception_4d_5x5_reduce','inception_4d_pool_proj','inception_4d_3x3','inception_4d_5x5','inception_4e_1x1','inception_4e_5x5_reduce','inception_4e_3x3_reduce','loss2_conv','inception_4e_pool_proj','inception_4e_5x5','inception_4e_3x3','loss2_fc_1','inception_5a_1x1','inception_5a_5x5_reduce','inception_5a_3x3_reduce','inception_5a_pool_proj','loss2_classifier_1','inception_5a_5x5','inception_5a_3x3','inception_5b_3x3_reduce','inception_5b_5x5_reduce','inception_5b_1x1','inception_5b_pool_proj','inception_5b_3x3','inception_5b_5x5', 'classifier']
MODIFIER = 'strong1'

def get_cmd(img_name, img_type, layers, modifier, use_layers_in_name):
    return "neural-dream -content_image inputs/{}{} -output_image outputs/{}{} -model_file models/bvlc_googlenet.pth -dream_layers {} -gpu 0 -num_iterations 1 -channel_mode {} -channels {} -original_colors 1 -jitter 0".format(img_name, img_type, img_name+"_{}".format(modifier)+(("/"+layers) if use_layers_in_name else ''), img_type, layers, ''.join([i for i in modifier if i.isalpha()]), ''.join([i for i in modifier if i.isdigit()]), 1 if "#" in modifier else 0)

def generate_textures(INPUT_IMG=INPUT_IMG, IMG_TYPE=IMG_TYPE, LAYERS=LAYERS, MODIFIER=MODIFIER):
    path = "outputs/{}".format(INPUT_IMG+"_{}/".format(MODIFIER))
    if not os.path.exists(path):
        os.makedirs(path)
    
    progress = 0
    layers = []
    for layer in LAYERS:
        cmd = get_cmd(INPUT_IMG, IMG_TYPE, layer, MODIFIER, True)
        print("COMMAND")
        print(cmd)
#        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
#        output, error = process.communicate()
        layers.append(layer)
        try:
            subprocess.check_call(cmd.split())
        except subprocess.CalledProcessError:
            layers.pop()
            print("Error in layer {}".format(layer))
        
#        if (error != None):
#            print(error)
        
        progress += 1
        
        print("{}% Complete".format(100*progress/len(LAYERS)))
    
    return layers

if __name__ == '__main__':
    generate_textures()
