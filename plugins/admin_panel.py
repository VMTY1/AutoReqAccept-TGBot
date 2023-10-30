from config import Config
from helper.database import add_user, add_group, all_users, all_groups, users, remove_user
from pyrogram.types import Message
from pyrogram.types import ChatJoinRequest, Message, ChatMemberUpdated
from pyrogram.errors import UserNotParticipant
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os
import sys
import time
import asyncio
import logging
import datetime
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.OWNER))
async def get_stats(bot, message):
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(
        time.time() - Config.BOT_UPTIME))
    start_t = time.time()
    st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ`\n\n**🍀 Chats Stats 🍀**\n**🙋‍♂️ Users :** `{xx}`\n**👥 Groups :** `{x}`\n**🚧 Total users & groups :** `{tot}`")
    

# Restart to cancell all process
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.OWNER))
async def restart_bot(b, m):
    await m.reply_text("🔄__Rᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("broadcast") & filters.user(Config.OWNER) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......")
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "broadcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")


@Client.on_chat_join_request()
async def autoAccept(bot: Client, cmd: ChatJoinRequest):
    chat = cmd.chat  # chat
    user = cmd.from_user  # user

    # Accepting Request of User ✅
    try:
        await bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        add_group(cmd.chat.id)
        add_user(user.id)
        bool_approve_msg = await db.get_bool_approve_msg(Config.OWNER)

        if bool_approve_msg:
            _param = await db.get_approve_msg(Config.OWNER)

            if _param:
                await bot.send_message(chat_id=user.id, text=_param.format(mention=user.mention, title=chat.title))
            else:
                await bot.send_message(chat_id=user.id, text=Config.APPROVED_WELCOME_TEXT.format(mention=user.mention, title=chat.title))
        else:
            print('Approval Message Is Disabled By Admin ❌')

        await asyncio.sleep(1)

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_chat_member_updated()
async def Upade(bot: Client, cmd: ChatMemberUpdated):
    chat = cmd.chat
    user = cmd.from_user

    # Sending Message those user who left the chat ✅
    try:
    
        ms = await bot.get_chat_member(chat_id=chat.id, user_id=user.id)
        print(ms.status)
    except UserNotParticipant:
        bool_leave = await db.get_bool_leave_msg(Config.OWNER)

        if bool_leave:
            leavemsg = await db.get_leave_msg(Config.OWNER)
            print(leavemsg)
            if leavemsg:
                await bot.send_message(chat_id=user.id, text=leavemsg.format(mention=user.mention, title=chat.title))

            else:
                await bot.send_message(chat_id=user.id, text=Config.LEAVING_BY_TEXT.format(mention=user.mention, title=chat.title))
        else:
            print('Leave Message is Disabled By Admin ❌')

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
