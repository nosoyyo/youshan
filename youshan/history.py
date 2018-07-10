class History():

    def __init__(self, group):
        self.group = group

    @classmethod
    def getHistoryGroupName(cls, group):
        r = group.r
