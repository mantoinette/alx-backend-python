import aiosqlite
import asyncio

class ExecuteQuery:
    def __init__(self, query, param=None):
        self.query = query
        self.param = param
        self.connection = None  # Placeholder for database connection

    async def __aenter__(self):
        # Establish the database connection here
        self.connection = await aiosqlite.connect('your_database.db')  # Replace with your database path
        return await self.execute_query()  # Execute the query and return the result

    async def __aexit__(self, exc_type, exc_value, traceback):
        # Close the database connection here
        if self.connection:
            await self.connection.close()  # Ensure the connection is closed

    async def execute_query(self):
        async with self.connection.execute(self.query, (self.param,)) as cursor:
            return await cursor.fetchall()  # Fetch all results

async def async_fetch_users():
    async with ExecuteQuery("SELECT * FROM users") as result:
        return result

async def async_fetch_older_users():
    async with ExecuteQuery("SELECT * FROM users WHERE age > ?", 40) as result:
        return result

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", users)
    print("Users Older Than 40:", older_users)

# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
