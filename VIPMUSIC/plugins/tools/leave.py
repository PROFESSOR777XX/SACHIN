import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from VIPMUSIC import app
from VIPMUSIC.misc import SUDOERS

@app.on_message(filters.command(["leave"], prefixes=["/"]) & SUDOERS)
async def leave(_, message: Message):
    chat_id = message.chat.id
    await app.leave_chat(chat_id)
    print(f"ʙᴏᴛ ʜᴀꜱ ʟᴇꜰᴛ ᴛʜᴇ ɢʀᴏᴜᴘ {chat_id}")
