from .. import User

with open('db', 'r') as f:
    all_corpus = f.read()
all_corpus = all_corpus.split('\n')
all_corpus = [item for item in all_corpus if item]


def trim(item):
    if item is not None:
        return eval(item.split(' = ')[1])


dicts = [trim(item) for item in all_corpus]
ul = [User(u) for u in User.group.members]


for item in dicts:
    for u in ul:
        # manually set `曾用名`
        if item['user'] in u.cym:
            # `故纸堆`
            u.gzd[item['time']] = item['text']
