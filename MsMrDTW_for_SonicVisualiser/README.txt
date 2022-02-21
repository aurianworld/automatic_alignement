[Here are the steps to setup the new alignment in Sonic Visualiser]

[First - Install Miniconda]
In the folder MsMrDTW_for_SonicVisualizer execute "MsMrDTW_for_SonicVisualiser/Miniconda3-py37_4.10.3-MacOSX-x86_64.pkg" and follow the steps.



[Second - Setting the environement]
- Open Terminal :
    On your Mac, do one of the following:

        - Click the Launchpad icon  in the Dock, type Terminal in the search field, then click Terminal.
        or
        - In the Finder , open the /Applications/Utilities folder, then double-click Terminal.
        or 
        - search for Terminal and press enter

(ATTENTION! change: [YOUR_PATH] into the path that correspond to the MsMrDTW_for_SonicVisualiser folder for you. 
You see it on Mac by activating :  View -> Show Path bar 
If the folder MsMrDTW_for_SonicVisualiser is on the desktop it should be something like : /Users/username/Desktop/)

- In the terminal enter those commands lines in this order : 

        - conda create -n mrmsdtw python=3.7
        - conda activate mrmsdtw
        - pip install -r [YOUR_PATH]/MsMrDTW_for_SonicVisualiser/requirements.txt
        - chmod +x [YOUR_PATH]/MsMrDTW_for_SonicVisualiser/MrMsDTW_for_sv_bash.sh



[Third - Replacing the Sonic Visualiser config file]
ATTENTION! change: [YOUR_PATH] into the path that correspond to the MsMrDTW_for_SonicVisualiser folder for you.

- Go into /Users/username/.config/sonic-visualiser

- Open the Sonic Visualiser.conf file and :
    - copy and paste this at the top : 

[Alignment]
alignment-program=[YOUR_PATH]/MsMrDTW_for_SonicVisualiser/MrMsDTW_for_sv_bash.sh
alignment-type=external-program-alignment



[Fourth - Changing the paths in MrMsDTW_for_sv_bash.sh]
- In the folder MsMrDTW_for_SonicVisualiser open the file MsMrDTW_for_SonicVisualiser/MrMsDTW_for_sv_bash.sh
- Change every : [YOUR_PATH] by the right path to the folder MsMrDTW_for_SonicVisualiser

