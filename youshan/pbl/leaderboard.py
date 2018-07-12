import random

from utils import formatToday
from shade import (buildShades, countUserShowUps,
                   getBiggestShade, getLongestShade, getShadeParticipants)


def initUserShowUps(group, day: str='today'):
    for u in group.members:
        countUserShowUps(u, day)


def initUserScore(group):
    for u in group.members:
        u.basic_score = 0
        u.bonus_score = 0


def addBasicScore(group):

    # show_ups
    for u in group.members:
        u.basic_score += len(set(u.show_ups)) / \
            (1+random.random()/len(group.members))
        u.basic_score += len(u.show_ups) * 0.1


def addBonusScore(participants):
    '''
    this is for bs

    :param participants: product of `getShadeParticipants()`
    '''
    p = participants
    _avr = sum([i[1] for i in p]) / len(p)
    for i in p:
        if abs(i[1]-_avr) < 1:
            i[0].bonus_score = 5
        elif 1 <= abs(i[1]-_avr) < 2:
            i[0].bonus_score = 3
        elif abs(i[1]-_avr) > 2:
            i[0].bonus_score = 1


def leaderboard(msg, group, day: str='today') -> str:
    '''
    '''

    if day is 'today':
        day = formatToday()

    # build shades
    shades = buildShades(group, day)
    bs = getBiggestShade(group, shades)
    ls = getLongestShade(group, shades)

    # init
    initUserScore(group)
    # basic
    addBasicScore(group)

    # bs/ls bonus
    bs_participants = getShadeParticipants(group, bs[0])
    for u in getShadeParticipants(group, bs[0]):
        u[0].bonus_score += bs[1] / \
            len(bs_participants) * (1 - (random.random()/len(bs_participants)))

    ls_participants = getShadeParticipants(group, ls[0])
    for u in getShadeParticipants(group, ls[0]):
        u[0].bonus_score += len(ls[0]) / \
            len(ls_participants) * (1 - (random.random()/len(ls_participants)))

    # participation bonus
    addBonusScore(bs_participants)
    addBonusScore(ls_participants)

    return parse(group, day)


def parse(group, day: str) -> str:
    '''
    Parse the `group` that `leaderboard` produced
    Return the text which `send` needs
    '''
    for u in group.members:
        if hasattr(u, 'iceBreakingBadges') and u.iceBreakingBadges:
            if '🏅' not in u.name:
                u.name = '🏅' + u.name
    leaderboard_title = f'{day} 积分榜 \n'
    raw_data = sorted([(u.basic_score+u.bonus_score, u.name)
                       for u in group.members])
    contents = []
    for i in range(len(raw_data)):
        item = raw_data.pop()
        content = f'#{i+1} {item[1]} 老师 {item[0]:.2f} 分'
        contents.append(content)

    return leaderboard_title + '\n'.join(contents)


def scoreDetails():
    pass
