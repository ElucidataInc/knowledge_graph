import csv
import numpy as np

def get_relationship(associations, outfile, headers, names, actions, cutoff):
    first = True
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', escapechar='\\', quotechar='"', quoting=csv.QUOTE_ALL)
        for line in associations:
            if first:
                data = line.decode('utf-8').rstrip("\r\n").split()
                # creating headers for the output csv
                row = ["Protein1", "Protein2"]
                row.extend(data[2:])
                row.extend(headers)
                writer.writerow(row)
                first = False
                continue
            data = line.decode('utf-8').rstrip("\r\n").split()
            protein1 = data[0]
            protein2 = data[1]
            # scores of interactions
            scores = data[2:]
            scores_dec = [str(float(score) / 1000) for score in scores]
            # setting a threshold of 400 for combined score
            if protein1 in names.keys() and protein2 in names.keys() and float(scores_dec[-1]) >= cutoff:
                k = protein1 + protein2
                row = [protein1, protein2]
                # getting the protein interaction types and directionality from 'actions' dictionary
                d = actions[k]
                # getting scores of interactions
                row.extend(scores_dec)
                # appending to row the types and directionality of interaction
                if len(d.keys()) > 0:
                    row.append(d[k + 'mode'])
                    row.append(d[k + 'action'])
                    row.append(d[k + 'is_directional'])
                    row.append(d[k + 'a_is_acting'])
                else:
                    row.append(["NaN"]*len(headers))
                # print(row)
                writer.writerow(row)
