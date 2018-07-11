import re
import time

from models import User
from history import History
from utils import formatToday
from stats import stats, getTiming
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
    funcs = []

    emojiDict = {
        '#1': '🥇',
        '#2': '🥈',
        '#3': '🥉',
    }

    def __init__(self, msg, group):
        self.msg = msg
        self.command = None
        self.group = group

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

    def replaceEmoji(self, payload):
        for key in self.emojiDict.keys():
            if key in payload:
                payload = payload.replace(key, self.emojiDict[key])
        return payload

    def deliver(self):
        if '我的统计' in self.command:
            payload = stats(self.msg, User(self.msg))
            send = self.msg.member.group.send
        elif '在吗' in self.command:
            payload = getTiming(User(self.msg))
            send = self.msg.member.group.send
        elif '群统计' in self.command:
            payload = stats(self.msg)
            send = self.msg.member.group.send
        elif '积分榜' in self.command:
            payload = leaderboard(self.group, self.day)
            send = self.msg.member.group.send
        elif '我的积分' in self.command:
            payload = scoreDetails(User(self.msg))
            send = self.msg.member.send
        elif '历史群名' in self.command:
            payload = History.getHistoryGroupName(self.group)
            send = self.msg.member.group.send

        else:
            time.sleep(0.5)
            payload = '你想干啥？'
            send = self.msg.member.group.send

        # final make up just before launch
        if payload:
            payload = self.replaceEmoji(payload)
            print(f'sending payload: \n{payload}')
            send(payload)

    # functioning part
    # register & init group
    # if msg.text == '开启统计功能':
    #     group.send(registerGroup(msg, 'on'))
    # elif msg.text == '关闭统计功能':
    #     group.send(registerGroup(msg, 'off'))
