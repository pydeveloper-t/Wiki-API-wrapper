import json
import asyncpg
from wiki_cashe.db.utils.util import ConvertData
from wiki_cashe.db.databases.database import Database
import logging;
logger = logging.getLogger('postgresdb')

class Postgresql(Database):
    def __init__(self, *, dsn=None, host=None, port=None, database=None, user=None, password=None):
        super().__init__(dsn=dsn, host=host, port=port, database=database, user=user, password=password)
        self.postresql_pool = None

    @staticmethod
    def convert_none(dct):
        return {k: '' if v is None else v for k, v in dct.items()}

    async def connect(self):
        if not self.dsn:
            db = f'/{self.database}' if self.database else ''
            pwd = f'{self.user}:{self.password}@' if self.user and self.password else ''
            self.dsn = f'postgres://{pwd}{self.host}:{self.port}{db}'
        self.postresql_pool = await asyncpg.create_pool(dsn=self.dsn)

    @ConvertData
    async def set_value(self, key, value):
        async with self.postresql_pool.acquire() as connection:
            async with connection.transaction():
                txt_json = json.dumps(value, ensure_ascii=False)

                await connection.execute("insert into scrap.wiki_requests (title, data) values ($1, $2) on conflict (un_title) do update set title  = excluded.title, data = excluded.data", key, txt_json)

    @ConvertData
    async def get_value(self, key):
        async with self.postresql_pool.acquire() as connection:
            async with connection.transaction():
                raw_result = await connection.fetchval(f"select data from scrap.wiki_requests where title = '{key}';")
                result = json.loads(raw_result) if raw_result else {}
                return result

    async def close(self):
        self.postresql_pool.close()





