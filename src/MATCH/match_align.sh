#!/bin/bash
#This is a script that does the match alignment from two audio file. First one passed is the reference. Second one passed is the one we align.

source '/home/osboxes/miniconda3/etc/profile.d/conda.sh'
conda activate sdia-python
#@Echo off
# Audio File Request 

AUDIOREF=$1
AUDIOALIGN=$2

# Creating the TTL files
# Creating Tuning-difference TTL
sonic-annotator -s vamp:tuning-difference:tuning-difference:cents > /home/osboxes/automatic_alignement/config_files/Match_alignment/tuning-difference-transform.ttl
# Creating Match-transform TTL. ONLY IF NOT CREATED BEFORE. match-transform_modified.ttl TTL has the same parameter as in Sonic Visualiser
# sonic-annotator -s vamp:match-vamp-plugin:match:path > /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform.ttl 


# Getting the frequency difference and storing it into the Match TTL files.
echo computing the tuning frequency
FREQ2=$(sonic-annotator -t /home/osboxes/automatic_alignement/config_files/Match_alignment/tuning-difference-transform.ttl --multiplex --writer csv --csv-basedir /home/osboxes/Desktop/Unwanted --csv-force $AUDIOALIGN $AUDIOREF  2>&1 | grep "channel 1: overall best Hz = " | grep -o -P '[0-9]+.[0-9]+')
echo tuning frequency is $FREQ2
PLINE=$(cat /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform.ttl | grep -n freq2 | cut -d : -f 1 | awk '{print $0+1}')

echo The frequency will be inserted into the line: $PLINE

# Using SED to exchange match-transform frequency in PLINE+1 into match-transform_modified.ttl
cat /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform.ttl | sed  "${PLINE}s/        vamp\:value \"440\"\^\^xsd\:float \;/        vamp\:value \"${FREQ2}\"\^\^xsd\:float \;/" > /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform_modified.ttl



# alignment
echo computing the warping path

sonic-annotator -t /home/osboxes/automatic_alignement/config_files/Match_alignment/match-transform_modified.ttl --multiplex --writer csv --csv-basedir /home/osboxes/Desktop/Dataset/05_Warping_path/01_MATCH/ --csv-force $AUDIOREF $AUDIOALIGN 
# find output in working directory

#Evaluating the WP 
echo running the evaluation of the warpping path with python
/home/osboxes/automatic_alignement/src/Utilities/evaluate_alignment.py --wp_file '/home/osboxes/Desktop/Dataset/05_Warping_path/01_MATCH/2003_Gielen_Mahler_IX-1_s147.1_e210.1_vamp_match-vamp-plugin_match_path.csv' --annotation_ref '/home/osboxes/automatic_alignement/data_sync_experiment/2003_Gielen_Mahler_IX-1_bpb_CU_final_updated_22-11-2021_s147.1_e210.1.csv' --annotation_align  '/home/osboxes/automatic_alignement/data_sync_experiment/1965_Bernstein_Mahler_IX-1_bpb_147-329_s147.1_e210.1.csv' 


#TO DO create automatic script to find the WP and the ground truth annotations directly from the name of the audio files