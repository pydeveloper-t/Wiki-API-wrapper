class Database():
    def __init__(self, *, dsn=None, host=None, port=None, database=None, user=None, password=None):
        self.dsn = dsn
        self.host =  host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    @staticmethod
    def convert_none(dct):
        return {k: '' if v is None else v for k, v in dct.items()}
