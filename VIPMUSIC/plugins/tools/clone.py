import re
import logging
import asyncio
import importlib
from sys import argv
from pyrogram import idle
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import (
    AccessTokenExpired,
    AccessTokenInvalid,
)
from VIPMUSIC.utils.database import get_assistant
from config import API_ID, API_HASH
from VIPMUSIC import app
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.utils.database import get_assistant, clonebotdb
from config import LOGGER_ID

CLONES = set()


@app.on_message(filters.command("cl") & SUDOERS)
async def clone_txt(client, message):
    userbot = await get_assistant(message.chat.id)
    if len(message.command) > 1:
        bot_token = message.text.split("/cl", 1)[1].strip()
        mi = await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ɪ ᴘʀᴏᴄᴇꜱꜱ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ.")
        try:
            ai = Client(
                bot_token,
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="VIPMUSIC.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            bot_users = await ai.get_users(bot.username)
            bot_id = bot_users.id

        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text(
                "ʏᴏᴜ ʜᴀᴠᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴀɴ ɪɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ. ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ."
            )
            return
        except Exception as e:
            await mi.edit_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {str(e)}")
            return

        # Proceed with the cloning process
        await mi.edit_text(
            "ᴄʟᴏɴɪɴɢ ᴘʀᴏᴄᴇꜱꜱ ꜱᴛᴀʀᴛᴇᴅ. ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ʙᴇ ꜱᴛᴀʀᴛ."
        )
        try:

            await app.send_message(
                LOGGER_ID, f"**#ɴᴇᴡ_ᴄʟᴏɴᴇꜱ**\n\n**ʙᴏᴛ:- @{bot.username}**"
            )
            await userbot.send_message(bot.username, "/start")

            details = {
                "ʙᴏᴛ_ɪᴅ": bot.id,
                "ɪꜱ_ʙᴏᴛ": True,
                "ᴜꜱᴇʀ_ɪᴅ": message.from_user.id,
                "ɴᴀᴍᴇ": bot.first_name,
                "ᴛᴏᴋᴇɴ": bot_token,
                "ᴜꜱᴇʀɴᴀᴍᴇ": bot.username,
            }
            clonebotdb.insert_one(details)
            CLONES.add(bot.id)
            await mi.edit_text(
                f"ʙᴏᴛ @{bot.username} ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʟᴏɴᴇᴅ ᴀɴᴅ ꜱᴛᴀʀᴛᴇᴅ ✅.\n**ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇᴅ ʙʏ :- /ᴅᴇʟᴄʟᴏɴᴇ**"
            )
        except BaseException as e:
            logging.exception("ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴄʟᴏɴɪɴɢ ʙᴏᴛ.")
            await mi.edit_text(
                f"⚠️ <b>ᴇʀʀᴏʀ:</b>\n\n<code>{e}</code>\n\n**ᴋɪɴᴅʟʏ ғᴏᴡᴀʀᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ @STORM_CHATZ ᴛᴏ ɢᴇᴛ ᴀssɪsᴛᴀɴᴄᴇ**"
            )
    else:
        await message.reply_text(
            "**ɢɪᴠᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀꜰᴛᴇʀ /ᴄʟᴏɴᴇ ᴄᴏᴍᴍᴀɴᴅ ꜰʀᴏᴍ @ʙᴏᴛꜰᴀᴛʜᴇʀ.**"
        )


@app.on_message(
    filters.command(
        [
            "deletecloned",
            "delcloned",
            "delclone",
            "deleteclone",
            "removeclone",
            "cancelclone",
        ]
    )
)
async def delete_cloned_bot(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "**⚠️ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀꜰᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.**"
            )
            return

        bot_token = " ".join(message.command[1:])
        await message.reply_text("ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ...")

        cloned_bot = clonebotdb.find_one({"token": bot_token})
        if cloned_bot:
            clonebotdb.delete_one({"token": bot_token})
            CLONES.remove(cloned_bot["bot_id"])
            await message.reply_text(
                "**🤖 ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴄᴏɴɴᴇᴄᴛᴇᴅ ꜰʀᴏᴍ ᴍʏ ꜱᴇʀᴠᴇʀ ☠️\nᴄʟᴏɴᴇ ʙʏ : /clone**"
            )
            await restart_bots()
            # Call restart function here after successful deletion
        else:
            await message.reply_text(
                "**⚠️ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪꜱ ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪꜱᴛ.**"
            )
    except Exception as e:
        await message.reply_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛ.")
        logging.exception(e)


async def restart_bots():
    global CLONES
    try:
        logging.info("ʀᴇꜱᴛᴀʀᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ........")
        bots = list(clonebotdb.find())
        for bot in bots:
            bot_token = bot["token"]
            ai = Client(
                f"{bot_token}",
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="VIPMUSIC.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            if bot.id not in CLONES:
                try:
                    CLONES.add(bot.id)
                except Exception:
                    pass
    except Exception as e:
        logging.exception("ᴇʀʀᴏʀ ᴡʜɪʟᴇ ʀᴇꜱᴛᴀʀᴛɪɴɢ ʙᴏᴛꜱ.")


@app.on_message(filters.command("cloned") & SUDOERS)
async def list_cloned_bots(client, message):
    try:
        cloned_bots = list(clonebotdb.find())
        if not cloned_bots:
            await message.reply_text("ɴᴏ ʙᴏᴛꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʟᴏɴᴇᴅ ʏᴇᴛ.")
            return

        total_clones = len(cloned_bots)
        text = f"**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ: {total_clones}**\n\n"

        for bot in cloned_bots:
            text += f"**ʙᴏᴛ ɪᴅ:** {bot['bot_id']}\n"
            text += f"**ʙᴏᴛ ɴᴀᴍᴇ:** {bot['name']}\n"
            text += f"**ʙᴏᴛ ᴜꜱᴇʀɴᴀᴍᴇ:** @{bot['username']}\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʟɪꜱᴛɪɴɢ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ.")


@app.on_message(filters.command("delallclone") & SUDOERS)
async def delete_all_cloned_bots(client, message):
    try:
        await message.reply_text("ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ...")

        # Delete all cloned bots from the database
        clonebotdb.delete_many({})

        # Clear the CLONES set
        CLONES.clear()

        await message.reply_text("ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.")
    except Exception as e:
        await message.reply_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ.")
        logging.exception(e)
