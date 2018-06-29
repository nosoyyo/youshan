import requests
from uuid import uuid4
from apistar import App, Route

from .. import config
from youshan import aloha, reLogin


def get_QRuuid(self):
    url = config.BASE_URL + '/jslogin'
    params = {
        'appid': 'wx782c26e4c19acffb',
        'hey': 'jude', }
    headers = {'User-Agent': config.USER_AGENT}
    r = self.s.get(url, params=params, headers=headers)
    if '200' in r.text:
        self.uuid = r.text.split('"')[-2]
        return self.uuid


def getBot(yid: str=None):
    from wxpy import Bot
    yid = yid or uuid4().__str__()

    return qr_file


def login():
    s = requests.Session()
    uuid = get_QRuuid()

routes = [
    Route('/', method='GET', handler=getBot),
    Route('/login', method='GET', handler=getBot),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
