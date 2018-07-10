import re

from utils import formatToday


class Query():
    '''
    :param msg: `obj` wxpy.Message object
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

    def __init__(self, msg):
        self.command = None
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
