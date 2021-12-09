#!/usr/bin/env python3

import argparse

def file_crop_beat(beat_start=1.1, beat_stop=32.1 ,**kwargs):
    ''' crop an audio and data file from beat_start to beat_stop in the performance
    
    Keyword arguments:
    beat_start -- the starting point in the audio and data file 
    beat_start -- the ending point in the audio and data file
    audio_path -- the audio path
    data_path -- the data path
    '''

    import subprocess
    import shlex
    import pandas as pd
    import time
    import numpy as np

    t2 = 0
    t3 = 0

    for arg in kwargs:
        if arg == "data_path" and kwargs.get(arg) != None : 
            t = time.time()

            data_path = kwargs.get(arg)
            
            data = pd.read_table(data_path, header = None)

            #We Define t_start and t_stop depending on the beat measure

            t_start = data[(data.iloc[:,1] == beat_start)].reset_index(drop = True)
            t_start = t_start[0][0]
            t_stop = data[(data.iloc[:,1] == beat_stop)].reset_index(drop = True)
            t_stop = t_stop[0][0]

            data = data[(data.iloc[:,0]>= t_start) & (data.iloc[:,0]<= t_stop)]

            data[0] = data[0] - t_start

            output_data_path_csv = data_path[:-4]+'_s'+str(beat_start)+'_'+'e'+str(beat_stop)+'.csv'
            output_data_path_txt = data_path[:-4]+'_s'+str(beat_start)+'_'+'e'+str(beat_stop)+'.txt'

            data.to_csv(output_data_path_csv, header = False, index = False)

            data_numpy = data.to_numpy()

            np.savetxt(output_data_path_txt, data_numpy, fmt = ["%10.9f","%10.1f"])

            t3 = time.time() - t


        if arg == "audio_path" and kwargs.get(arg) != None :
            t = time.time()
            audio_path = kwargs.get(arg)

            # #We Check if we have a wav or a mp3
            # if audio_path[-4:] == ".wav":
            #     audio_file = AudioSegment.from_wav(audio_path)[t_start*1000:(t_start+length)*1000]
            # else :
            #     audio_file = AudioSegment.from_mp3(audio_path)[t_start*1000:(t_start+length)*1000]


            #We crop the audio and export it as wav
            output_audio_path = audio_path[:-4]+'_s'+str(beat_start)+'_'+'e'+str(beat_stop)+'.wav'

            bashCommand = "ffmpeg -loglevel quiet -ss "+ str(t_start) + " -t "+ str(t_stop-t_start)+" -i "+audio_path+" "+ output_audio_path

            args = shlex.split(bashCommand)

            process = subprocess.Popen(args)
            output, error = process.communicate()

            t2 =  time.time() - t

    return print("Done in : "+str(t2)+"s + "+ str(t3)+"s ="+str(t2+t3))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                         help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                         const=sum, default=max,
    #                         help='sum the integers (default: find the max)')

    parser.add_argument('beat_start', type=float, 
                            help='Starting beat of the crop')

    parser.add_argument('beat_stop', type=float, 
                            help='Last beat to be taken into account')

    parser.add_argument('--audio_path', type=str, 
                            help='Path of the audio file to crop')

    parser.add_argument('--data_path', type=str, 
                            help='Path of the data (anotation in .txt) to crop')

    

    args = parser.parse_args()
    print(args.beat_start, args.beat_stop, args.data_path, args.audio_path)
    file_crop_beat(args.beat_start, args.beat_stop, data_path = args.data_path, audio_path = args.audio_path)