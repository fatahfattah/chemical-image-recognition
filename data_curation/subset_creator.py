import os, random, argparse
random.seed(42)
from shutil import move


"""
Simple program to create a subset of a dataset.
Usefull when you have an imbalanced dataset and want to create a balanced subset

INPUT:
    -datasetpath: path to the complete dataset folder
    -destpath: path to where the subset should be placed
    -n: number of images each new class subset should contain
OUTPUT:
    Will create a subset that contains n samples from each target class

Can be ran as: 'python -m subset_creator -datasetpath=path/to/dataset -destpath=path/to/subset -n=x
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-datasetpath', 'Path to the dataset', required=True)
    parser.add_argument('-destpath', 'Path where the subset should be placed', required=False)
    parser.add_argument('-n', 'Number of datapoints for each class, if empty, takes 20% for each subclass', required=False)
    parsed_args = parser.parse_args()

    path = parsed_args.datasetpath
    target_path = parsed_args.destpath if parsed_args.destpath else os.path.join(path, 'subset')
    n = parsed_args.n

    # Move to subset dir
    classes = os.listdir(path)
    for c in classes:
        if not os.path.isdir(os.path.join(target_path, c)):
            os.makedirs(os.path.join(target_path, c))

    for c in classes:
        root = os.path.join(path, c)
        subset_size = n if n else os.listdir(root) // 5 # if n is not provided, take 20% of class size
        # Take random sample from original dataset and move to subset
        for x in random.sample(os.listdir(root), subset_size):
            move(os.path.join(root, x), os.path.join(target_path, c))
    

    print(f'Finished creating subset of original dataset: {path}, to subset: {target_path}')