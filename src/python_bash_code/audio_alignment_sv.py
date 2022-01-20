#!/usr/bin/env python3

import argparse
import configparser
import librosa
import numpy as np 
import scipy
import pandas as pd

from synctoolbox.feature.utils import estimate_tuning
from synctoolbox.feature.pitch_onset import audio_to_pitch_onset_features
from synctoolbox.feature.dlnco import pitch_onset_features_to_DLNCO
from synctoolbox.feature.pitch import audio_to_pitch_features
from synctoolbox.feature.chroma import pitch_to_chroma, quantize_chroma
from synctoolbox.feature.chroma import quantized_chroma_to_CENS
from synctoolbox.dtw.utils import compute_optimal_chroma_shift, shift_chroma_vectors, evaluate_synchronized_positions
from synctoolbox.dtw.mrmsdtw import sync_via_mrmsdtw
from synctoolbox.dtw.utils import make_path_strictly_monotonic


def audio_alignment_sv(audio_1_path, audio_2_path, config_path): 
    """The audio_alignement_sv function will be used by sonic visualiser to perform an alignement between two audio files.


    Args:
        audio_1_path (string): the reference audio's file path.
        audio_2_path (string): the audio's file path of the audio to align with the reference
        config_path (string): file path of the config file containing parameters for the alignment (Numbers of features per second, algorithm type)
    """

    #Reading the arguments in the config file
    config = configparser.ConfigParser()
    config.read(config_path)

    #Parameters of the DTW
    Fs = config.getint("config","Fs") #Sample Rate
    save_warping_path = config.getboolean("config","save_warping_path") #Flag to know if we export the warping path or not
    feature_rate = config.getint("config", "feature_rate") #Number of features per seconds in the output representation
    strictly_monotonic = config.getboolean("config","strictly_monotonic") #Flag to know if we output the warping path strictly monotonic or not
    output_wp = config.get("config", "output_wp") #output path of the warping path
    step_weights = np.array([1.5, 1.5, 2.0]) #DTW step weights
    threshold_rec = 10 ** 6 #Defines the maximum area that is spanned by the rectangle of two consecutive elements in the alignment 
    result = config.getint("config","result") #Flag to compute the results of the alignement


    #Loading the audio
    audio_1, _ = librosa.load(audio_1_path, Fs)
    audio_2, _ = librosa.load(audio_2_path, Fs)

    #Getting the tuning deviation between the two audio 
    tuning_offset_1 = estimate_tuning(audio_1, Fs)
    tuning_offset_2 = estimate_tuning(audio_2, Fs)

    #Computing the Chroma and DLNCO (Decaying locally adaptive normalized chroma onset) for both audio
    f_chroma_quantized_1, f_DLNCO_1 = get_features_from_audio(audio_1, tuning_offset_1, Fs, feature_rate)
    f_chroma_quantized_2, f_DLNCO_2 = get_features_from_audio(audio_2, tuning_offset_2, Fs, feature_rate)

    #Shifting the Chroma to minimize the DTW cost
    f_cens_1hz_1 = quantized_chroma_to_CENS(f_chroma_quantized_1, 201, 50, feature_rate)[0] #Chroma energy normalized statistics features
    f_cens_1hz_2 = quantized_chroma_to_CENS(f_chroma_quantized_2, 201, 50, feature_rate)[0]
    opt_chroma_shift = compute_optimal_chroma_shift(f_cens_1hz_1, f_cens_1hz_2)

    f_chroma_quantized_2 = shift_chroma_vectors(f_chroma_quantized_2, opt_chroma_shift)
    f_DLNCO_2 = shift_chroma_vectors(f_DLNCO_2, opt_chroma_shift)


    #Computing the warping path 

    wp = sync_via_mrmsdtw(f_chroma1=f_chroma_quantized_1, f_onset1=f_DLNCO_1, f_chroma2=f_chroma_quantized_2, f_onset2=f_DLNCO_2, input_feature_rate=feature_rate, step_weights=step_weights, threshold_rec=threshold_rec)

    if strictly_monotonic :
        wp = make_path_strictly_monotonic(wp)

    if save_warping_path:
        np.savetxt(output_wp+".csv", wp.T/feature_rate,fmt = '%.5f',delimiter = ',')


    for _, pair in enumerate(wp.T/feature_rate):
            print(tuple(pair)[0],',',tuple(pair)[1])


    #Computing the MAE and Standard deviation to evaluate the alignment 

    if result : 
        header_name = ["time","beat"]


        #DEFINE FILE_PATH_REF and FILE_PATH_ALIGN FROM the audio path TODO 
        beat_annotations_ref = pd.read_csv(filepath_or_buffer=file_path_ref+"_s"+str(beat_start)+"_e"+str(beat_stop)+".csv",names = header_name)
        beat_annotations_align = pd.read_csv(filepath_or_buffer=file_path_align+"_s"+str(beat_start)+"_e"+str(beat_stop)+".csv", names = header_name)
        beat_annotations_align = beat_annotations_align.loc[beat_annotations_align['beat'].isin(beat_annotations_ref['beat'])].reset_index(drop = True) #We make sure that we compare only the same beats 


        beat_positions_ref_transferred_to_align = scipy.interpolate.interp1d(wp2[0]/ feature_rate , wp2[1]/ feature_rate , kind='linear')(beat_annotations_ref["time"])
        mean_absolute_error, accuracy_at_tolerances = evaluate_synchronized_positions(beat_annotations_align["time"] * 1000, beat_positions_ref_transferred_to_align * 1000)



#Function to compute the Chroma and DLNCO 
def get_features_from_audio(audio, tuning_offset, Fs, feature_rate):
    f_pitch = audio_to_pitch_features(f_audio=audio, Fs=Fs, tuning_offset=tuning_offset, feature_rate=feature_rate)
    f_chroma = pitch_to_chroma(f_pitch=f_pitch)
    f_chroma_quantized = quantize_chroma(f_chroma=f_chroma)

    f_pitch_onset = audio_to_pitch_onset_features(f_audio=audio, Fs=Fs, tuning_offset=tuning_offset) #Tuning offset is used to shift the filterbank that detects the pith onset
    f_DLNCO = pitch_onset_features_to_DLNCO(f_peaks=f_pitch_onset, feature_rate=feature_rate, feature_sequence_length=f_chroma_quantized.shape[1])
    return f_chroma_quantized, f_DLNCO




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align to audio files.')

    parser.add_argument('--audio_1', type=str, 
                            help='Path of the audio 1')

    parser.add_argument('--audio_2', type=str, 
                            help='Path of the audio 2')

    parser.add_argument('--config_path', type=str, 
                            help='Path of the config file')

    
    args = parser.parse_args()
    audio_alignment_sv(args.audio_1, args.audio_2, args.config_path)