import os
import tensorflow as tf
import tensorflow_io as tfio

#Parameters 
VALID_SPLIT = 0.2
BATCHSIZE = 10


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
    