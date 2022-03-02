#! /bin/bash

set -x
# this is the install file for MsMrDTW_for_SonicVisualiser 
# it should 
# 1. detect where this folder lives and save that in $MY_NAME
# -> this should be $0 
MY_NAME=$0
echo $MY_NAME

MY_DIRECTORY=$(dirname $MY_NAME)
MY_ROOT=$(id -un)
echo $MY_ROOT
echo $MY_DIRECTORY

# 2. replace [YOUR_PATH] in various files 
cp -f "${MY_DIRECTORY}"/MrMsDTW_for_sv_bash.sh_ "${MY_DIRECTORY}"/MrMsDTW_for_sv_bash.sh

#MY_DIRECTORY_SED=$(echo "${MY_DIRECTORY}" | sed -e 's/\/\_[]$.*[\^]/\\&/g' )
#echo sed -i "s/\[YOUR\_PATH\]/${MY_DIRECTORY_SED}/g" MrMsDTW_for_sv_bash.sh
echo sed -i "s|[YOUR_PATH]|${MY_DIRECTORY}|" "${MY_DIRECTORY}"/MrMsDTW_for_sv_bash.sh
sed -i 's|\[YOUR_PATH\]|'${MY_DIRECTORY}'|g' "${MY_DIRECTORY}"/MrMsDTW_for_sv_bash.sh

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
sed -i 's|\[YOUR_ROOT\]|/home/'${MY_ROOT}'|g' "${MY_DIRECTORY}"/MrMsDTW_for_sv_bash.sh #FOR LINUX
elif [[ "$OSTYPE" == "darwin"* ]]; then
sed -i 's|\[YOUR_ROOT\]|/Users/'${MY_ROOT}'|g' "${MY_DIRECTORY}"/MrMsDTW_for_sv_bash.sh #FOR LINUX
fi


# 3. edit sonic visualiser config file
SV_CONFIG="/home/"$MY_ROOT"/.config/sonic-visualiser/Sonic Visualiser.conf" #FOR LINUX
# SV_CONFIG="/Users/"$MY_ROOT"/.config/sonic-visualiser/Sonic Visualiser.conf" #FOR MAC

sed -i "/\[Alignment\]/d" "${SV_CONFIG}"
sed -i "/alignment\-program/d" "${SV_CONFIG}"
sed -i "/alignment\-type/d" "${SV_CONFIG}"
echo '[Alignment]
alignment-program='"${MY_DIRECTORY}"'/MrMsDTW_for_sv_bash.sh
alignment-type=external-program-alignment' >> "${SV_CONFIG}"

# 4. install anaconda
source "/home/"$MY_ROOT"/miniconda3/etc/profile.d/conda.sh"
# source "/Users/"$MY_ROOT"/miniconda3/etc/profile.d/conda.sh" #FOR MAC
conda create -n mrmsdtw2 python=3.7 

# 5. install requirements 
conda deactivate
conda config --set auto_activate_base false # stop base environment from automatic load
conda activate mrmsdtw2
pip install -r ${MY_DIRECTORY}/requirements.txt


# 6. chmod the align shell file to be executable
chmod +x ""${MY_DIRECTORY}"/mrmsdtw_for_sv.py"
chmod +x ""${MY_DIRECTORY}"/MrMsDTW_for_sv_bash.sh"