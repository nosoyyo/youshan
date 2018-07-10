import time
from wxpy import Bot, Group

from storage import persistize
from utils import aloha, reLogin
from models import User, Query, theGroup
from stats import getTiming


DGBUG = True
bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)


@bot.register(Group, None, except_self=False)
def deal(msg):
    group = theGroup.getTheGroup(msg)
    # register & init group
    # if msg.text == '开启统计功能':
    #     group.send(registerGroup(msg, 'on'))
    # elif msg.text == '关闭统计功能':
    #     group.send(registerGroup(msg, 'off'))

    if theGroup(msg.member.group) == group:
        time.sleep(0.5)
        print(msg)
        persistize(msg)
        if msg.is_at:
            query = Query(msg, group)
            query.deliver()
        elif msg.text is not None and '在吗' in msg.text:
            if Query.isCommand(msg):
                return getTiming(User(msg))
