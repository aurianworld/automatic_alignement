#!/bin/bash

echo $1 > param1.txt
echo $2 > parma2.txt

#Making sure that we are using the good environement 
conda activate sdia-python

/home/osboxes/automatic_alignement/Code/audio_alignment_sv.py --audio_1 $1 --audio_2 $2 --config_path "/home/osboxes/automatic_alignement/config_audio_alignment_sv.conf"

#output of the alignement
cat "/home/osboxes/automatic_alignement/Code/wp2.csv" 