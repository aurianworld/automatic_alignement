#!/usr/bin/env python3

# This script is going throught all the .csv file that contains the "regular beat" of a performance, and outputs .txt files of the common regular beat between two performances

import os
import numpy as np

dirpath = "/home/osboxes/Data/beat-per-beat/_data/processed/Regular Beat/"
ext = ('.csv')
visit = []

for file_1 in os.listdir(dirpath):
    if file_1.endswith(ext):

        np_file_1 =np.genfromtxt(dirpath+file_1, delimiter=',')
        visit += [file_1]

        for file_2 in os.listdir(dirpath):
            if file_2.endswith(ext) and file_2 not in visit :

                np_file_2 =np.genfromtxt(dirpath+file_2, delimiter=',')

                common_beat = np.intersect1d(np_file_1[:,1],np_file_2[:,1])

                np.savetxt(dirpath+'/common_beat/'+file_1[:50]+'__and__'+file_2[:50]+'_commonn_beat.txt', common_beat, fmt='%.3f', delimiter=",")