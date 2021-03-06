#!/usr/bin/env python3

import os
import subprocess
import argparse
import tensorflow as tf
from tensorflow.keras import layers
from autoencoder_model import autoencoder_model



def training_pipeline(dataset_path, model_output_path, SPLIT = 0.7, epochs = 100): 
    """Training function that loads the model and the dataset. Train the model and save it.

    Args:
        dataset_path (string): the path where the dataset is saved 
        model_output_path (string): Directory where we want to save the model and the checkpoints
        SPLIT (float, optional): The splitting factor between the training and testing data. Defaults to 0.7.
        epochs (int, optional): Number of epochs to run the model. Defaults to 100.
    """

    # get the git hash before changing the directory
    # note: we really should avoid changing the directory    
    git_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], shell=False).decode("ascii").strip()


    #We Work in the directory of the dataset
    command = (dataset_path)
    os.chdir(command)

    #We load the dataset 
    ds = tf.data.experimental.load(dataset_path)

    #We zip the dataset to have (x,y) for inputs and outputs
    ds = tf.data.Dataset.zip((ds,ds))


    #We split the dataset into training and testing
    #First we shuffle the Dataset 
    ds = ds.shuffle(buffer_size = 32 * 32)

    #We Split it
    Datasetsize = (tf.data.experimental.cardinality(ds).numpy())
    train_dataset = ds.take(int(SPLIT*Datasetsize)) 
    test_dataset = ds.skip(int(SPLIT*Datasetsize))

    #We load our model
    autoencoder, encoder = autoencoder_model(layers.Input(shape=(None,128,1),  name='encoder_inputs'))
    autoencoder.compile(optimizer="adam", loss="binary_crossentropy")

    #We preparee callbacks
    checkpoint_path = model_output_path + 'model_'+git_hash+'{epoch:02d}_{binary_crossentropy:.4f}_{val_binary_crossentropy:.4f}.h5'
    
    autoencoder.fit(train_dataset, epochs = epochs, validation_data=test_dataset,
                                callbacks = [tf.keras.callbacks.ModelCheckpoint(checkpoint_path, verbose=1, save_best_only=False, save_weights_only=False, mode='max')])

    encoder.save(model_output_path+'encoder_model')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load a model and a dataset to train the model.')

    parser.add_argument('--dataset_path', type=str, 
                            help='Path of the processed dataset')
    parser.add_argument('--model_output_path', type=str, 
                            help='Path where the model is saved')
    parser.add_argument('--split', type=float, default=0.7,
                            help='Splitting factor between training and testing')
    parser.add_argument('--epochs', type=int, default=100,
                            help='Number of epochs to train the model')

    args = parser.parse_args()
    training_pipeline(args.dataset_path, args.model_output_path, SPLIT = args.split, epochs = args.epochs)
