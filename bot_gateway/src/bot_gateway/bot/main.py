from aiogram import Bot, Dispatcher
from aiogram.types import Message

from bot_gateway.core.config import settings
from bot_gateway.grpc_clients.auth_service_client import AuthServiceClient

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(commands=["start"])
async def start_handler(message: Message, auth_client: AuthServiceClient = Depends(AuthServiceClient)):
    user = await auth_client.get_user(user_id=message.from_user.id)
    if user:
        await message.answer(f"Hello, {user.username}!")
    else:
        await message.answer("Hello! Please, register.")