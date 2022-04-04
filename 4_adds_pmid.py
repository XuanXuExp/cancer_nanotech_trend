# import csv
import pandas as pd

lla = pd.read_csv('lla_all_1.csv', low_memory=False)
PMID = pd.read_csv('adds_id_1.csv', low_memory=False)
ID = PMID[['id']]

# adds = pd.read_csv("address.csv", header=None, delimiter='\t', error_bad_lines=False)

cnt = 0
matchid = []

for item in lla['LAT']:
        if item == 'nl':
            val == "nl"
            cnt += 1
        else:
            val = ID[cnt]
        matchid.append(val)
print (matchid)

lla['ID'] = matchid

lla.to_csv("lla_id_1.csv", index=False)
