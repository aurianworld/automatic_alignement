#!/usr/bin/env python3

import pandas as pd
import argparse
import numpy as np
import scipy

from synctoolbox.dtw.utils import evaluate_synchronized_positions
from synctoolbox.dtw.utils import make_path_strictly_monotonic


def evaluate_alignment(wp_file,annotation_ref,annotation_align):
    header_name = ['time','beat']

    wp = np.genfromtxt(wp_file, delimiter=',').T
    wp = make_path_strictly_monotonic(wp)

    print(wp[0][-1])

    #GET THE ANNOTATION PATH FROM AUDIO PATH -> TODO    
    beat_annotations_ref = pd.read_csv(filepath_or_buffer=annotation_ref, names = header_name).reset_index(drop = True)
    beat_annotations_align = pd.read_csv(filepath_or_buffer=annotation_align, names = header_name).reset_index(drop = True)
    #beat_annotations_align = beat_annotations_align.loc[beat_annotations_align['beat'].isin(beat_annotations_ref['beat'])].reset_index(drop = True) #We make sure that we compare only the same beats 

    beat_positions_ref_transferred_to_align = scipy.interpolate.interp1d(wp[1] , wp[0], bounds_error=False, fill_value=[0.], kind='linear')(beat_annotations_ref["time"])
    
    print(wp[0][:5])

    mean_absolute_error, accuracy_at_tolerances = evaluate_synchronized_positions(beat_annotations_align["time"] * 1000, beat_positions_ref_transferred_to_align * 1000)


    #ADD THE WARPING PATH IN GOOD FILE -> TODO
    beat_position_transfered_ref_to_align = pd.DataFrame(data = beat_positions_ref_transferred_to_align, columns = ["time"])
    beat_position_transfered_ref_to_align["beat"] = beat_annotations_ref["beat"]
    
    beat_position_transfered_ref_to_align.to_csv('/home/osboxes/Desktop/Dataset/06_Transfered_Annotation/01_MATCH/2003-1965_147.1_210.1.csv', header = False, index = False)

    return mean_absolute_error, accuracy_at_tolerances



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--wp_file', type=str, 
                            help='Path of the alignement file csv or txt')
    parser.add_argument('--annotation_ref', type=str, 
                            help='Path of the annotation file of the ref csv or txt')
    parser.add_argument('--annotation_align', type=str, 
                            help='Path of the annotation file of the align csv or txt')

    args = parser.parse_args()
    print(args.wp_file, args.annotation_ref, args.annotation_align)
    evaluate_alignment(args.wp_file, args.annotation_ref, args.annotation_align)