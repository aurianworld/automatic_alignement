#!/usr/bin/env python3

import os
import subprocess
import argparse
import tensorflow as tf
from keras.models import Model
from keras import layers
from autoencoder_model import autoencoder_model



def training_pipeline(dataset_path, model_output_path, SPLIT = 0.7, epochs = 100): 
    """Training function that loads the model and the dataset. Train the model and save it.

    Args:
        dataset_path (string): the path where the dataset is saved 
        model_output_path (string): Directory where we want to save the model and the checkpoints
        SPLIT (float, optional): The splitting factor between the training and testing data. Defaults to 0.7.
        epochs (int, optional): Number of epochs to run the model. Defaults to 100.
    """

    #We Work in the directory where the audio are
    command = (dataset_path)
    os.chdir(command)

    #We load the dataset 
    ds = tf.data.experimental.load(dataset_path)

    #We zip the dataset to have (x,y) for inputs and outputs
    ds = tf.data.Dataset.zip((ds,ds))


    #We split the dataset into training and testing
    #First we shuffle the Dataset 
    ds = ds.shuffle()
    Datasetsize = (tf.data.experimental.cardinality(ds).numpy())

    train_dataset = ds.take(int(SPLIT*Datasetsize)) 
    test_dataset = ds.skip(int(SPLIT*Datasetsize))


    #We load our model
    autoencoder, encoder = autoencoder_model(layers.Input(shape=(None,128,1),  name='encoder_inputs'))
    autoencoder.compile(optimizer="adam", loss="binary_crossentropy")

    #We preparee callbacks
    git_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("ascii").strip()
    checkpoint_path = model_output_path + 'model_'+git_hash+'.h5' 
    
    autoencoder.fit(train_dataset, epochs = epochs, validation_data=test_dataset,
                                callbacks = [tf.keras.callbacks.ModelCheckpoint(checkpoint_path, verbose=1, save_best_only=False, save_weights_only=False, mode='max')])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load a model and a dataset to train the model.')

    parser.add_argument('--dataset_path', type=str, 
                            help='Path of the processed dataset')
    parser.add_argument('--model_output_path', type=str, 
                            help='Path where the model is saved')
    parser.add_argument('--split', type=float, 
                            help='Splitting factor between training and testing')
    parser.add_argument('--epochs', type=int, 
                            help='Number of epochs to train the model')

    args = parser.parse_args()

    if args.split == None and args.epochs == None:
        training_pipeline(args.dataset_path, args.model_output_path)
    
    if args.split == None and args.epochs != None:
        training_pipeline(args.dataset_path, args.model_output_path, epochs = args.epochs)

    if args.split != None and args.epochs == None:
        training_pipeline(args.dataset_path, args.model_output_path, SPLIT = args.split)

    if args.split != None and args.epochs != None:
        training_pipeline(args.dataset_path, args.model_output_path, SPLIT = args.split, epochs = args.epochs)