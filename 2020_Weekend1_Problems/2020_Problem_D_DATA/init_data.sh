#! /bin/bash

### DOESN'T SEEM TO WORK
rm -f data/groundtruths/*.csv
python groundtruth.py
python gamegroundanal.py
