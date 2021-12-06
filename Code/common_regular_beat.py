#!/usr/bin/env python3

import os
import numpy as np

dirpath = "/home/osboxes/Data/beat-per-beat/_data/processed/Regular Beat/"
ext = ('.csv')

for file_1 in os.listdir(dirpath):
    if file_1.endswith(ext):

        np_file_1 =genfromtxt(dirpath+file_1, delimiter=',')

        for file_2 in os.listdir(dirpath):
            if file_2.endswith(ext) and file_1 != file_2 :

                np_file_2 =np.genfromtxt(dirpath+file_2, delimiter=',')

                common_beat = np.intersect1d(np_file_1[:,1],np_file_2[:,1])

                np.savetxt(dirpath+'/common_beat/'+file_1[:35]+'__and__'+file_2[:35]+'_commonn_beat.txt', common_beat, fmt='%.3f', delimiter=",")