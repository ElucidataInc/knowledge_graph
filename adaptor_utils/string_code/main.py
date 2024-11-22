# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# STRING database wrapper,creates a mapping and relationship file
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

import os.path
import gzip
import yaml
import numpy as np
from download_files import download_db
from get_actions_dict import get_actions
from get_map_dict import get_mapping
from get_name_dict import get_names
from get_node_file import get_node
from get_relationship_file import get_relationship

if __name__ == '__main__':
    yaml_file = './config.yml'
    with open(yaml_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            raise yaml.YAMLError("The yaml file {} could not be parsed. {}".format(yaml_file, err))
    # get all arguments from config.yml
    databaseURL = config['STRING_database_url']
    mapping_url = config['STRING_mapping_url']
    name_url = config['STRING_name_url']
    actions_url = config['STRING_actions_url']
    cutoff = config['STRING_cutoff']
    directory = config['STRING_directory']
    source1 = config['STRING_source1']
    source2 = config['STRING_source2']
    source3 = config['STRING_source3']

    try:
        # Create target Directory
        os.mkdir(directory)
        print("Directory ", directory, " Created ")
    except FileExistsError:
        print("Directory ", directory, " already exists")

    # download protein interactions,actions,aliases and info file from STRING
    db_file = download_db(databaseURL, directory)
    map_file = download_db(mapping_url, directory)
    actions_file = download_db(actions_url, directory)
    names_file = download_db(name_url, directory)

    # get dictionary with key  as string formed by concatenating ensembl ids of interacting proteins and
    # value as a dictionary with all possible  types and direction of interaction of the interacting proteins
    fi = os.path.join(directory, actions_file)
    actions, headers = get_actions(fi)

    # get dictionary for each of the sources(sources of protein accession ids) with ensembl id as key and
    # all possible aliases for that source as values
    fi = os.path.join(directory, map_file)
    source1_list, source2_list, source3_list = get_mapping(source1, source2, source3, fi)

    # get dictionary with ensembl ids as keys and preferred name as value
    fi = os.path.join(directory, names_file)
    names = get_names(fi)

    df = get_node(source1, source2, source3, source1_list, source2_list, source3_list, names)
    # writing to csv
    df.to_csv(os.path.join(directory, "string_protein_node.tsv"), sep='\t', index=False)

    # read the protein interactions file
    fi = os.path.join(directory, db_file)
    associations = gzip.open(fi, 'r')

    outfile = os.path.join(directory, "string_interactswith_relationship.tsv")
    get_relationship(associations, outfile, headers, names, actions, cutoff)
