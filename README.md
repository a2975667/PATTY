# PATTY
This repository is an enhanced version from the forked library. It is an implementation from the publication [PATTY: A Taxonomy of Relational Patterns with Semantic Types](https://www.aclweb.org/anthology/D12-1104). This implementation can have slight modification from the original paper due to limited information disclosed and the results are not guaranteed. 

The goal of PATTY is given a entity labed corpus, extract entity relationships and locate patterns of sentneces for future entity extraction usage.

# Requirements
PATTY requires python 3.5+ to run. All external libraries are specified within the requirements.txt file.
```
python3 -m venv .venv
pip install -r requirements.txt
```

# Run
PATTY requires two user input information: entity and corpus data.
- entity: located in `src/entity.py`, it specifies the entities that were to be extracted and appears in the corpus
- data: `data/` requires a file that follows the following structure. Each line is a document that entities are highlighted by appending `<Entity>_` in front.
```
PERSON_Tom_Thabane resigned in DATE_October_last_year to form the All Basotho Convention (ORGANIZATION_ABC), crossing the floor with NUMBER_17 members of parliament, causing constitutional monarch King PERSON_Letsie_III to dissolve parliament and call the snap election.
```

To execute the program, run:
```
cd src
python main $DATA_ROOT $CORPUS_NAME
```

# Output
All output files are in binary for the intrest of data size and machine readability. It can be transformed into text by running `transform.sh` in the `data/` folder.
```
./transform.sh
```
