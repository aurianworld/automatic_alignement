#!/bin/bash

#Making sure that we are using the good environement 
#conda init bash

source '/home/osboxes/miniconda3/etc/profile.d/conda.sh'
conda activate mrmsdtw

/home/osboxes/automatic_alignement/MsMrDTW_forSonicVisualiser/mrmsdtw_for_sv.py --audio_1 $1 --audio_2 $2 --config_path "/home/osboxes/automatic_alignement/MsMrDTW_for_SonicVisualizer/MrMsDTW_config.conf"