import time
from wxpy import Bot, Group

from pbl import Badge
from storage import persistize
from utils import aloha, reLogin
from models import Query, theGroup


DGBUG = True
LATTICE = 300
BADGES_CHECKED_ON = None
bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)


def check_badges(group):
    global BADGES_CHECKED_ON
    for u in group.members:
        Badge(u)
        BADGES_CHECKED_ON = time.time()
    return True


@bot.register(Group, None, except_self=False)
def deal(msg):
    group = theGroup.getTheGroup(msg)

    if theGroup(msg.member.group) == group:
        # check badges every secs
        global BADGES_CHECKED_ON
        if not BADGES_CHECKED_ON:
            check_badges(group)
        elif time.time() - BADGES_CHECKED_ON >= LATTICE:
            check_badges(group)
        else:
            time.sleep(0.5)

        print(msg)
        persistize(msg)
        if msg.is_at:
            query = Query(msg, group)
            query.deliver()
        elif msg.text is not None and Query.isCommand(msg):
            query = Query(msg, group)
            query.deliver()
