from psycopg import AsyncConnection


class Request:
    def __init__(self, connector: AsyncConnection):
        self.connector = connector

    async def add_user(self, user_id: int):
        query = "INSERT INTO users (user_id)" \
                "VALUES (%s)" \
                "ON CONFLICT (user_id) " \
                "DO NOTHING"
        async with self.connector.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            await self.connector.commit()

    async def create_table_sender(self, name_table: str):
        drop_query = f"DROP TABLE IF EXISTS {name_table};"
        create_query = f"CREATE TABLE {name_table}" \
                       f"(user_id bigint NOT NULL, status text, description text," \
                       f"PRIMARY KEY (user_id));"
        insert_query = f"INSERT INTO {name_table} (user_id, status, description)" \
                       f"SELECT users.user_id, 'waiting', null FROM users;"

        async with self.connector.cursor() as cursor:
            await cursor.execute(drop_query)
            await self.connector.commit()
            await cursor.execute(create_query)
            await self.connector.commit()
            await cursor.execute(insert_query)
            await self.connector.commit()

    async def get_count_sender(self, name_company):
        query = f"SELECT COUNT(*) FROM {name_company}"
        async with self.connector.cursor() as cursor:
            await cursor.execute(query)
            results = await cursor.fetchone()
            await self.connector.commit()
        return results[0]

    async def delete_table(self, name_table):
        query = f"DROP TABLE {name_table};"
        async with self.connector.cursor() as cursor:
            await cursor.execute(query)
            await self.connector.commit()

    async def get_users(self, name_company: str):
        query = f'SELECT user_id FROM {name_company} WHERE status = %s'
        async with self.connector.cursor() as cursor:
            await cursor.execute(query, ('waiting', ))
            results = await cursor.fetchall()
            user_ids = [result[0] for result in results]
        return user_ids
