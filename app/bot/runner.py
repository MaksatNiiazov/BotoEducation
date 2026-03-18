from __future__ import annotations

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import httpx

from app.core.config import get_settings
from app.core.security import create_user_token


async def register_handlers(dp: Dispatcher) -> None:
    @dp.message(CommandStart())
    async def start(msg: Message) -> None:
        await msg.answer("1) Отправь URL для сокращения\n2) /mylinks для списка твоих ссылок")

    @dp.message(F.text == "/mylinks")
    async def my_links(msg: Message) -> None:
        s = get_settings()
        token = create_user_token(str(msg.from_user.id))
        async with httpx.AsyncClient(base_url=s.base_url, timeout=10) as client:
            r = await client.get("/me/links", headers={"Authorization": f"Bearer {token}"})
        if r.status_code != 200:
            await msg.answer(f"Ошибка: {r.status_code}")
            return
        data = r.json()
        if not data:
            await msg.answer("Ссылок пока нет")
            return
        text = "\n".join([f"{i+1}. {s.base_url.rstrip('/')}/{x['code']} -> {x['url']}" for i, x in enumerate(data[:20])])
        await msg.answer(text)

    @dp.message(F.text.regexp(r"^https?://"))
    async def shorten(msg: Message) -> None:
        s = get_settings()
        token = create_user_token(str(msg.from_user.id))
        async with httpx.AsyncClient(base_url=s.base_url, timeout=10) as client:
            r = await client.post(
                "/shorten",
                json={"url": msg.text},
                headers={"Authorization": f"Bearer {token}"},
            )
        if r.status_code != 201:
            await msg.answer(f"Ошибка: {r.status_code} {r.text}")
            return
        await msg.answer(r.json()["short_url"])


async def run_bot() -> None:
    s = get_settings()
    if not s.bot_token:
        return
    bot = Bot(token=s.bot_token)
    dp = Dispatcher()
    await register_handlers(dp)
    await dp.start_polling(bot)
