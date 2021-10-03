from .. import loader, utils
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from asyncio.exceptions import TimeoutError

def register(cb):
    cb(VoiceVMOD(cb))

class VoiceVMOD(loader.Module):
    """Send voice from you`re text"""
    strings = {"name": "VoiceVMOD"}

    async def vftsndcmd(self, message):
        """Use .vftsnd {args or reply}"""
        try:
            text = utils.get_args_raw(message)
            reply = await message.get_reply_message()
            chat = "@aleksobot"
            if not text and not reply:
                await message.edit("<b>No reply or args</b>")
                return
            if text:
                await message.edit("<b>Whait a minute...</b>")
                async with message.client.conversation(chat) as conv:
                    try:
                        response = conv.whait_event(events.NewMessage(incoming=True, from_users=616484527))
                        await message.client.send_message(chat, text)
                        response = await response
                    except YouBlockedUserError:
                        await message.edit("You blocked @aleksobot")
                        return
                    if not response.voice:
                        response = conv.whait_event(events.NewMessage(incoming=True, from_users=616484527))
                        await message.client.send_message(chat, text)
                        response = await response
                    await message.delete()
                    await message.client.send_message(message.to_id, response.voice)
            if reply:
                await message.edit("<b>Whait a minute...</b>")
                async with message.client.conversation(chat) as conv:
                    try:
                        response = conv.whait_event(events.NewMessage(incoming=True, from_users=616484527))
                        await message.client.send_message(chat, reply)
                        response = await response
                    except YouBlockedUserError:
                        await message.edit("You blocked @aleksobot")
                        return
                    if not response.voice:
                        response = conv.whait_event(events.NewMessage(incoming=True, from_users=616484527))
                        await message.client.send_message(chat, reply)
                        response = await response
                    await message.delete()
                    await message.client.send_message(message.to_id, response.voice)
        except TimeoutError:
            return await message.edit("<b>Time out. Bot is death or you are invalid</b>")
