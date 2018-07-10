import re
import time

from stats import stats
from models import User
from history import History
from utils import formatToday
from pbl import leaderboard, scoreDetails


class Query():
    '''
    :param msg: `obj` wxpy.Message object
    :param group: `obj` necessary when in need to `deliver`
    '''
    commands = ['在吗',

                '群统计',
                '我的统计',

                '今日关键词',
                '全部关键词',

                '积分榜',
                '我的积分',

                '历史群名',
                ]

    def __init__(self, msg, group=None):
        self.msg = msg
        self.command = None
        self.deliverToMember = msg.member.send
        if group:
            self.group = group
            self.deliverToGroup = msg.member.group.send

        for c in self.commands:
            if c in msg.text:
                self.command = c
        self.isCommand(msg)
        if self.parseDate(msg):
            self.day = self.parseDate(msg)

    @classmethod
    def isCommand(self, msg):
        if msg.text.count('@') == 1 and msg.text.index('@') == 0:
            if '\u2005' in msg.text:
                separator = '\u2005'
            else:
                separator = ' '

            if len(msg.text.split(separator)) == 2:
                if msg.text.split(separator)[1] in self.commands:
                    self.name = msg.text.split(separator)[0].replace('@', '')
                    return True

    def parseDate(self, msg):
        match = re.search(r'20\d\d\d\d\d\d', msg.text)
        if not hasattr(match, 'group'):
            return formatToday()
        else:
            return match.group()

    def deliver(self):
        if '我的统计' in self.command:
            self.deliverToGroup(stats(self.msg, User(self.msg)))
        elif '群统计' in self.command:
            self.deliverToGroup(stats(self.msg))
        elif '积分榜' in self.command:
            self.deliverToGroup(leaderboard(self.group, self.day))
        elif '我的积分' in self.command:
            self.deliverToMember(scoreDetails(User(self.msg)))
        elif '历史群名' in self.command:
            self.deliverToGroup(History.getHistoryGroupName(self.group))

        else:
            time.sleep(0.5)
            self.deliverToGroup('你想干啥？')
