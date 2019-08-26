from os.path import dirname, join

import dotenv


class Settings:
    def __init__(self, client, filename='.env'):
        envpath = join(dirname(__file__), filename)
        dotenv.load_dotenv(envpath)
        self.ES_CLIENT = client
