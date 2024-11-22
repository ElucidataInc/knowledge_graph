import pandas as pd
import numpy as np


def get_node(source1, source2, source3, source1_list, source2_list, source3_list, names):
    df = pd.DataFrame(columns=["Ensembl_ID", "Preferred_name", source1, source2, source3])
    for i in names.keys():
        # append rows by adding ensembl ids from 'names' dictionary
        df = df.append({'Ensembl_ID': i}, ignore_index=True)
        df.loc[df['Ensembl_ID'] == i, 'Preferred_name'] = names[i]
        # if ensembl id is present in the source dictionary, add the list to specific source column
        h=0
        g=0
        p=0
        if i in source1_list.keys():
            df.loc[df['Ensembl_ID'] == i, source1] = source1_list[i]
            h = 1
        if i in source2_list.keys():
            df.loc[df['Ensembl_ID'] == i, source2] = source2_list[i]
            g = 1
        if i in source3_list.keys():
            df.loc[df['Ensembl_ID'] == i, source3] = source3_list[i]
            p = 1
        if h != 1:
            df.loc[df['Ensembl_ID'] == i, source1] = "NaN"
        if g != 1:
            df.loc[df['Ensembl_ID'] == i, source2] = "NaN"
        if p != 1:
            df.loc[df['Ensembl_ID'] == i, source3] = "NaN"
    return df
