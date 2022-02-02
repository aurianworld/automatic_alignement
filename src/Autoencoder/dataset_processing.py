#!/usr/bin/env python3


import os
import argparse
import random
import subprocess, json
import tensorflow as tf
import tensorflow_io as tfio

# compatibility with tf.23 and tfio 0.16
try: 
    AUTOTUNE = tf.data.AUTOTUNE
except:
    AUTOTUNE = tf.data.experimental.AUTOTUNE

try:
    spectrogram = tfio.audio.spectrogram
    melscale = tfio.audio.melscale
except:
    spectrogram = tfio.core.python.api.experimental.audio.spectrogram
    melscale = tfio.core.python.api.experimental.audio.melscale

#Useful functions 
def path_to_audio(path):
    """Reads and decodes an audio file (MP3) for now"""
    audio = tf.io.read_file(path)
    audio = tfio.audio.decode_mp3(audio)
    return audio

def paths_to_dataset(audio_paths):
    """Constructs a dataset of audios and labels."""
    path_ds = tf.data.Dataset.from_tensor_slices(audio_paths)
    audio_ds = path_ds.map(lambda x: path_to_audio(x))

    #Converting Stereo to mono by summing the channel and dividing by 2
    audio_ds = audio_ds.map(lambda x: tf.math.divide(
        tf.reduce_sum(x,axis=1,keepdims=True),
        tf.constant([2.])))
    
    return audio_ds


def audio_to_spectrograms(x):
    # Since tf.signal.fft applies FFT on the innermost dimension,
    # we need to squeeze the dimensions and then expand them again
    # after FFT
    x = tf.squeeze(x, axis=-1)
    x = spectrogram(x, nfft=256, window=256, stride=128) 
    x = tf.expand_dims(x, axis=-1)
    
    return x


def spectrograms_to_melspectrograms(x):
    #Takes a spectrogram tensor and convert it into a a Mel Spectrograms
    x = tf.squeeze(x, axis=-1)    
    x = melscale(x, rate=16000, mels=128, fmin=20, fmax=8000)
    x = tf.expand_dims(x, axis=-1)
    print(x[:,:128,:].shape)
    # Return the mel_spectrogram without the bin for the highest frequencies 
    # since we want only 128 frequency bins

    return x[:,:128,:]


def normalize_spectrograms(x):
    # Normalizing along the frequency axis by L2 norm
    x = tf.math.l2_normalize(x, axis=1, epsilon=1e-12) 

    return x    

def splitting_spectrograms(tensor,n):
    #We want to split our whole spectogram into bins of size n
    a =[]
    q, r = tf.shape(tensor)[0]//n, tf.shape(tensor)[0]%n
    for i in range(q): 
      a.append(tensor[n*i:n*(i+1),:,:])
    a.append(tf.concat([tensor[q*n:,:,:],tf.zeros([n - r,128,1])],0))

    return tf.data.Dataset.from_tensor_slices(a)

def is_compatible_mp3(filename):
    format = subprocess.check_output(['ffprobe','-v', 'quiet', '-print_format','json','-show_format', '-i', filename]) 
    format = json.loads(format.decode())

    
    if  ('tags' in format['format']) and \
        ('compatible_brands' in format['format']['tags']) and \
        (format['format']['tags']['compatible_brands'] == 'isomiso2'):
        print('Removing %s from dataset because of incompatible isomiso format' % filename)
        return False
    else: 
        return True

#Main Function
def dataset_processing(audio_paths, output_path, nb_of_frames, BATCHSIZE, maxfiles=-1):
    """This function take the audio path of the dataset and outputs a 
    of Mel Spectrograms. The shape is (Batch_size, nb of frames, 128, 1)

    Args:
        audio_paths (string): the path of the audio folder we want to process
        output_path (string): the path where to save the dataset
        BATCHSIZE (int, optional): The batch size. Defaults to 32.
        nb_of_frames (int, optional): The number of frames that the mel Spectrograms
        will have.

    Returns:
        PrefetchDataset: Returns the training and testing datasets.
    """
    #We Work in the directory where the audio are
    command = (audio_paths)
    os.chdir(command)
    print(os.getcwd())

    # load mp3 files
    files = [f for f in os.listdir(audio_paths) if f[-3:] in ['mp3']]
    
    # filter files that cannot be loaded
    # incompatible_file_filter=['2014_Stenz_Mahler_IX-1.mp3']
    files = [f for f in files if is_compatible_mp3(f)]

    #files = files[:BATCHSIZE]
    #print('Only loading one batch for debugging: ', files)
    if maxfiles > 0 and len(files) > maxfiles:
        print('Reducing number of files from %d to %d (see maxfiles parameter)' % (len(files), maxfiles))
        files = random.sample(files, maxfiles)
        
    print('Final file list: ', files)

    #Loading the audio from the paths
    ds = paths_to_dataset(files)
    print('file dataset cardinality: ', tf.data.experimental.cardinality(ds))

    #Transforming the audios in Spectrograms
    ds = ds.map(
        lambda x: audio_to_spectrograms(x), num_parallel_calls=AUTOTUNE
    )
    print('specgram dataset cardinality: ', tf.data.experimental.cardinality(ds))

    #Transforming the Spectrograms into Mel Spectrograms
    ds = ds.map(
        lambda x: spectrograms_to_melspectrograms(x), num_parallel_calls=AUTOTUNE
    )
    print('melscec dataset cardinality: ', tf.data.experimental.cardinality(ds))

    #Normalizing the Mel Spectrograms Tensor 
    ds = ds.map(
        lambda x: normalize_spectrograms(x), num_parallel_calls=AUTOTUNE
    )
    print('norm dataset cardinality: ', tf.data.experimental.cardinality(ds))


    #We split each element of the dataset into a dataset into dataset of 
    #size (Batch_size, nb of frames, 128, 1)
    splitted_mel_spectrograms_ds = []
    for elem in ds:
        elem_ds = splitting_spectrograms(elem,nb_of_frames).batch(batch_size = BATCHSIZE)
        print('splitting dataset cardinality: ', tf.data.experimental.cardinality(elem_ds))
        splitted_mel_spectrograms_ds.append(elem_ds)

    #We now concatenate all the "small" dataset 

    ds = splitted_mel_spectrograms_ds[0]

    for i in range(1,len(splitted_mel_spectrograms_ds)):
        ds = ds.concatenate(splitted_mel_spectrograms_ds[i])
        print('concatenated growing dataset cardinality: ', tf.data.experimental.cardinality(ds))

    #We Save the Dataset 
    print('final dataset cardinality: ', tf.data.experimental.cardinality(ds))
    tf.data.experimental.save(ds, output_path)
    print("Dataset saved in: ", output_path)

    return ds 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process the raw audio to create a dataset.')

    parser.add_argument('--audio_path', type=str, 
                            help='Path of the dataset of the audios')
    parser.add_argument('--output_path', type=str, 
                            help='Path where the dataset is saved')
    parser.add_argument('--nb_of_frames', type=int, default=128 ,
                            help='Number of frames the Mel spectrograms will have, default 128')
    parser.add_argument('--batchsize', type=int, default=10,
                            help='batch size, default 10')
    parser.add_argument('--maxfiles', type=int, default=-1,
                            help='maximum number of files to process, default -1')

    args = parser.parse_args()

    dataset_processing(args.audio_path, args.output_path, nb_of_frames= args.nb_of_frames,
                             BATCHSIZE= args.batchsize, maxfiles= args.maxfiles)

