import os
import sys
import yaml
from collections import namedtuple
from wiki_cashe.db.databases.redis import Redis
from wiki_cashe.db.databases.postgresql import Postgresql
import logging;
logger = logging.getLogger('DATA')

class Data(object):
    @staticmethod
    def get_os_environment():
        config = namedtuple('Config', ['type', 'host', 'port', 'database', 'user', 'password'])
        _type, _host, _port, _database, _user, _password = (None, None, None, None, None, None, )
        if _type in ('REDIS', 'POSTGRESQL'):
            _host = os.getenv(f"{_type}_HOST", None)
            _port = os.getenv(f"{_type}_PORT", None)
            _database = os.getenv(f"{_type}_DATABASE", None)
            _user = os.getenv(f"{_type}_USER", None)
            _password = os.getenv(f"{_type}_PASSWORD", None)
        return config(_type, _host, _port, _database, _user, _password)

    @staticmethod
    def get_configuration():
        config = Data.get_os_environment()
        if all(config):
            return config
        else:
            dir_pth = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(dir_pth, 'config.yaml')
            try:
                with open(full_path) as f:
                    config = yaml.safe_load(f)
            except Exception as exc:
                msg = f'Could not open configuration file "{full_path}". Exception: {exc}'
                logger.fatal(msg)
                raise Exception(msg)
            try:
                _type = config['general']['db_type'].lower()
                _host = config['general']['db'][_type]['host']
                _port = config['general']['db'][_type]['port']
                _database = config['general']['db'][_type]['database']
                _user = config['general']['db'][_type]['user']
                _password = config['general']['db'][_type]['password']
                if all((_type, _host, _port, _database, _user, _password,)):
                    return config(_type, _host, _port, _database, _user, _password)
                else:
                    return config(None, None, None, None, None, None, )
            except Exception as exc:
                msg = f'Could not process configuration file "{full_path}". Exception: {exc}'
                logger.fatal(msg)
                raise Exception(msg)

    @classmethod
    def data_pipeline(cls, settings):
        data_obj = None
        if settings.use_db in ('redis', 'postgresql'):
            if settings.use_db == 'redis':
                data_obj = Redis(dsn=settings.redis_dsn)
            elif settings.use_db == 'postgresql':
                data_obj = Postgresql(dsn=settings.postgres_dsn)
        return data_obj