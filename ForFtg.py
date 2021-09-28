from .. import loader, utils
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


def register(cb):
    cb(TikTokDLMod())

class TikTokDLMod(loader.Module):
    """Скачивает ТикТоки без водяного знака"""
    strings = {'name': 'TikTokDlByVova'}

    async def tiktokcmd(self, message):
        """.tiktok <аргумент или реплай>"""
        chat = "@SaveOFFbot"
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not text and not reply:
            await message.edit("<b>Нет аргумента или реплая</b>")
            return
        await message.edit("<b>Пожалуйста, поождите...</b>")
        async with message.client.conversation(chat) as conv:
            if text:
                try:
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1825028508))
                    await message.client.send_message(chat, text)
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>Разблокируй бота @SaveOFFbot !</b>")
                    return
            else:
                try:
                    user = await utils.get_user(reply)
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1825028508))
                    await message.client.send_message(chat, f"{reply.raw_text} (c) {user.first_name}")
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>Разблокируй бота @SaveOFFbot !</b>")
                    return
        if response.media:
            await message.client.send_file(message.to_id, response.media, reply_to=reply.id if reply else None)
            await message.delete()
        if response.text:
            await message.client.send_message(message.to_id, f"<b> {response.text} </b>")
            await message.delete()
