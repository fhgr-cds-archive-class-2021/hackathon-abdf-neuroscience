# fhgr-cds-310-neuroscience
Repository for hackathon in neuroscience module cds-310@FHGR

## Goal of the project
The goal of our project is to set a target mood according to the brain wave frequencies.
- Gamma (greater than 30Hz)
- BETA (13-30Hz)
- ALPHA (8-12 Hz)
- THETA (4-8 Hz)
- DELTA (less than 4 Hz)

We try to pick a playlist according to the given mood and stimulate the brain to achieve the change of mood, e.g. we want to put our users to a more calm environment for studying.

## Python Environemnt
- ``conda create --name myenv python=3.10``
- ``conda activate myenv``
- ``conda install pip``
- ``pip install -r requirements.txt``

## Project structure
- [Data Simulator](./Simulator)
    - Here we created a data simulator for testing our code as it is hard to achieve a consistent brain wave change
- [Preprocessing](./Preprocessing)
    - Here we implemented our preprocessing logic
- [Start Code](./Pipeline)
    - To run the code use the following:
        - ``python .\datastream.py``
    - Instructions for data pipeline and gui: [README](./Gui/README.md).
