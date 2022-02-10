#!/usr/bin/env python3
from tensorflow.keras.models import load_model






if __name__ == '__main__':
    encoder = load_model('/home/osboxes/Desktop/Test_dataset/Autoencoder_model')
    print(encoder.summary())