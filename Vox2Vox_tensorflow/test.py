import os, v3dpy

from v3dpy.loaders import PBD

path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\target_image_aug\09133_P048_T01_(3)_S009_-_TL.R_R0919_WYT_20230818_WYT\x_2_y_1.v3dpbd'
pbd = PBD()
v3d_img = pbd.load(path)

