import re

from history import History
from utils import formatToday
from stats import groupStats, userStats, getTiming
from pbl import leaderboard, scoreDetails


class Query():
    '''
    :param msg: `obj` wxpy.Message object
    :param group: `obj` necessary when in need to `deliver`
    '''
    commands = {'在吗': getTiming,

                '群统计': groupStats,
                '群排名': groupStats,
                '群排行': groupStats,
                '我的统计': userStats,

                '积分榜': leaderboard,
                '群积分': leaderboard,
                '群榜单': leaderboard,
                '我的积分': scoreDetails,

                '历史群名': History.getHistoryGroupName,
                }
    funcs = []

    emojiDict = {
        '#1': '🥇',
        '#2': '🥈',
        '#3': '🥉',
    }

    def __init__(self, msg, group):
        self.command = None
        self.day = self.parseDate(msg)
        self.group = group
        self.msg = msg
        self.send = msg.member.group.send

        for c in self.commands.keys():
            if c in msg.text:
                self.command = self.commands[c]
        self.isCommand(msg)

    @classmethod
    def isCommand(self, msg):
        if msg.text.count('@') == 1 and msg.text.index('@') == 0:
            if '\u2005' in msg.text:
                separator = '\u2005'
            else:
                separator = ' '

            if len(msg.text.split(separator)) == 2:
                if msg.text.split(separator)[1] in self.commands.keys():
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
        payload = self.command(self.msg, self.group, self.day)

        # final make up just before launch
        if payload:
            payload = self.replaceEmoji(payload)
            print(f'sending payload: \n{payload}')
            self.send(payload)

    # functioning part
    # register & init group
    # if msg.text == '开启统计功能':
    #     group.send(registerGroup(msg, 'on'))
    # elif msg.text == '关闭统计功能':
    #     group.send(registerGroup(msg, 'off'))
