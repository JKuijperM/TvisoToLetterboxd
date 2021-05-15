import csv
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# csv_path = Path(r'D:\DESCARGAS\tviso-collection.csv')
# df = pd.read_csv(csv_path, sep=';')

json_path = Path('data/tviso-collection.json')
with open(json_path, encoding='utf-8') as json_file:
    data = json.load(json_file)

# col = ['imdbID,Title,Rating10,WatchedDate']
col = ['imdbID', 'Title', 'Rating10', 'WatchedDate']
df = pd.DataFrame(columns=col)

for line in data:
    if line['status'] == 'watched' and line['type'] == 2:
        title = line['title']
        imdb = line['imdb']
        rating = line['rating'] if line['rating'] is not None else ''
        try:
            watchedDate = line['checkedDate']
        except:
            watchedDate = ''

        if watchedDate != '':
            dt = datetime.strptime(watchedDate, '%Y-%m-%dT%H:%M:%S+%f:00')
            watchedDate = dt.strftime('%Y-%m-%d')

        # row_data = '{},{},{},{}'.format(imdb, title, rating, watchedDate)
        row_data = [imdb, title, rating, watchedDate]
        df.loc[len(df) + 1] = row_data

df.to_csv('test.csv', index=False, encoding='utf-8')
