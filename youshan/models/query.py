class Query():
    '''
    :param msg: `obj` wxpy.Message object
    '''
    commands = ['我的统计',
                '群统计',
                '今日关键词',
                '全部关键词',
                '在吗',
                ]

    def __init__(self, msg):
        self.command = None
        for c in self.commands:
            if c in msg.text:
                self.command = c
        self.isCommand(msg)

    @classmethod
    def isCommand(self, msg):
        if msg.text.count('@') == 1 and msg.text.index('@') == 0:
            if '\u2005' in msg.text:
                separator = '\u2005'
            else:
                separator = ' '

            if len(msg.text.split(separator)) == 2:
                if msg.text.split(separator)[1] == '在吗':
                    self.name = msg.text.split(separator)[0].replace('@', '')
                    return True
