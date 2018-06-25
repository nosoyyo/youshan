import time
import jieba.analyse
from datetime import datetime
from sortedcontainers import SortedDict

from wxpy import *

global LOGGEDIN
LOGGEDIN = False


def aloha():
    global LOGGEDIN
    LOGGEDIN = True
    print('successfully logged in')
    print('LOGGEDIN is ' + str(LOGGEDIN))


def reLogin():
    global LOGGEDIN
    LOGGEDIN = False
    print('logged out')
    print('LOGGEDIN is ' + str(LOGGEDIN))
    time.sleep(1)
    for i in range(3):
        bot = Bot(cache_path=True, login_callback=aloha,
                  logout_callback=reLogin)
        if LOGGEDIN:
            break


bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)

the_group = bot.search('友善')[0]


def getNamePuidDict():
    bot.enable_puid()
    name_list = [m.nick_name for m in the_group.members]
    puid_list = [m.puid for m in the_group.members]
    return dict(zip(name_list, puid_list))


def getUserByPuid(puid: str) -> str:
    youshan = getNamePuidDict()
    return tuple(youshan)[list(youshan.values()).index(puid)]


def formatToday() -> str:
    ahora = datetime.now()

    def zero(inp: int) -> str:
        if len(str(inp)) != 2:
            return '0' + str(inp)
        else:
            return str(inp)
    return str(ahora.year) + zero(ahora.month) + zero(ahora.day)


def genMsgId() -> str:
    with open('db', 'r') as f:
        return str(len(f.readlines()) + 1)


def stats(puid: str=None) -> str:
    corpus_today = getCorpus('today')
    today_n = len(corpus_today)
    youshan = getNamePuidDict()
    if not puid:
        sds = {}
        sd_names = list(youshan)
        sd_rank = {}
        for sd in sd_names:
            sds[sd] = [item for item in corpus_today if item['user'] == sd]
            sd_rank[sd] = len(sds[sd])
        sd_rank = {value: key for key, value in sd_rank.items()}
        sd_rank = SortedDict(sd_rank)

        # build chart
        chart_title = '今天贵群刷了{}条:\n'.format(today_n)
        charts = []
        sd_rank_list = list(sd_rank)
        sd_name_list = list(sd_rank.values())
        for i in range(len(sd_rank)):
            chart_content = '#{} {} 老师 {} 条'.format(
                i+1, sd_name_list.pop(), sd_rank_list.pop())
            charts.append(chart_content)
        chart = chart_title + '\n'.join(charts)
        return chart
    elif puid:
        name = getUserByPuid(puid)
        user_corpus = [item for item in corpus_today if item['user'] == name]
        user_n = len(user_corpus)
        user_texts = [item['text']
                      for item in user_corpus if item['text'] is not None]
        max_chars = ''
        for item in user_texts:
            if len(item) > len(max_chars):
                max_chars = item

        user_chars = sum(len(item) for item in user_texts)

        my_kw_today = '\n'.join(jieba.analyse.textrank(
            getCorpus('raw_puid_today', puid),
            topK=10,
            withWeight=False,
            allowPOS=('ns', 'n')))

        stats = '''{0} 老师今天刷了 {1} 条，共 {2} 字
平均每条 {3:.2f} 字
最长一条 {4} 字，内容如下：
{5}\n
{0} 老师的今日关键词：\n
{6}
        '''.format(name, user_n, user_chars, user_chars/user_n,
                   len(max_chars), max_chars, my_kw_today)
        return stats


def getCorpus(arg='today', puid: str=None):
    '''
    :param `today`: `list` return a list of dict like
    {'serial': '164',
    'user': 'ch',
    'date': '20180615',
    'time': 1528996039.0,
    'type': 'Text',
    'text': '回不来了，已经晚了'}
    :param `raw_today`: `str` return everything people said today
    :param `raw_alltime`: `str` return everything people said since day0
    :param `raw_puid_today`: `str` return everything a certain dude said today
    '''
    with open('db', 'r') as f:
        all_dict = f.read().split('\n')
    all_dict.remove('')
    # today for instance: `20180615`
    today = formatToday()
    corpus_today = [eval(item.split(' = ')[1])
                    for item in all_dict if today in item.split(' = ')[0]]
    if arg == 'today':
        return corpus_today
    elif arg == 'raw_today':
        return ''.join(
            [item['text'] for item in corpus_today if item['text'] is not None])
    elif arg == 'raw_alltime':
        corpus_all = [eval(item.split(' = ')[1]) for item in all_dict]
        return ''.join(
            [item['text'] for item in corpus_all if item['text'] is not None])
    elif arg == 'raw_puid_today':
        name = getUserByPuid(puid)
        user_corpus = [item for item in corpus_today if item['user'] == name]
        user_texts = [item['text']
                      for item in user_corpus if item['text'] is not None]
        return ''.join(user_texts)


def groupKeyword(arg: str='today') -> str:
    corpus = ''
    if arg == 'today':
        corpus = getCorpus('raw_today')
    elif arg == 'alltime':
        corpus = getCorpus('raw_alltime')
    kw = jieba.analyse.textrank(
        corpus, topK=20, withWeight=False, allowPOS=('ns', 'n'))
    return '\n'.join(kw)


def persistize(msg):
    hoy = formatToday()
    serial = genMsgId()
    content = {}
    content['serial'] = serial
    content['user'] = getUserByPuid(msg.member.puid)
    content['date'] = hoy
    content['time'] = msg.create_time.timestamp()
    content['type'] = msg.type
    content['text'] = msg.text

    msg_name = 'msg{}_{}'.format(hoy, serial)
    with open('db', 'a') as f:
        f.write(msg_name + ' = ' + str(content) + '\n')
    print(msg_name + ' saved.')
    return True


def getQuery(msg: Message) -> list:
    '''
    return a list of puid: str, like
    ['01f0700d', 73b7c671']
    '''
    names = msg.text.replace('\u2005', '').split('@')[2:]
    if names:
        return [the_group.search(name)[0].puid for name in names]
    elif '\u2005' in msg.text:
        return msg.text.split('\u2005')[1]
    else:
        return msg.text.split(' ')[-1]


def isPuid(queries):
    if isinstance(queries, list):
        for query in queries:
            if str(eval('0x'+query)).isdigit():
                return True
    else:
        return False


@bot.register(Group, None, except_self=False)
def deal(msg):

    youshan = getNamePuidDict()

    # detect if gc puid changed
    if msg.member.puid not in list(youshan.values()):
        youshan['gc'] = msg.member.pu

    time.sleep(1)
    if msg.chat.puid == the_group.puid:
        print(msg)
        persistize(msg)

        if msg.is_at:
            # queries: `['154f50b4', '30b3c33f9']`
            queries = getQuery(msg)
            if not queries:
                the_group.send(stats())
            elif '今日关键词' in queries:
                the_group.send(groupKeyword('today'))
            elif '全部关键词' in queries:
                the_group.send(groupKeyword('alltime'))
            elif '我的统计' in queries:
                the_group.send(stats(msg.member.puid))
            elif '群统计' in queries:
                the_group.send(stats())
            elif isPuid(queries):
                for query in queries:
                    # :query: `puid`: str
                    the_group.send(stats(query))
            else:
                the_group.send('你想干啥？')
