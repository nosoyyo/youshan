import time

from core import *
from wxpy import *
from stats import stats

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
bot.enable_puid()


@bot.register(Group, None, except_self=False)
def deal(msg):

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
                the_group.send('你整的这是啥？')
