import pandas as pd
import argparse
import numpy as np
import scipy

from synctoolbox.dtw.utils import evaluate_synchronized_positions


def evaluate_alignment(alignment_file,annotation_ref,annotation_align):
    header_name = ['time','beat']

    wp = np.genfromtxt(alignment_file, delimiter=',')

    beat_annotations_ref = pd.read_csv(filepath_or_buffer=annotation_ref, names = header_name)
    beat_annotations_align = pd.read_csv(filepath_or_buffer=annotation_align, names = header_name)
    beat_annotations_align = beat_annotations_align.loc[beat_annotations_align['beat'].isin(beat_annotations_ref['beat'])].reset_index(drop = True) #We make sure that we compare only the same beats 


    beat_positions_ref_transferred_to_align = scipy.interpolate.interp1d(wp[0] , wp[1], kind='linear')(beat_annotations_ref["time"])


    mean_absolute_error, accuracy_at_tolerances = evaluate_synchronized_positions(beat_annotations_align["time"] * 1000, beat_positions_ref_transferred_to_align * 1000)

    return mean_absolute_error, accuracy_at_tolerances



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--alignment_file', type=str, 
                            help='Path of the alignement file csv or txt')
    parser.add_argument('--annotation_ref', type=str, 
                            help='Path of the annotation file of the ref csv or txt')
    parser.add_argument('--annotation_align', type=str, 
                            help='Path of the annotation file of the align csv or txt')

    args = parser.parse_args()
    print(args.alignment_file, args.annotation_ref, args.annotation_align)
    evaluate_alignment(args.alignment_file, args.annotation_ref, args.annotation_align)