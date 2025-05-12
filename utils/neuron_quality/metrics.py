#!/usr/bin/env python
import os

#================================================================
#   Copyright (C) 2023 Yufeng Liu (Braintell, Southeast University). All rights reserved.
#   
#   Filename     : metrics.py
#   Author       : Yufeng Liu
#   Date         : 2023-04-04
#   Description  : 
#
#================================================================

import numpy as np

from utils.swc_handler import tree_to_voxels, parse_swc
from utils.math_utils import min_distances_between_two_sets

class DistanceEvaluation(object):
    def __init__(self, dsa_thr=2., resample1=True, resample2=True):
        self.dsa_thr = dsa_thr
        self.resample1 = resample1
        self.resample2 = resample2

    def calc_dist(self, voxels1, voxels2):
        ds = {
            'ESA': None,
            'DSA': None,
            'PDS': None,
        }

        dists1, dists2 = min_distances_between_two_sets(voxels1, voxels2, reciprocal=True, return_index=False)
        for key in ds.keys():
            if key == 'DSA':
                dists1_ = dists1[dists1 > self.dsa_thr]
                dists2_ = dists2[dists2 > self.dsa_thr]
                if dists1_.shape[0] == 0:
                    dists1_ = np.array([0.])
                if dists2_.shape[0] == 0:
                    dists2_ = np.array([0.])
            elif key == 'PDS':
                dists1_ = (dists1 > self.dsa_thr).astype(np.float32)
                dists2_ = (dists2 > self.dsa_thr).astype(np.float32)
            elif key == 'ESA':
                dists1_ = dists1
                dists2_ = dists2
            ds[key] = dists1_.mean(), dists2_.mean(), (dists1_.sum() + dists2_.sum()) / (len(dists1) + len(dists2))
        ds = np.array(list(ds.values()))
        return ds

    def run(self, reconfile, gsfile):
        if type(reconfile) is str or isinstance(reconfile, os.PathLike):
            tree1 = parse_swc(reconfile)
        else:
            tree1 = reconfile
        if type(gsfile) is str or isinstance(reconfile, os.PathLike):
            tree2 = parse_swc(gsfile)
        else:
            tree2 = gsfile
        #print(f'#nodes for recon and gs: {len(tree1)}, {len(tree2)}')

        if self.resample1:
            voxels1 = tree_to_voxels(tree1, crop_box=(100000,100000,100000))
        else:
            voxels1 = np.array([node[2:5] for node in tree1])
        if self.resample2:
            voxels2 = tree_to_voxels(tree2, crop_box=(100000,100000,100000))
        else:
            voxels2 = np.array([node[2:5] for node in tree2])

        if len(voxels1) == 0 or len(voxels2) == 0:
            print(len(voxels1), len(voxels2))
            return None
        
        ds = self.calc_dist(voxels1, voxels2)
        return ds


if __name__ == '__main__':
    gsfile = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\gold_standard_modified\03764_P025_T02_-S054_TL_R0613_YW-20230204_NYT_stamp_2024_07_29_09_31.ano.eswc.attachment.eswc'
    reconfile = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\sliver_standard_CAR_modified_data\03764_P025_T02_-S054_TL_R0613_YW-20230204_NYT_stamp_2024_07_29_09_31.ano.eswc'
    de = DistanceEvaluation()
    ds = de.run(reconfile, gsfile)
    print(ds)


