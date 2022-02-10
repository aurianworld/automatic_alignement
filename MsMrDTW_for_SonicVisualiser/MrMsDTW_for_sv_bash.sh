#!/bin/bash

#Making sure that we are using the good environement 
#conda init bash

source '~/miniconda3/etc/profile.d/conda.sh'
<<<<<<< HEAD
conda activate mrmsdtw

/home/osboxes/automatic_alignement/MsMrDTW_for_SonicVisualiser/mrmsdtw_for_sv.py --audio_1 $1 --audio_2 $2 --config_path "/home/osboxes/automatic_alignement/MsMrDTW_for_SonicVisualiser/MrMsDTW_config.conf"
=======
conda deactivate
conda activate mrmsdtw

python3 [YOUR_PATH]/MsMrDTW_for_SonicVisualiser/mrmsdtw_for_sv.py --audio_1 $1 --audio_2 $2 --config_path "[YOUR_PATH]/MsMrDTW_for_SonicVisualiser/MrMsDTW_config.conf"
>>>>>>> 24e5ee8b6e3ce5d03a9dee7561b11e0aefd4aefc
