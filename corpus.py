from youshan import formatToday, getUserByPuid


class Corpus():

    def __init__(self, puid: str=None):
        with open('db', 'r') as f:
            all_dict = f.read().split('\n')
        all_dict.remove('')
        today = formatToday()
        self.today = [eval(item.split(' = ')[1])
                      for item in all_dict if today in item.split(' = ')[0]]
        self.raw_today = ''.join(
            [item['text'] for item in self.today if item['text'] is not None])
        self.alltime = [eval(item.split(' = ')[1]) for item in all_dict]
        self.raw_alltime = ''.join(
            [item['text'] for item in self.alltime
             if item['text'] is not None])
        if puid:
            self.puid = puid
            self.puid_today = [
                m for m in self.today if m['user'] == getUserByPuid(puid)]
            self.raw_puid_today = ''.join([item['text']
                                           for item in self.puid_today
                                           if item['text'] is not None])
