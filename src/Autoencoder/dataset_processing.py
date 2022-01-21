import os
import argparse
import tensorflow as tf
import tensorflow_io as tfio

#Parameters 
VALID_SPLIT = 0.2
BATCHSIZE = 56


#Specify the folder with the audio to process 
audio_paths = '/osboxes/Desktop/Dataset/01_Audio/01_Full_Symphonies'

#Useful functions 
def path_to_audio(path):
    """Reads and decodes an audio file."""
    audio = tf.io.read_file(path)
    audio, _ = tf.audio.decode_wav(audio,2, -1)
    # audio = tfio.audio.decode_mp3(audio)
    print(audio.shape)
    return audio

def paths_to_dataset(audio_paths):
    """Constructs a dataset of audios"""
    path_ds = tf.data.Dataset.from_tensor_slices(audio_paths)
    audio_ds = path_ds.map(lambda x: path_to_audio(x))
    audio_ds = audio_ds.map(lambda x: tf.math.divide(
        tf.reduce_sum(x,axis=1,keepdims=True),
        tf.constant([2.])))
    return audio_ds

def audio_to_spectrograms(audio):
    """Compute the spectrogram of an audio tensor"""
    print(audio.shape)
    audio = tf.squeeze(audio, axis=-1)
    
    spectrogram = tfio.audio.spectrogram(audio, nfft=256, window=256, stride=128)
    print(spectrogram.shape)
    spectrogram = tf.expand_dims(spectrogram, axis=-1)
    print(spectrogram.shape)

    return spectrogram


#Main Function
def dataset_processing(audio_paths, VALID_SPLIT=0.1, BATCHSIZE=10):
    """This function take the audio path of the dataset and outputs a training
        and testing dataset of Spectrograms. The shape is (Batch_size, spectrogram_length, 129, 1)

    Args:
        audio_paths (string): the path of the audio folder we want to process
        VALID_SPLIT (float, optional): The pourcentage of samples to use for testing. Defaults to 0.1.
        BATCHSIZE (int, optional): The batch size. Defaults to 10.

    Returns:
        PrefetchDataset: Returns the training and testing datasets.
    """
    #Split into training and testing set
    num_val_samples = int(VALID_SPLIT * len(audio_paths))
    print("Using {} files for training.".format(len(audio_paths) - num_val_samples))
    train_audio_paths = audio_paths[:-num_val_samples]

    print("Using {} files for testing.".format(num_val_samples))
    test_audio_paths = audio_paths[-num_val_samples:]

    #Create to Dataset, one for training and one for testing
    train_ds = paths_to_dataset(train_audio_paths)
    train_ds = train_ds.shuffle(buffer_size=32 * 8, seed=4).batch(BATCHSIZE)

    testing_ds = paths_to_dataset(test_audio_paths)
    testing_ds = testing_ds.shuffle(buffer_size=32*8, seed=4).batch(BATCHSIZE)

    #Converting the audio wave into spectrograms 
    train_ds = train_ds.map(
        lambda x: audio_to_spectrograms(x), num_parallel_calls=tf.data.AUTOTUNE
        )

    testing_ds = train_ds.map(
        lambda x: audio_to_spectrograms(x), num_parallel_calls=tf.data.AUTOTUNE
        )

    #Adding the input as the expected output 

    train_ds = tf.data.Dataset.zip((train_ds,train_ds))
    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)

    testing_ds = tf.data.Dataset.zip((testing_ds,testing_ds))
    testing_ds = testing_ds.prefetch(tf.data.AUTOTUNE)
    return train_ds, testing_ds 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align to audio files.')

    parser.add_argument('--audio_path', type=str, 
                            help='Path of the dataset of the audios')
    parser.add_argument('--validsplit', type=float, 
                            help='pourcentage of samples for testing, default 0.1')
    parser.add_argument('--batchsize', type=int, 
                            help='batch size, default 10')

    args = parser.parse_args()
    dataset_processing(args.audio_path, args.validsplit, args.batchsize)