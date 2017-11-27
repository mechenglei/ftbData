# -*- coding: utf-8 -*-

__author__ = 'chenglei'

import sys
import pandas as pd

from urls import Urls
from utils import hint
from parser import parser, parser_team, parser_event_stats, parser_event_url

reload(sys)
sys.setdefaultencoding('utf-8')


def get_today(odds=False):
    return parser(Urls.url(pd.datetime.now().strftime('%Y%m%d')), odds=odds)


def get_his(start, end=None, odds=False):
    if end is None:
        return parser(Urls.url(start))
    else:
        ts = pd.DataFrame()
        for day in pd.date_range(start, end).strftime('%Y%m%d'):
            ts = ts.append(parser(Urls.url(day), odds=odds))
        return ts


def get_team(team_name, odds=False):
    team_name = team_name.decode('utf-8')
    team_id = hint(team_name)
    team_url = Urls.team_url(team_id)
    return parser_team(team_url, odds=odds)


def get_rank(event_name):
    event_name = event_name.decode('utf-8')
    event_id = hint(event_name, key='events')
    urls = parser_event_url(Urls.event_url(event_id))
    rank_url = urls.get('rank')
    return parser_event_stats(rank_url)
