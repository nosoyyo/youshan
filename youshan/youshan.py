import time
from wxpy import Bot, Group

from storage import persistize
from utils import aloha, reLogin
from models import Query, theGroup


DGBUG = True
bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)


@bot.register(Group, None, except_self=False)
def deal(msg):
    group = theGroup.getTheGroup(msg)

    if theGroup(msg.member.group) == group:
        time.sleep(0.5)
        print(msg)
        persistize(msg)
        if msg.is_at:
            query = Query(msg, group)
            query.deliver()
        elif msg.text is not None and Query.isCommand(msg):
            query = Query(msg, group)
            query.deliver()
