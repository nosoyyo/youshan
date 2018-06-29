import time
from wxpy import Bot


RETRY_LOGIN = 3
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
    for i in range(len(RETRY_LOGIN)):
        bot = Bot(cache_path=True, login_callback=aloha,
                  logout_callback=reLogin)
        if LOGGEDIN:
            break
