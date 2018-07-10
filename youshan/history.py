from utils import formatToday


class History():

    def __init__(self, group):
        self.group = group

    @classmethod
    def getHistoryGroupName(cls, group):
        raw = group.r.hgetall('group_name_history')
        content = [(formatToday(timestamp=float(i[0])), i[1])
                   for i in raw.items()]
        return '\n'.join([' '.join(i) for i in content])

    @classmethod
    def getUserHistotyScore(cls, user):
        pass
