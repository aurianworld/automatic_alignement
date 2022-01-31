#!/usr/bin/env python3

from curses import def_shell_mode
import os
import subprocess
import argparse
import tensorflow as tf
from keras.models import Model
from keras import layers
from autoencoder_model import autoencoder_model



def training_pipeline(dataset_path, model_output_path, SPLIT = 0.7): 

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

    train_dataset = ds.take(int(0.7*Datasetsize)) 
    test_dataset = ds.skip(int(0.7*Datasetsize))

    autoencoder, encoder = autoencoder_model(layers.Input(shape=(None,128,1),  name='encoder_inputs'))



    git_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("ascii").strip()