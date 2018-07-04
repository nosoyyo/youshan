import time
import jieba
from sortedcontainers import SortedDict

from models import User, theGroup
from utils import formatToday


INTERVAL = 300


def stats(msg, user: User=None) -> str:
    group = theGroup(msg)
    for u in group.members:
        u.uuid = theGroup.getUserUUID(u)

    if not user:
        # build chart
        raw_data = group.r.zscan(f'{group.uuid}{formatToday()}freq')[1]
        if not raw_data:
            return '今天贵群还没开张！'
        chart_title = '今天贵群刷了{:.0f}条:\n'.format(raw_data.pop()[1])
        charts = []
        if len(raw_data) > 0:
            for i in range(len(raw_data)):
                item = raw_data.pop()
                chart_content = '#{} {} 老师 {:.0f} 条'.format(
                    i+1, group.r.hget(group.uuid, item[0]), item[1])
                charts.append(chart_content)
        chart = chart_title + '\n'.join(charts)

        # get the longest disappearing guy
        ldg_flag = all(
            [bool(
                group.r.lrange(
                    f'{u.uuid}{formatToday()}', 0, -1))
             for u in group.members])
        if ldg_flag:
            ldg = SortedDict(
                zip(
                    [group.r.lrange(f'{u.uuid}{formatToday()}', 0, -1)[-1]
                     for u in group.members],
                    [u.name for u in group.members]
                )
            )
            guy = ldg.popitem(0)
            delta = abs(float(guy[0]) - time.time())
            if delta > 3600:
                text = f'{guy[1]}老师已经 {int(delta/3600)} 个多小时没有出现了，大家快去关心他一下。'
                return chart + '\n' + text
            else:
                return chart
        else:
            return chart
    elif user:
        user.uuid = user.r.hget(group.uuid, user.remark_name)
        user.keys = user.r.lrange(f'{user.uuid}{formatToday()}', 0, -1)
        if not user.keys:
            return f'{user.nick_name}老师还没发言。'
        user.corpus = user.r.hmget(group.uuid, user.keys)
        max_chars = ''
        for item in user.corpus:
            if item is not None and len(item) > len(max_chars):
                max_chars = item
        user.today_chars = sum(len(item)
                               for item in user.corpus if item is not None)
        user.kw_today = '\n'.join(jieba.analyse.textrank(
            '。'.join(item for item in user.corpus if item is not None),
            topK=10,
            withWeight=False,
            allowPOS=('ns', 'n')))
        stats = '''{0} 老师今天刷了 {1:.0f} 条，共 {2} 字
平均每条 {3:.2f} 字
最长一条 {4} 字，内容如下：
{5}\n
{0} 老师的今日关键词：\n
{6}
        '''.format(user.name,
                   len(user.corpus),
                   user.today_chars,
                   user.today_chars/len(user.corpus),
                   len(max_chars),
                   max_chars,
                   user.kw_today)
        return stats


def getTiming(user: User):
    '''
    Separators look like
    `SortedDict({6: 1033.0, 7: 406.0, 11: 752.0, 23: 605.0, 25: 552.0})`
    A `separator` is a special `delta` that's bigger than `INTERVAL`
    the key in the SortedDict is the index
    `INTERVAL` is set as a global var, `300` by default
    `delta` = `msg[i]['time'] - msg[i-1]['time']`
    Thus, for instance, an item like `{6:1033.0}` indicates that
    it is generated via `msg[7] - msg[6]`, therefore the 6th `delta`
    in the `delta_list`
    And as the 1st separator in `separators`, the 1st `time_block` could be
    formed with `corpus[:7]` i.e. `corpus[:list(separators)[0]+1]`
    '''
    # name = getUserByPuid(puid) -> user.name
    user.uuid = user.r.hget(theGroup.uuid, user.remark_name)
    user.keys = user.r.lrange(f'{user.uuid}{formatToday()}', 0, -1)
    if not user.keys:
        return '{}老师今天还未出现！'.format(user.name)
    user.corpus = user.r.hmget(theGroup.uuid, user.keys)
    time_nodes = user.keys
    delta_list = []
    for i in range(len(time_nodes)):
        if i > 0:
            delta_list.append(float(time_nodes[i]) - float(time_nodes[i-1]))
    separators = SortedDict([(delta_list.index(delta), delta)
                             for delta in delta_list if delta > INTERVAL])
    n_time_blocks = len(separators) + 1
    # list(separators)[0]: the last msg from the 1st time_block
    # list(separators)[-1] the last msg from time_blocks[-2] if
    # TODO: time_blocks = []
    now = time.time()
    last_seen = float(user.keys[-1])
    if now - last_seen > INTERVAL:
        if (now - last_seen)/60 >= 60:
            h = str((now - last_seen)/3600).split('.')[0]
            m = '{:.0f}'.format((now - last_seen)/60 % 60)
            conclusion = '{}老师今天出现{}次，最近一次是 {} 小时 {} 分钟前'.format(
                user.name, n_time_blocks, h, m)
        else:
            m = '{:.0f}'.format((now - last_seen)/60 % 60)
            conclusion = '{}老师今天出现{}次，最近一次是 {} 分钟前'.format(
                user.name, n_time_blocks, m)
        return conclusion
    else:
        conclusion = '{}老师今天出现{}次，当前还在线呢'.format(
            user.name, n_time_blocks)
        return conclusion
