import logging
from urllib.parse import urlparse

import aiohttp
from peewee import IntegrityError
from rss_parser import Parser

from model import Article


async def parse(url):
    """
    Собирает информацию с 1 конкретного URL,
    возвращает её в виде текста.

    :param url: URL в виде 'https://mysite.com/some_path
    :return: данные, полученные с указанного URL
    """
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=5)) as session:
        async with session.get(url) as response:
            parser = Parser(xml=await response.text())
    return parser.parse().feed


async def parse_articles(url):
    """
    Собирает всю информацию из конкретной RSS-ленты,
    сохраняет в БД следующие поля:
        - заголовок;
        - дату публикации;
        - ссылку на статью;
        - домен.

    :param url: URL в виде 'https://mysite.com/some_path
    """
    feed = await parse(url)
    for item in reversed(feed):
        try:
            # Цитата из документации, объясняющая, почему не используем async
            # https://docs.peewee-orm.com/en/latest/peewee/database.html
            # SQLite, because it is embedded in the Python
            # application itself, does not do any socket operations
            # that would be a candidate for non-blocking.
            # Async has no effect one way or the other on SQLite databases.
            Article.create(
                title=item.title,
                link=item.link,
                domain=urlparse(item.link).netloc,
                publish_date=item.publish_date,
            )
        except IntegrityError:
            ...


async def parse_all(urls):
    for url in urls:
        try:
            await parse_articles(url)
        except Exception as e:
            logging.exception(e)

