import time
from sortedcontainers import SortedDict

from youshan import formatToday, getUserByPuid, INTERVAL


class Corpus():
    '''
    :attr today:
    :attr raw_today:
    :attr alltime:
    :attr raw_alltime:
    :attr puid_today:
    :attr raw_puid_today:

    '''

    def __init__(self, puid: str=None):
        with open('db', 'r') as f:
            all_dict = f.read().split('\n')
        all_dict.remove('')
        today = formatToday()
        self.today = [eval(item.split(' = ')[1])
                      for item in all_dict if today in item.split(' = ')[0]]
        self.raw_today = ''.join(
            [item['text'] for item in self.today if item['text'] is not None])
        self.alltime = [eval(item.split(' = ')[1]) for item in all_dict]
        self.raw_alltime = ''.join(
            [item['text'] for item in self.alltime
             if item['text'] is not None])
        if puid:
            self.puid = puid
            self.name = getUserByPuid(puid)
            self.puid_today = [
                m for m in self.today if m['user'] == getUserByPuid(puid)]
            self.raw_puid_today = ''.join([item['text']
                                           for item in self.puid_today
                                           if item['text'] is not None])
            self.buildConclusion()
            self.buildTimeBlocks()

    def buildConclusion(self):
        time_nodes = [m['time'] for m in self.puid_today]
        self.time_nodes = time_nodes
        delta_list = []
        for i in range(len(time_nodes)):
            if i > 0:
                delta_list.append(time_nodes[i] - time_nodes[i-1])
        separators = SortedDict([(delta_list.index(delta), delta)
                                 for delta in delta_list if delta > INTERVAL])
        self.separators = separators
        n_time_blocks = len(separators) + 1
        now = time.time()
        last_seen = self.puid_today[-1]['time']
        if now - last_seen > INTERVAL:
            if (now - last_seen)/60 >= 60:
                h = str((now - last_seen)/3600).split('.')[0]
                m = '{:.0f}'.format((now - last_seen)/60 % 60)
                self.conclusion = '{}老师今天出现{}次，最近一次是 {} 小时 {} 分钟前'.format(
                    self.name, n_time_blocks, h, m)
            else:
                m = '{:.0f}'.format((now - last_seen)/60 % 60)
                self.conclusion = '{}老师今天出现{}次，最近一次是 {} 分钟前'.format(
                    self.name, n_time_blocks, m)
        else:
            self.conclusion = '{}老师今天出现{}次，当前还在线呢'.format(
                self.name, n_time_blocks)

    def buildTimeBlocks(self):
        n_time_blocks = len(self.separators) + 1
        if n_time_blocks == 0:
            self.time_blocks = None
            return
        else:
            head = self.puid_today[:list(self.separators)[0]+1]
            body = []
            for i in range(len(self.separators) - 2):
                i += 1
                block = ''
                body.append()
            tail = self.puid_today[list(self.separators)[-1]+1:]
            self.time_blocks = head + body + tail
