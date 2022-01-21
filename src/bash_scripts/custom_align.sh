#!/bin/bash

#Making sure that we are using the good environement 
#conda init bash

source '/home/osboxes/miniconda3/etc/profile.d/conda.sh'
conda activate sdia-python


/home/osboxes/automatic_alignement/src/audio_alignment_sv.py --audio_1 $1 --audio_2 $2 --config_path "/home/osboxes/automatic_alignement/config_files/sonic_visualiser/config_audio_alignment_sv.conf"