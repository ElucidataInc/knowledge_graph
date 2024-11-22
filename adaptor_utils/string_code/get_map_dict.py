import gzip
from collections import defaultdict


def get_mapping(source1, source2, source3, fi):
    source1_list = defaultdict(set)
    source2_list = defaultdict(set)
    source3_list = defaultdict(set)
    first = True
    with gzip.open(fi, 'rb') as mf:
        for line in mf:
            if first:
                first = False
                continue
            data = line.decode('utf-8').rstrip("\r\n").split("\t")
            string_id = data[0]
            alias = data[1]
            sources = data[2].split(' ')
            # creating list for desired protein accession ids
            if source1 in sources or source2 in sources or source3 in sources:
                if source1 in sources:
                    source1_list[string_id].add(alias)
                elif source2 in sources:
                    source2_list[string_id].add(alias)
                else:
                    source3_list[string_id].add(alias)
    return source1_list, source2_list, source3_list
