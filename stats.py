
def stats(puid: str=None) -> str:
    corpus_today = getCorpus('today')
    today_n = len(corpus_today)
    if not puid:
        sds = {}
        sd_names = list(youshan)
        sd_names.pop(0)
        sd_rank = {}
        for sd in sd_names:
            sds[sd] = [item for item in corpus_today if item['user'] is sd]
            sd_rank[sd] = len(sds[sd])
        sd_rank = {value: key for key, value in sd_rank.items()}
        sd_rank = SortedDict(sd_rank)

        # build chart
        chart_title = '今天贵群刷了{}条:\n'.format(today_n)
        charts = []
        sd_rank_list = list(sd_rank)
        sd_name_list = list(sd_rank.values())
        for i in range(len(sd_names)):
            chart_content = '#{} {} 老师 {} 条'.format(
                i+1, sd_name_list.pop(), sd_rank_list.pop())
            charts.append(chart_content)
        chart = chart_title + '\n'.join(charts)
        return chart
    elif puid:
        name = getUserByPuid(puid)
        user_corpus = [item for item in corpus_today if item['user'] == name]
        user_n = len(user_corpus)
        user_texts = [item['text']
                      for item in user_corpus if item['text'] is not None]
        max_chars = ''
        for item in user_texts:
            if len(item) > len(max_chars):
                max_chars = item

        user_chars = sum(len(item) for item in user_texts)

        my_kw_today = '\n'.join(jieba.analyse.textrank(
            getCorpus('raw_puid_today', puid), topK=10, withWeight=False, allowPOS=('ns', 'n')))

        stats = '''{0} 老师今天刷了 {1} 条，共 {2} 字
平均每条 {3:.2f} 字
最长一条 {4} 字，内容如下：
{5}\n
{0} 老师的今日关键词：\n
{6}
        '''.format(name, user_n, user_chars, user_chars/user_n,
                   len(max_chars), max_chars, my_kw_today)
        return stats
