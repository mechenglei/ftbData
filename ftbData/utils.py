# -*- coding: utf-8 -*-

__author__ = 'chenglei'

import os
import difflib
import pandas as pd
import cPickle as pickle


def format_url(url):
    return ''.join(['https://', url.split('//')[-1]])


def extract_day(url):
    if 'date' in url:
        day = url.split('date=')[-1]
    else:
        day = pd.datetime.now()
    return pd.to_datetime(day).strftime('%Y-%m-%d')


def pklfile(key='teams'):
    if key == 'teams':
        filename = '.teams.pkl'
    if key == 'events':
        filename = '.events.pkl'
    return os.path.join(os.path.expanduser('~'), filename)


def hint(name, key='teams'):
    filepath = pklfile(key)
    with open(filepath) as f:
        dataset = pickle.load(f)
        id = dataset.get(name)
        if id is not None:
            return id

    df = pd.DataFrame(list(dataset.items()))
    df.columns = ['name', 'id']
    df['score'] = df['name'].apply(lambda x: (difflib.SequenceMatcher(None, x, name).quick_ratio()))
    print ' '.join(['Do you mean', (df[df['score'] > 0].sort_values(by='score', ascending=False).head(1)['name'].values[0]).decode('utf-8'), '?'])
    raise KeyError('Name Error.')


def serialize(dataset, key='teams'):
    filepath = pklfile(key)
    if os.path.exists(filepath) and os.stat(filepath).st_size > 0:
        with open(filepath, 'rb') as f:
            dataset.update(pickle.load(f))

    with open(filepath, 'wb') as f:
        pickle.dump(dataset, f)


def serialize_id(df):

    columns = df.columns.tolist()
    if 'hometeam_id' in columns and 'hometeam_name' in columns:
        serialize(dict(zip(df['hometeam_name'], df['hometeam_id'])))

    if 'awayteam_id' in columns and 'awayteam_name' in columns:
        serialize(dict(zip(df['awayteam_name'], df['awayteam_id'])))

    if 'eventid' in columns and 'event_name' in columns:
        serialize(dict(zip(df['event_name'], df['eventid']), key='events'))

