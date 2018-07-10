from .shade import buildShades


class Badge:

    def __init__(self, user):
        if not hasattr(user, 'corpus_values'):
            user.buildUserCorpus(day='today')

        self.user = user
        buildShades(self.user.group, day='today')

    def monoplyBadge(self):
        '''
        「内心独白」：连续 n 条自说自话/一个 lattice 发言超过10条，无人出现
        '''
        pass

    def iceBeakingBadge(self):
        '''
        「破冰者」：一段空白后第一位发言者
        '''
        pass

    def halfChampBadge(self):
        '''
        「半程冠军」：中午 12:00 积分榜第一
        '''
        pass
