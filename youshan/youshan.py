import time
from wxpy import Bot, Group

from models import User, Query, theGroup
from storage import persistize
from stats import stats, getTiming
from youshan import aloha, reLogin
from pbl import leaderboard


DGBUG = True
bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)


@bot.register(Group, None, except_self=False)
def deal(msg):
    the_group = theGroup.getTheGroup(msg)
    # register & init group
    # if msg.text == '开启统计功能':
    #     the_group.send(registerGroup(msg, 'on'))
    # elif msg.text == '关闭统计功能':
    #     the_group.send(registerGroup(msg, 'off'))

    if theGroup(msg.member.group) == the_group:
        print(msg)
        persistize(msg)
        if msg.text is not None and '在吗' in msg.text:
            if Query.isCommand(msg):
                msg.member.group.send(getTiming(User(msg)))
                return
        elif msg.is_at:
            time.sleep(0.5)
            query = Query(msg)
            if '我的统计' in query.command:
                msg.member.group.send(stats(msg, User(msg)))
            elif '群统计' in query.command:
                msg.member.group.send(stats(msg))
            elif '积分榜' in query.command:
                msg.member.group.send(leaderboard(msg))
            else:
                time.sleep(0.5)
                msg.member.group.send('你想干啥？')
