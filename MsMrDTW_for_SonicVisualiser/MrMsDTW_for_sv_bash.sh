#!/bin/bash

#Making sure that we are using the good environement 
#conda init bash

source '/home/osboxes/miniconda3/etc/profile.d/conda.sh'
conda activate mrmsdtw

[YOUR_PATH]/MsMrDTW_for_SonicVisualiser/mrmsdtw_for_sv.py --audio_1 $1 --audio_2 $2 --config_path "[YOUR_PATH]/MsMrDTW_for_SonicVisualiser/MrMsDTW_config.conf"