import csv

with open('./data/guild_id_list.csv') as f:
    reader = csv.reader(f)
    print([int(y) for x in reader for y in x])