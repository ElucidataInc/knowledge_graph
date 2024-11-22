import gzip
from collections import defaultdict


def get_actions(fi):
    actions = defaultdict(dict)
    temp = defaultdict(list)
    first = True
    with gzip.open(fi, 'rb') as mf:
        for line in mf:
            if first:
                first = False
                data = line.decode('utf-8').rstrip("\r\n").split("\t")
                # copy the headers
                headers = data[2:]
                continue
            data = line.decode('utf-8').rstrip("\r\n").split("\t")
            protein1 = data[0]
            protein2 = data[1]
            properties = data[2:]
            proteins_interacting = protein1 + protein2
            # creating a dictionary for storing all modes , actions and directionality of two interacting proteins
            temp[proteins_interacting + 'mode'].append(properties[0])
            temp[proteins_interacting + 'action'].append(properties[1])
            temp[proteins_interacting + 'is_directional'].append(properties[2])
            temp[proteins_interacting + 'a_is_acting'].append(properties[3])
            # keys are string formed by concatenating 'protein1' and 'protein2'
            actions[proteins_interacting] = temp
    return actions, headers
