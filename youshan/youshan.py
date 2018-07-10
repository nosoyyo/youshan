import time
from wxpy import Bot, Group

from history import History
from storage import persistize
from stats import stats, getTiming
from utils import aloha, reLogin
from models import User, Query, theGroup
from pbl import leaderboard, scoreDetails


DGBUG = True
bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)


@bot.register(Group, None, except_self=False)
def deal(msg):
    group = theGroup.getTheGroup(msg)
    group.send = msg.member.group.send
    # register & init group
    # if msg.text == '开启统计功能':
    #     group.send(registerGroup(msg, 'on'))
    # elif msg.text == '关闭统计功能':
    #     group.send(registerGroup(msg, 'off'))

    if theGroup(msg.member.group) == group:
        time.sleep(0.5)
        print(msg)
        persistize(msg)
        if msg.text is not None and '在吗' in msg.text:
            if Query.isCommand(msg):
                return getTiming(User(msg))

        elif msg.is_at:
            query = Query(msg)
            if '我的统计' in query.command:
                group.send(stats(msg, User(msg)))
            elif '群统计' in query.command:
                group.send(stats(msg))
            elif '积分榜' in query.command:
                group.send(leaderboard(group, query.day))
            elif '我的积分' in query.command:
                msg.member.send(scoreDetails(User(msg)))
            elif '历史群名' in query.command:
                group.send(History.getHistoryGroupName(group))

            else:
                time.sleep(0.5)
                group.send('你想干啥？')
