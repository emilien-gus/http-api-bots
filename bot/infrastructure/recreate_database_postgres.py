import asyncio
from bot.infrastructure.storage_postgres import StoragePostgres


async def main():
    storage = StoragePostgres()
    try:
        await storage.recreate_db()
        print("✅ Database recreated successfully")
    finally:
        await storage.close()


if __name__ == "__main__":
    asyncio.run(main())
