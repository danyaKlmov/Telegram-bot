rss_news_channels = {
    'habr.com': 'https://habr.com/ru/rss/news/?fl=ru',
    'rbc.ru': 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss',
    'ria.ru': 'https://ria.ru/export/rss2/archive/index.xml',
    '1prime.ru': 'https://1prime.ru/export/rss2/index.xml',
    'interfax.ru': 'https://www.interfax.ru/rss.asp',
}

rss_fun_channels = {
    'dtf.ru': 'https://dtf.ru/rss/new',
    'goha.ru': 'https://www.goha.ru/rss/news',
    'bugaga.ru': 'https://bugaga.ru/rss.xml',
    'trinixy.ru': 'https://trinixy.ru/rss.xml',
}

rss_channels = {}
rss_channels.update(rss_fun_channels)
rss_channels.update(rss_news_channels)

news_urls = list(rss_news_channels)
fun_urls = list(rss_fun_channels)
