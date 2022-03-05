import os, re

def annotation_from_audio(audio_path):

    #We get only the base name of the audio path
    file_name = os.path.basename(audio_path)[:-4] #we don't take the file extension
    cropped = False

    #We do some regular expression check to see if it is a crop file or a whole symphonie
    pattern = '_s'+r'[0-3]?[0-9]+.[0-9]'+'_e'+r'[0-3]?[0-9]+.[0-9]'
    search = re.search(pattern,file_name)
    if search:
        cropped = True
        cropped_beats = search.group(0)


    #If it is cropped: 
    if cropped:
        folder_path = '/home/osboxes/Desktop/Dataset/02_Beat_per_beat_annotation/02_Cropped_Symphonies/'
        for file in os.listdir(folder_path):
            
            base_name = os.path.basename(file)
            file_name = re.sub(cropped_beats, '',file_name) #We use only the file name without the beat start and end markers
            pattern = file_name + r'.*' + cropped_beats  #We know that the annotation files have additional info after the file name 
            search = re.search(pattern,base_name)
            if search :
                return folder_path + search.group(0) + '.txt'
            else :
                return 'No annotation for this audio file'
    
    #If it is not cropped:  
    folder_path = '/home/osboxes/Desktop/Dataset/02_Beat_per_beat_annotation/01_Full_Symphonies/'
    for file in os.listdir(folder_path):
        
        base_name = os.path.basename(file)
        pattern = file_name + r'.*' 
        search = re.search(pattern,base_name)
        if search :
            return folder_path + search.group(0)
        else :
                return 'No annotation for this audio file'