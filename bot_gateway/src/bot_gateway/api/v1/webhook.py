from aiogram import Bot, Dispatcher, types
from fastapi import APIRouter, Depends, Header
from starlette.requests import Request

from bot_gateway.bot.main import bot, dp
from bot_gateway.core.config import settings

router = APIRouter()


@router.post(f"/{settings.TELEGRAM_BOT_TOKEN}")
async def webhook(request: Request, x_telegram_bot_api_secret_token: str = Header(None)):
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        return {"status": "Forbidden"}, 403

    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot=bot, update=update)
    return {"status": "ok"}