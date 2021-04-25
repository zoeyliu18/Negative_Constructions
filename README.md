# Negative_Constructions
This repository contains code and data for the paper "English Negative Constructions and Communicative Functions in Child Language". The study investigates negative syntactic constructions and the communicative functions they play in early child language of English (age ranges from 12 to 72 months). 

## Data set construction ##

### From childes-db to csv ###
```
python3 COGSCI2021/diaparse/chides2csv.py --path OUTPUT_PATH
```

### From csv to conll (parsed dependency annotations) ###
```
python3 COGSCI2021/diaparse/diaparser.py --input CSV_DIRECTORY --output CONLL_DIRECTORY
```

### Extract negative (and positive) utterances ###
```
python3 COGSCI2021/diaparse/construction.py --input CONLL_DIRECTORY --output FILENAME --domain DOMAIN/FUNCTION (--desp)
```
    1. ```-desp``` is for whether you'd like to generate descriptive file (e.g. number of uterances at each age of the childre) for both child and parent speech
    2. 
