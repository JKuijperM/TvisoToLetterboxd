#!/usr/bin/env python
"""
Python script that converts an exported json file from the web TVISO to a csv file can be read by the web Letterboxd.

Author: Jorge Kuijper
Copyright: Copyright 2021, TvisoToLetterboxd
License: GPL 3.0
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# input_path is the path for the json file
input_path = Path('your_path.json')  # Replace the string 'your_path' by yours
# output_path is the path where will be saved the csv file
output_path = Path('your_path.csv')  # Replace the string 'your_path' by yours
with open(input_path, encoding='utf-8') as json_file:
    data = json.load(json_file)

# The following column names are the tags that need Letterboxd to read the file.
# Create an empty DataFrame with this columns:
# * imdbID: is the ID of the film in IMDB
# * Title: is the Title of the movie
# * Rating10: is the rate in TVISO
# * WatchedDate: is the date when you watched the movie
col = ['imdbID', 'Title', 'Rating10', 'WatchedDate']
df = pd.DataFrame(columns=col)

# Fill the DataFrame
for line in data:
    # Check if the status is watched and the type is movie
    if line['status'] == 'watched' and line['type'] == 2:
        title = line['title']
        imdb = line['imdb']
        rating = line['rating'] if line['rating'] is not None else ''
        # Silent catch if the watched date doesn't exist in TVISO and add an empty string
        try:
            watchedDate = line['checkedDate']
        except:
            watchedDate = ''

        if watchedDate != '':
            dt = datetime.strptime(watchedDate, '%Y-%m-%dT%H:%M:%S+%f:00')
            watchedDate = dt.strftime('%Y-%m-%d')

        # Insert into the DataFrame
        row_data = [imdb, title, rating, watchedDate]
        df.loc[len(df) + 1] = row_data
# Export DataFrame to csv
df.to_csv(output_path, index=False, encoding='utf-8')
print('Done!')
