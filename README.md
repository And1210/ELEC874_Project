# ELEC874_Project - T-Dream
T-Dream, a texture transfer method which uses Google DeepDream.

# Requirements
- Python 3.7
- MATLAB
- CUDA

# Setup
To setup, clone this repository. Then, pip install any required packages. This can be done with the following command:
```python3.7 -m pip install shutil neural-dream opencv-python subprocess```
Next, make sure you have the MATLAB Python api setup, https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html.
Then, navigate to the deep-dream folder and run 
```python3.7 main.py ${NAME}```
Where ${NAME} is the name of the folder with the segments that you would like to texture transfer.

The demo can be run using ```python3.7 main.py carla_city3_day_clear_6```.
