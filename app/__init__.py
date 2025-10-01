import asyncio
import motor.motor_asyncio
from beanie import init_beanie

from . import config
from app.model.user import User
from app.model.auth import TokenData

app_settings = config.get_app_settings()
auth_settings = config.get_auth_settings()
db_settings = config.get_db_settings()


# init log setup
config.setup_log_settings()


client = motor.motor_asyncio.AsyncIOMotorClient(db_settings.mongo_uri)
db = client[db_settings.mongo_db]
motorcon = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)
# beanie connection
async def initialize_beanie():
    client.get_io_loop = asyncio.get_event_loop
    await init_beanie(
        database=client[db_settings.mongo_db],
        document_models=[
            User,
            TokenData,
        ],
    )