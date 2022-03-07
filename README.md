# automatic_alignement
Automatic alignment (Audio/Score-Audio) for precise performance analysis of symphonic recordings
This project was done in colaboration with Ircam as a last year project in Centrale Lille.

In src all the code developped for the project is accessible. It is composed of the code for the Auto-encoder, the bash script to use MATCH in a terminal, MrMsDTW function to use this method in Sonic-Visualiser and in a terminal, and there is utilities function used in the project. 

MrMsDTW_for_SonicVisualiser is a custom install folder to install MrMsDTW in Sonic-Visualiser on a Linux machine, it was given to the Musicologist of the project.

1. Clone this repository:

```bash
git clone https://github.com/aurianworld/automatic_alignement.git

```

2. Install requirements:

```bash
cd automatic_alignment
pip install -r requirements.txt

```

3. Install package locally:
```bash
pip install -e .
```
