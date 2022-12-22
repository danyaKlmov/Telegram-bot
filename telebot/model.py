from urllib.parse import urlparse

import peewee as pw

from config_reader import config

db = pw.SqliteDatabase(config.db_path)


class Article(pw.Model):
    """
    Таблица в БД, в которой хранятся статьи.
    Храним домен и полный URL,
    с которого её спарсили.
    """
    title = pw.CharField()
    link = pw.CharField()
    domain = pw.CharField()
    publish_date = pw.DateField()

    class Meta:
        constraints = [pw.SQL('UNIQUE("title", "publish_date")')]
        database = db


def create_tables(db: pw.SqliteDatabase):
    """
    Вспомогательная функция для первичного создания таблиц в базе.

    :param db: ранее созданная база данных.
    """
    with db:
        db.create_tables([Article])


def get_by_url(url: str) -> pw.ModelSelect:
    """
    Извлекает из базы статьи,
    имеющие такой же домен, как и переданный URL.

    :param url: URL в формате 'https://mysite.com/some_path
    :return: результат запроса (несколько строк из базы)
    """
    domain = urlparse(url).netloc
    return Article.select().where(Article.domain == domain)