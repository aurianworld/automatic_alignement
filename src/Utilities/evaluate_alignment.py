#!/usr/bin/env python3

import pandas as pd
import argparse
import numpy as np
import scipy

from synctoolbox.dtw.utils import evaluate_synchronized_positions
from synctoolbox.dtw.utils import make_path_strictly_monotonic
from annotation_path_from_audio_path import annotation_from_audio


def evaluate_alignment(wp_file,audio_path_ref,audio_path_align):
    header_name = ['time','beat']

    wp = np.genfromtxt(wp_file, delimiter=',').T
    wp = make_path_strictly_monotonic(wp)


    #GET THE ANNOTATION PATH FROM AUDIO PATH    
    beat_annotations_ref = pd.read_csv(filepath_or_buffer=annotation_from_audio(audio_path_ref), names = header_name).reset_index(drop = True)
    beat_annotations_align = pd.read_csv(filepath_or_buffer=annotation_from_audio(audio_path_align), names = header_name).reset_index(drop = True)
    # beat_annotations_align = beat_annotations_align.loc[beat_annotations_align['beat'].isin(beat_annotations_ref['beat'])].reset_index(drop = True)

    beat_positions_ref_transferred_to_align = scipy.interpolate.interp1d(wp[1] , wp[0], bounds_error=False, fill_value=[0.], kind='linear')(beat_annotations_ref["time"])
    

    mean_absolute_error, accuracy_at_tolerances = evaluate_synchronized_positions(beat_annotations_align["time"][:-1] * 1000, beat_positions_ref_transferred_to_align[:-1] * 1000)


    beat_position_transfered_ref_to_align = pd.DataFrame(data = beat_positions_ref_transferred_to_align, columns = ["time"])
    beat_position_transfered_ref_to_align["beat"] = beat_annotations_ref["beat"]
    
    beat_position_transfered_ref_to_align.to_csv('/home/osboxes/Desktop/Dataset/06_Transfered_Annotation/01_MATCH/2003-1965_147.1_210.1.csv', header = False, index = False)

    return mean_absolute_error, accuracy_at_tolerances



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--wp_file', type=str, 
                            help='Path of the alignement file csv or txt')
    parser.add_argument('--audio_path_ref', type=str, 
                            help='Path of the reference audio ')
    parser.add_argument('--audio_path_align', type=str, 
                            help='Path of the audio to align')

    args = parser.parse_args()
    print(args.wp_file, args.audio_path_ref, args.audio_path_align)
    evaluate_alignment(args.wp_file, args.audio_path_ref, args.audio_path_align)