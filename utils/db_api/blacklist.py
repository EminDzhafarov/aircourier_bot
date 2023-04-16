from db import


async def add_category(name: str):
    sql = "INSERT INTO categories (name) VALUES ($1)"
    await db.pool.execute(sql, name)
