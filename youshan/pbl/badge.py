import time

from .shade import buildShades, countUserShowUps, getSecByLattice


class Badge:

    def __init__(self, user):

        countUserShowUps(user)

        self.user = user
        self.group = user.group
        self.r = user.r
        self.shades = buildShades(self.group, day='today')
        self.group_corpus_keys = [float(i) for i in list(
            self.r.hgetall(self.group.uuid)) if i.replace('.', '').isdigit()]

        # check badges one by one
        self.iceBreakingBadge()

    def monoplyBadge(self):
        '''
        「内心独白」：连续 n 条自说自话/一个 lattice 发言超过10条，无人出现
        '''
        pass

    def iceBreakingBadge(self):
        '''
        「破冰者」：一段空白(至少半小时)后第一位发言者
        '''
        self.user.iceBreakingBadges = []
        self.user.buildUserCorpus(day='today')
        self.user_corpus = list(self.user.corpus_values)
        first_in_shades = [i[0] for i in self.shades]
        candidates = list(
            set([i for i in self.user.show_ups if i in first_in_shades]))
        if candidates:
            for c in candidates:
                bound = getSecByLattice(c)
                _min = 999
                for i in self.group_corpus_keys:
                    if abs(i-bound) < _min:
                        _min = i - bound
                winner = self.r.hget(
                    self.group.uuid, str(bound+_min))
                if winner == 'None':
                    continue
                elif winner in self.user_corpus:
                    t = time.localtime(bound+_min)
                    winner = f'{t.tm_hour} 点 {t.tm_min} 分： {winner}\n'
                    self.user.iceBreakingBadges.append(winner)
            if self.user.iceBreakingBadges:
                return len(self.user.iceBreakingBadges)

    def halfChampBadge(self):
        '''
        「半程冠军」：中午 12:00 积分榜第一
        '''
        pass
