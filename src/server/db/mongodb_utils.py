import logging

from motor.motor_asyncio import AsyncIOMotorClient

from src.server.core.config import ConfigManager
from src.server.db.mongodb import db


config = ConfigManager(echo=True)


async def connect_to_mongo():
    logging.info("Connect to the database...")
    db.client = AsyncIOMotorClient(
        str(config.mongo["MONGODB_URL"]),
        minPoolSize=int(config.mongo["MIN_CONNECTIONS_COUNT"]),
        maxPoolSize=int(config.mongo["MAX_CONNECTIONS_COUNT"]),
    )
    logging.info("Successfully connected to the database!")


async def close_mongo_connection():
    logging.info("Close database connection...")
    db.client.close()
    logging.info("The database connection is closed!")
