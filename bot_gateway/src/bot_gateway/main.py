from fastapi import FastAPI

from bot_gateway.api.v1 import webhook
from bot_gateway.bot.main import bot
from bot_gateway.core.config import settings

app = FastAPI()

app.include_router(webhook.router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != f"{settings.WEBHOOK_HOST}/api/v1/{settings.TELEGRAM_BOT_TOKEN}":
        await bot.set_webhook(
            url=f"{settings.WEBHOOK_HOST}/api/v1/{settings.TELEGRAM_BOT_TOKEN}",
            secret_token=settings.TELEGRAM_SECRET_TOKEN,
        )


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()