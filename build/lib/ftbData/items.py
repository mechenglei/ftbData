# -*- coding: utf-8 -*-

__author__ = 'chenglei'


class ITEMS(object):

   @staticmethod
   def score_items():
      return {
         'event_name': None,
         'matchtime': None,
         'score': None,
         'hometeam_name': None,
         'awayteam_name': None,
         'result': None,
      }

   @staticmethod
   def odds_items():
      return {
         'company': None,
         'hometeam_handicap': None,
         'odds_handicap': None,
         'awayteam_handicap': None,
         'hometeam_win': None,
         'draw': None,
         'awayteam_win': None,
         'big': None,
         'odds_goals': None,
         'small': None,
      }

