from databases import Database
from schemas import DB_ENV


class LegacyDatabase:
    def __init__(self):
        self.base: Database = Database(f'mysql://{DB_ENV["user"]}:{DB_ENV["password"]}@{DB_ENV["host"]}/{DB_ENV["db"]}')

    async def execute(self, query, args=None):
        await self.base.execute(query, args)

    async def executeOne(self, query, args=None):
        row = await self.base.fetch_one(query, args)
        return row

    async def executeAll(self, query, args=None):
        rows = await self.base.fetch_all(query, args)
        return rows

