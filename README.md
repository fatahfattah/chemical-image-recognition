# chemical-image-recognition


## data_curation
Contains all code to create a labeled dataset from the USPTO.

### USPTO extractor
Create a chemical/nonchemical labeled dataset from a "raw" USPTO input file

### Subset creator
Create a subset of n images per class, i.e. when balancing an imbalanced dataset

### manychem seperator
Extract chemical datapoints that contain more than one 1 count structure.
* Requires creation of a countfile through some external tool or manually


## chemononchem
Contains all code to train the chemical/nonchemical model, using a labeled dataset