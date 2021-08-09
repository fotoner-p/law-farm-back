from databases import Database
from schemas import db_config


class database:
    def __init__(self):
        self.base: Database = Database(f'mysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}/{db_config["db"]}')

    async def execute(self, query, args=None):
        await self.base.execute(query, args)

    async def executeOne(self, query, args=None):
        row = await self.base.fetch_one(query, args)
        return row

    async def executeAll(self, query, args=None):
        rows = await self.base.fetch_all(query, args)
        return rows

