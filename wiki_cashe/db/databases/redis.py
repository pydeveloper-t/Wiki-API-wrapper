import aioredis
from wiki_cashe.db.utils.util import ConvertData
from wiki_cashe.db.databases.database import Database
import logging;
logger = logging.getLogger('redis')

class Redis(Database):
    def __init__(self, *, dsn=None, host=None, port=None, database=None, user=None, password=None):
        super().__init__(dsn=dsn, host=host, port=port, database=database, user=user, password=password)
        self.redis_pool = None

    async def connect(self):
        if not self.dsn:
            db = f'/{self.database}' if self.database else ''
            pwd = f'{self.password}@' if self.password else ''
            self.dsn = f'redis://{pwd}{self.host}:{self.port}{db}'
        self.redis_pool = await aioredis.create_redis_pool(self.dsn,minsize=5, maxsize=10)

    @ConvertData
    async def set_value(self, key, value):
        with await self.redis_pool as conn:
            conv_dict = Redis.convert_none(dict(value))
            await conn.hmset_dict(key, conv_dict)

    @ConvertData
    async def get_value(self, key):
        with await self.redis_pool as conn:
            result = await conn.hgetall(key, encoding='utf-8')
            return result

    async def close(self):
        self.redis_pool.close()
        await self.redis_pool.wait_closed()


