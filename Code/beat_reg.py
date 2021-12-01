#!/usr/bin/env python3

import argparse

def beat_reg(file_path, precision = 1e-5, t_start = None, length = None):
    '''Take a beat-per-beat annotation file and outputs all the regular beat
    
    file_path : str of the file path //
    precision : precision of the regularity //
    t_start : float starting time (optional) // 
    length : float of the length (optional) //
    '''
    import pandas as pd
    import numpy as np 
    import time

    t = time.time()

    data = pd.read_table(file_path, header = None)

    cond = np.zeros((data.shape[0], 1))

    for i in range(1,data.shape[0]-1) : 
        dist_beat_1 = np.abs(data.iloc[i - 1][0] - data.iloc[i][0])
        dist_beat_2 = np.abs(data.iloc[i + 1][0] - data.iloc[i][0])
        diff =np.abs(dist_beat_2 - dist_beat_1)

        if diff < precision : 
           cond[i,0] = diff
        #    cond[i-1,0] = diff
        #    cond[i+1,0] = diff
    
    output_data = data.iloc[cond != 0]

    output_data['diff'] = cond[cond != 0]
    
    output_data_path_csv = file_path[:-4]+'_t'+str(t_start)+'s_'+'l'+str(length)+'s_beat_regularity.csv'
    output_data_path_txt = file_path[:-4]+'_t'+str(t_start)+'s_'+'l'+str(length)+'s_beat_regularity.txt'

    output_data.to_csv(output_data_path_csv, header = False, index = False)

    data_output_numpy = output_data.to_numpy()

    np.savetxt(output_data_path_txt, data_output_numpy, fmt = ["%10.9f","%10.1f", "%10.9f"])   

    return print("Done in " + str(time.time() - t))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                         help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                         const=sum, default=max,
    #                         help='sum the integers (default: find the max)')

    parser.add_argument('--t_start', type=float, 
                            help='Starting time of the crop in s')

    parser.add_argument('--length', type=float, 
                            help='Length of the crop in second from the starting point')

    parser.add_argument('--file_path', type=str, 
                            help='Path of the data (anotation in .txt) to analyse for beat regularity')

    parser.add_argument('--precision', type=float, 
                        help='Precision required to consider three consecutive beat to be regular')

    

    args = parser.parse_args()
    print(args.file_path, args.precision, args.t_start, args.length)
    beat_reg(args.file_path, precision = args.precision, t_start = args.t_start, length = args.length)