# -*- coding: utf-8 -*-

__author__ = 'chenglei'

import pandas as pd
from contextlib import wraps

from ftbData import games


NOW = pd.datetime.now().strftime('%Y-%m-%d %H:%M')


def msc():
    def decorator(func):
        def wrapper(*args, **kwargs):
	        top = kwargs.get('top', 20)
	        df = func(args[0], top=top)
	        df['count'] = 1
	        return df.iloc[:top].groupby(['score'])['count'].sum().reset_index().sort_values(by=['count'], ascending=False)
        return wraps(func)(wrapper)
    return decorator


def filter():
    def decorator(func):
        def wrapper(*args, **kwargs):
	        df = func(*args, **kwargs)
	        return df[(df['matchtime'] <= NOW)]
        return wraps(func)(wrapper)
    return decorator


@filter()
def his_games(team_name):
	return games.get_team(team_name=team_name)

@msc()
def away_mcs(team_name, top=20):
	df = his_games(team_name)
	return df[df['awayteam_name']==team_name]


@msc()
def home_mcs(team_name, top=20):
	df = his_games(team_name)
	return df[df['hometeam_name']==team_name]


def games_record(hometeam_name, awayteam_name, top=20):
	df = his_games(hometeam_name)
	return df[((df['awayteam_name'] == awayteam_name) | (df['hometeam_name'] == awayteam_name)) & (df['matchtime'] <= NOW)]