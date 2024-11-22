import gzip


def get_names( fi):
    first = True
    names = {}
    with gzip.open(fi, 'rb') as mf:
        for line in mf:
            if first:
                first = False
                continue
            data = line.decode('utf-8').rstrip("\r\n").split("\t")
            string_id = data[0]
            preferred_name = data[1]
            # ensembl id as key and preferred name as value
            names[string_id] = preferred_name
    return names
