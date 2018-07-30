# -*- coding: utf-8 -*-

__author__ = 'chenglei'

import pandas as pd
from contextlib import wraps

from ftbData import games


NOW = pd.datetime.now().strftime('%Y-%m-%d %H:%M')


def msc():
    def decorator(func):
        def wrapper(*args, **kwargs):
            hometeam = kwargs.get('hometeam')
            top = kwargs.get('top', 20)
            df = func(hometeam=hometeam, top=top)
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


def hometeam():
    def decorator(func):
        def wrapper(*args, **kwargs):
	        hometeam = kwargs.get('hometeam')
	        df = func(hometeam=hometeam)
	        return df[df['hometeam_name']==hometeam]
        return wraps(func)(wrapper)
    return decorator


def awayteam():
    def decorator(func):
        def wrapper(*args, **kwargs):
            awayteam = kwargs.get('awayteam')
            df = func(hometeam=hometeam)
            return df[df['awayteam_name']==awayteam]
        return wraps(func)(wrapper)
    return decorator


def anyteam():
    def decorator(func):
        def wrapper(*args, **kwargs):
            hometeam = kwargs.get('hometeam')
            awayteam = kwargs.get('awayteam')
            df = func(hometeam=hometeam, awayteam=awayteam)
            return df[((df['awayteam_name'] == awayteam) | (df['hometeam_name'] == hometeam))]
        return wraps(func)(wrapper)
    return decorator


@filter()
def his_games(hometeam=None):
	return games.get_team(hometeam)


@msc()
@awayteam()
def away_mcs(hometeam=None, top=20):
	return his_games(hometeam)


@msc()
@hometeam()
def home_mcs(hometeam=None, top=20):
	return his_games(hometeam)


@msc()
@anyteam()
def games_mcs(hometeam=None, awayteam=None, top=20):
	return his_games(hometeam)


if __name__ == '__main__':
    print games_mcs(hometeam=u'曼彻斯特城', awayteam=u'多特蒙德')
