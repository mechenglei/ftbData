# -*- coding: utf-8 -*-


__author__ = 'chenglei'

import pandas as pd
from ftbData.config import BASE_URL, TEAM_URL, EVENT_URL, ODDS_URL

class Urls(object):

    @staticmethod
    def url(day):
        if pd.datetime.now().strftime('%Y%m%d') == day:
            return BASE_URL
        else:
            return '?date='.join([BASE_URL, day])

    @staticmethod
    def team_url(team_id):
        return ''.join([TEAM_URL, str(team_id)])

    @staticmethod
    def event_url(event_id):
        return ''.join([EVENT_URL, str(event_id)])

    @staticmethod
    def odds_url(game_id):
        return ''.join([ODDS_URL, str(game_id)])

