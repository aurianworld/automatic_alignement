#!/usr/bin/env python3

import argparse
from sys import path_importer_cache
import pandas as pd
import numpy as np 
import time
import os


def beat_reg(file_path, precision = 1e-5):
    '''Take a beat-per-beat annotation file and outputs all the regular beat
    
    file_path : str of the directory where the annotations are//
    precision : precision of the regularity //
    '''
    t = time.time()

    for file in os.listdir(file_path):

        header = ["Time in s", "Beat"]
        data = pd.read_table(file_path+file, names = header)

        cond = np.zeros((data.shape[0], 1))

        for i in range(1,data.shape[0]-1) : 
            dist_beat_1 = np.abs(data.iloc[i - 1][0] - data.iloc[i][0])
            dist_beat_2 = np.abs(data.iloc[i + 1][0] - data.iloc[i][0])
            diff =np.abs(dist_beat_2 - dist_beat_1)

            if diff < precision : 
                cond[i,0] = diff
            #    cond[i-1,0] = diff
            #    cond[i+1,0] = diff
        
        data = data.iloc[cond != 0]

        #Difference of the time intervals between two regular beat
        data['Time difference'] = cond[cond != 0]
        
        output_data_path_csv = '~/Desktop/Dataset/04_Regular_beat/01_Regular_Beat/'+os.path.splitext(os.path.basename(file))[0]+'_regular_beat.csv'
        data.to_csv(output_data_path_csv, index=False)

        # output_data_path_txt = '/home/osboxes/Desktop/Dataset/04_Regular_beat/01_Regular_Beat/'+os.path.splitext(os.path.basename(file))[0]+'_regular_beat.txt'

        # data_output_numpy = output_data.to_numpy()

        # np.savetxt(output_data_path_txt, data_output_numpy)   

    return print("Done in " + str(time.time() - t))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find regular beat in annotation text file')

    parser.add_argument('--file_path', type=str, 
                            help='Path of the directory where the annotations are to analyse the beat regularity')

    parser.add_argument('--precision', type=float, 
                        help='Precision required to consider three consecutive beat to be regular')

    

    args = parser.parse_args()
    print(args.file_path, args.precision)
    beat_reg(args.file_path, precision = args.precision)