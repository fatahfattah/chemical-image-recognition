import argparse, os, shutil
from fnmatch import fnmatch
from zipfile import ZipFile

"""
This program extracts the datapoints from a dataset, downloaded from the USPTO
Currently tested dataset type is called "Patent Grant Data/XML" on the USPTO site
I.e. https://bulkdata.uspto.gov/data/patent/grant/redbook/2021/

INPUT:
    -path = path to USPTO directory
OUTPUT:
    Will generate a new folder called 'dataset', contained chemical or nonchemical images

Can be ran as: 'python -m uspto_extractor -path=path/to/dir'
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", help="Provide the path to the extracted USPTO directory", required=True)
    uspto_data_path = parser.parse_args()

    pattern = "*.TIF"
    zip_pattern = "*.ZIP"

    # We walk through all dubdirectories
    for path, subdirs, files in os.walk(uspto_data_path):
        try:
            for name in files:

                # If a file is a ZIP, we unzip
                if fnmatch(name, zip_pattern):
                    os.chdir(path)
                    zip_file = ZipFile(os.path.join(path, name))
                    zip_file.extractall()
                    print("zip:", os.path.join(path, name))
                    zip_file.close()
                    unzipped_path = os.path.join(path, name[:-4])

                    # We walk through the unzipped files
                    for sub_path, sub_subdirs, sub_files in os.walk(unzipped_path):
                        for sub_name in sub_files:

                            # If file is an image (TIF)
                            if fnmatch(sub_name, pattern):
                                dataset_suffix = 'nonchemical'
                                if 'C' in sub_name.split('-')[-1]: # If name contains a 'C', it is a chemical image
                                    dataset_suffix = 'chemical'

                                    # Make chemical or nonchemical directory is not exist
                                    if not os.path.isdir(os.path.join(uspto_data_path, 'dataset', dataset_suffix)):
                                        os.makedirs(os.path.join(uspto_data_path, 'dataset', dataset_suffix))
                                        
                                    print(os.path.join(sub_path, sub_name), 'TO', dataset_suffix)
                                    shutil.copyfile(os.path.join(sub_path, sub_name), os.path.join(uspto_data_path, 'dataset', dataset_suffix, sub_name))

                    shutil.rmtree(unzipped_path)
                    print("\tRemoved zip:", name[:-4])
        except FileNotFoundError as e:
            print('File was not found', e)
            