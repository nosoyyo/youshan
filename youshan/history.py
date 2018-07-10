from utils import formatToday


class History():

    def __init__(self, group):
        self.group = group

    @classmethod
    def getHistoryGroupName(cls, group):
        raw = r.hgetall('group_name_history')
        content = []
