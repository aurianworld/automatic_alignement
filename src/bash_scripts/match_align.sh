#!/bin/bash
#This is a script that does the match alignment from two audio file. First one passed is the reference. Second one passed is the one we align.

source '/home/osboxes/miniconda3/etc/profile.d/conda.sh'
conda activate sdia-python
#@Echo off
# Audio File Request 

AUDIOREF=$1
AUDIOALIGN=$2

# tuning
# sonic-annotator -l | grep tune

echo configuring tuning differences
sonic-annotator -s vamp:tuning-difference:tuning-difference:cents > /home/osboxes/automatic_alignement/config_files/Match_alignment/tuning-difference-transform.ttl
# sonic-annotator -t tuning-difference-transform.ttl --multiplex --writer csv --csv-force  2003_Gielen_Mahler_IX-1_s147.1_e210.1.wav 1965_Bernstein_Mahler_IX-1_s147.1_e210.1.wav #~/Downloads/glitch_example_shorter.wav ~/Downloads/dw_f2_demo_audio_cut_click_16.413_pitched.wav

# to get the frequency directly

echo computing the tuning frequency
#FREQ2=$(sonic-annotator -t /home/osboxes/automatic_alignement/config_files/Match_alignment/tuning-difference-transform.ttl --multiplex --writer csv --csv-force $AUDIOALIGN $AUDIOREF  2>&1 | grep "channel 1: overall best Hz = " | grep -o -P '[0-9]+.[0-9]+')
#echo tuning frequency is $FREQ2
#PLINE=$(cat match-transform.ttl | grep -n freq2 | cut -d : -f 1 | awk '{print $0+1}')

echo The frequency will be inserted into the line: $PLINE

# Creating Match-transform TTL
# sonic-annotator -s vamp:match-vamp-plugin:match:path > /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform.ttl # get transform skeleton
# use SED to exchange match-transform frequency in PLINE+1 into match-transform_modified.ttl
#cat match-transform.ttl | sed  "${PLINE}s/        vamp\:value \"440\"\^\^xsd\:float \;/        vamp\:value \"${FREQ2}\"\^\^xsd\:float \;/" > /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform_modified.ttl

# alignment
# sonic-annotator -l | grep match # check if match is installed and what outputs

echo computing the warping path

sonic-annotator -t /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform.ttl --multiplex --writer csv --csv-force  $AUDIOREF $AUDIOALIGN
# find output in: ~/Downloads/glitch_example_shorter_vamp_match-vamp-plugin_match_path.csv


echo running the evaluation of the warpping path with python
/home/osboxes/automatic_alignement/src/python_bash_code/evaluate_alignment.py --wp_file '/home/osboxes/Desktop/Dataset/01_Audio/02_Cropped_Symphonies/2003_Gielen_Mahler_IX-1_s147.1_e210.1_vamp_match-vamp-plugin_match_path.csv' --annotation_ref '/home/osboxes/automatic_alignement/data_sync_experiment/2003_Gielen_Mahler_IX-1_bpb_CU_final_updated_22-11-2021_s147.1_e210.1.csv' --annotation_align '/home/osboxes/automatic_alignement/data_sync_experiment/1965_Bernstein_Mahler_IX-1_bpb_147-329_s147.1_e210.1.csv'
