#!/usr/bin/env python3

def file_crop(t_start=0, length=5 ,**kwargs):
    ''' crop an audio or data file from t_start for a certain length
    
    Keyword arguments:
    t_start -- the starting point in the audio/data file
    length -- the length of the crop 
    audio_path -- the audio path
    data_path -- the data path
    '''

    from pydub import AudioSegment
    import pandas as pd
    import time

    t2 = 0
    t3 = 0

    for arg in kwargs:
        if arg == "audio_path" :
            t = time.time()
            audio_path = kwargs.get(arg)

            #We Check if we have a wav or a mp3
            if audio_path[-4:] == ".wav":
                audio_file = AudioSegment.from_wav(audio_path)[t_start*1000:(t_start+length)*1000]
            else :
                audio_file = AudioSegment.from_mp3(audio_path)[t_start*1000:(t_start+length)*1000]

            #We crop the audio and export it as wav
            output_audio_path = audio_path[:-4]+'_t='+str(t_start)+'s_'+'l='+str(length)+'s.wav'

            audio_file.export(output_audio_path, format="wav")

            t2 =  time.time() - t

        if arg == "data_path" : 
            t = time.time()

            data_path = kwargs.get(arg)
            
            data = pd.read_table(data_path, header = None)

            data = data[(data.iloc[:,0]>= t_start) & (data.iloc[:,0]<= t_start+length)]

            data[0] = data[0] - t_start

            output_data_path = data_path[:-4]+'_t='+str(t_start)+'s_'+'l='+str(length)+'s.csv'

            data.to_csv(output_data_path, header = False, index = False)

            t3 = time.time() - t

    return print("Done in : "+str(t2)+"s + "+ str(t3)+"s ="+str(t2+t3))