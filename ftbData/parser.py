# -*- coding: utf-8 -*-

__author__ = 'chenglei'

import re
import sys
import pandas as pd
from pyquery import PyQuery as pq

from ftbData.urls import Urls
from ftbData.items import ITEMS
from ftbData.config import TEAMS, EVENTS, COLUMNS
from ftbData.utils import extract_day, format_url, serialize, serialize_id

reload(sys)
sys.setdefaultencoding('utf-8')


def parser(url, odds=False):
    '''
    :param url: 
    :param odds: 
    :return: 
    '''
    items = []
    doc = pq(url=url)
    day = extract_day(url)

    for record in pq(doc('ul.layout-grid-list li')):
        item = ITEMS.score_items()
        record = pq(record)
        try:
            event_name = record('a.event-name').text().strip()
            event_id = record('a.event-name').attr('href').strip('/').split('-')[-1]
            hometeam_name = record('span.lab-team-home a').text().strip()
            hometeam_id = record('span.lab-team-home a').attr('href').strip('/').split('-')[-1]
            awayteam_name = record('span.lab-team-away a').text().strip()
            awayteam_id = record('span.lab-team-away a').attr('href').strip('/').split('-')[-1]
        except AttributeError:
            continue

        EVENTS[event_name] = event_id
        TEAMS[hometeam_name] = hometeam_id
        TEAMS[awayteam_name] = awayteam_id
        item['event_name'] = event_name
        item['hometeam_name'] = hometeam_name
        item['awayteam_name'] = awayteam_name
        item['matchtime'] = ' '.join([day, record('span.lab-time').text().strip()])
        item['score'] = record('span.score b').text().strip()
        item['result'] = record('span.lab-bet-odds span').text().strip()

        if odds:
            odds_url = format_url(record('span.lab-data a').attr('href'))
            item.update({
                'odds_url': odds_url
            })
        items.append(item)

    serialize(TEAMS, key='teams')
    serialize(EVENTS, key='events')

    df = pd.DataFrame(items)

    if odds:

        odds_items = [
            parser_odds(url)
            for url in df['odds_url'].tolist()
        ]

        odds_df = pd.DataFrame([
            odds_item
            for odds_item in odds_items
            if odds_item is not None
        ])

        df = pd.merge(df, odds_df, how='outer')
        del df['odds_url']

    return df


def parser_odds(url):

    doc = pq(url)
    item = ITEMS.odds_items()
    records = doc('tbody tr')
    if records is None:
        return item

    for record in records:
        record = pq(record)
        item['odds_url'] = url
        item['company'] = record('td.name.border').text().strip()

        handicap = record('td.rangQiu tr.first').text().strip().split()
        if len(handicap) == 3:
            item['hometeam_handicap'], item['odds_handicap'], item['awayteam_handicap'] = tuple(handicap)

        standard = record('td.biaoZhunPan tr.first').text().strip().split()
        if len(standard) == 3:
            item['hometeam_win'], item['draw'], item['awayteam_win'] = tuple(standard)

        goals = record('td.daXiaoQiu tr.first').text().strip().split()
        if len(goals) == 3:
            item['big'], item['odds_goals'], item['small'] = tuple(goals)

        return item


def parser_team(url, odds=False):
    '''
    :param team_url: 
    :return: 
    '''
    def compare(row):
        if row['homescore'] > row['awayscore']:
            return '胜'
        elif row['homescore'] == row['awayscore']:
            return '平'
        else:
            return '负'

    doc = pq(url).text()

    games = eval((re.findall(r'SCHEDULES=(.+?])', doc)[0]).split('SCHEDULES=')[1])
    df = pd.DataFrame(games)
    df['matchtime'] = df['matchtime'].apply(lambda x: pd.to_datetime(x, unit='s').strftime('%Y-%m-%d %H:%M'))
    df['score'] = df['homescore'].astype('str').str.cat(df['awayscore'].astype('str'), sep='-')
    df['result'] = df.apply(lambda row: compare(row), axis=1)
    serialize_id(df)

    if odds:
        df['odds_url'] = df['scheduleid'].apply(lambda x: Urls.odds_url(x))
        odds_items = [
            parser_odds(url)
            for url in df['odds_url'].tolist()
        ]

        odds_df = pd.DataFrame([
            odds_item
            for odds_item in odds_items
            if odds_item is not None
        ])

        df = pd.merge(df, odds_df, how='outer')
        del df['odds_url']
        columns = ITEMS.score_items().keys() + ITEMS.odds_items().keys()
    else:
        columns = ITEMS.score_items().keys()

    return df[columns]


def parser_event_url(url):
    '''
    :param event_url:
    :return:
    '''
    response = pq(url)
    url_dict = {}
    for link in response('a.color-black'):
        url = pq(link).attr('href').strip()
        if 'jifen' in url:
            url_dict['rank'] = format_url(url)
    return url_dict


def parser_event_stats(url):

    response = pq(url)

    tips = []
    for tip in response('div.tips span'):
        tip = pq(tip)
        tips.append(
            {
                'value': tip.text(),
                'color': tip[0].values()[0]
            }
        )

    columns = response('thead td').text().split()[:-1]

    items = []
    for record in response('table tbody')[0]:
        record = pq(record)
        item = record.text().split()

        if 'jifen' in url:
            item.insert(1, '')
            for tip in tips:
                if record('td.{0}'.format(tip.get('color'))):
                    item[1] = tip.get('value')

        items.append(item)

    if 'jifen' in url:
        columns.insert(1, u'升降级')
        columns = [ COLUMNS.get(column) for column in columns ]
    return pd.DataFrame(items, columns=columns)


def parse_live(url, jc=None):
	
	index = 0
	key = ''
	
	if jc is not None:
		if jc == 'jc':
			index = 0
			key = '竞彩'
		if jc == 'bd':
			index = 1
			key = '北单'
		if jc == 'zc':
			index = 2
			key = '足彩'
	
	doc = pq(url).text()
	text = eval(re.findall(r'THATDATA=({".+?}});', doc)[0])
	teams = dict([[item[0], item[1][0].split(',')[0]] for item in text.get('teams').items()])
	events = dict([[item[0], item[1][0].split(',')[0]] for item in text.get('events').items()])
	living = text.get('matchesTrans').get('live')
	unstart = [
		{
			'event': str(item[1]),
	        'time': item[3],
	        'hometeam': str(item[5][0]),
	        'awayteam': str(item[6][0]),
			'lottery': str(eval(item[-1])[-3][index])
		}
		for item in text.get('matchesTrans').get('notStart')
	]

	df = pd.DataFrame(unstart)
	df['event'] = df['event'].map(events)
	df['hometeam'] = df['hometeam'].map(teams)
	df['awayteam'] = df['awayteam'].map(teams)
	
	if jc is not None:
		df = df[df['lottery'].str.contains(key)]
		
	return df