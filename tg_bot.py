import asyncio
import logging
import sys
import os
import json

import aiofiles
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
rebus = os.getenv('REBUS_NAME')
fitok = os.getenv('FITOK_NAME')
listening_album_date = os.getenv('LISTENING_ALBOM')
album_out_date = os.getenv('ALBUM_OUT')
from_chat_id = os.getenv('CHAT_ID_FROM')
message_id_to_forward = int(os.getenv('START_VIDEO_ID'))
audio_id = int(os.getenv('SKIT_ID'))
interview_id = int(os.getenv('INTERVIEW_VIDEO_ID'))
winner_1_id = int(os.getenv('WINNER_1'))
winner_2_id = int(os.getenv('WINNER_2'))
winner_3_id = int(os.getenv('WINNER_3'))
winner_4_id = int(os.getenv('WINNER_4'))
syka_id = int(os.getenv('SYKA_VIDEO_ID'))
xuy_id = int(os.getenv('PENIS_VIDEO_ID'))
pizda_id = int(os.getenv('PENIS_VIDEO_ID'))
album_out_id = int(os.getenv('SITE_ID'))
listening_album_id = int(os.getenv('LISTENING_ID'))
USER_FILE = "start_users.json"
REBUS_FILE = "rebus_users.json"
FITOK_FILE = "fitok_users.json"

rebus_user_list = []
fitok_user_list = []
rebus_count = 0

async def save_users_to_file(users):
    async with aiofiles.open(USER_FILE, 'w') as f:
        await f.write(json.dumps(list(users)))

async def save_rebus_users_to_file(users):
    async with aiofiles.open(REBUS_FILE, 'w') as f:
        await f.write(json.dumps(list(users)))

async def save_fitok_users_to_file(users):
    async with aiofiles.open(FITOK_FILE, 'w') as f:
        await f.write(json.dumps(list(users)))


async def load_users_from_file():
    if os.path.exists(USER_FILE):
        async with aiofiles.open(USER_FILE, 'r') as f:
            contents = await f.read()
            if contents.strip():
                try:
                    return set(json.loads(contents))
                except json.JSONDecodeError:
                    logging.error(f"Error decoding JSON from {USER_FILE}. Returning an empty set.")
                    return set()
            else:
                return set()
    return set()

async def load_rebus_users_from_file():
    if os.path.exists(REBUS_FILE):
        async with aiofiles.open(REBUS_FILE, 'r') as f:
            contents = await f.read()
            if contents.strip():
                try:
                    return set(json.loads(contents))
                except json.JSONDecodeError:
                    logging.error(f"Error decoding JSON from {REBUS_FILE}. Returning an empty set.")
                    return set()
            else:
                return set()
    return set()

async def rebus_func(message, user_id):
    global rebus_count
    chat_id_to_forward_to = message.chat.id
    rebus_set = await load_rebus_users_from_file()
    if user_id not in rebus_user_list and user_id not in rebus_set:
        if rebus_count == 0:
            rebus_count += 1
            rebus_user_list.append(user_id)
            await save_rebus_users_to_file(rebus_user_list)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=winner_1_id)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=audio_id)
        elif rebus_count == 1:
            rebus_count += 1
            rebus_user_list.append(user_id)
            await save_rebus_users_to_file(rebus_user_list)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=winner_2_id)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=audio_id)
        elif rebus_count == 2:
            rebus_count += 1
            rebus_user_list.append(user_id)
            await save_rebus_users_to_file(rebus_user_list)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=winner_3_id)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=audio_id)
        elif rebus_count == 3:
            rebus_count += 1
            rebus_user_list.append(user_id)
            await save_rebus_users_to_file(rebus_user_list)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=winner_4_id)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=audio_id)
        else:
            rebus_user_list.append(user_id)
            await save_rebus_users_to_file(rebus_user_list)
            await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=audio_id)
    else:
        await message.answer('попробуй еще раз')

def convert(date_time):
    format = '%Y-%m-%d %H:%M'
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    if user_id not in start_users:
        start_users.add(user_id)
        await save_users_to_file(start_users)

    chat_id_to_forward_to = message.chat.id
    await message.answer("привет) когда альбом?")
    await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id, message_id=message_id_to_forward)

@dp.message()
async def echo_handler(message: Message) -> None:
    sending_text = (str(message.text)).lower()
    sending_text = sending_text.replace(" ", "")
    user_id = message.from_user.id

    if sending_text == rebus:
        await rebus_func(message, user_id)
    elif sending_text == fitok.lower():
        fitok_user_list.append(user_id)
        await save_fitok_users_to_file(fitok_user_list)
        chat_id_to_forward_to = message.chat.id
        await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id,
                               message_id=interview_id)
    elif sending_text == "сука":
        chat_id_to_forward_to = message.chat.id
        await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id,
                               message_id=syka_id)
    elif sending_text == "хуй":
        chat_id_to_forward_to = message.chat.id
        await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id,
                               message_id=xuy_id)
    elif sending_text == "пизда":
        chat_id_to_forward_to = message.chat.id
        await bot.copy_message(chat_id=chat_id_to_forward_to, from_chat_id=from_chat_id,
                               message_id=pizda_id)
    else:
        await message.answer("попробуй еще раз")

async def present_album_notification(bot: Bot):
    target_time = convert(listening_album_date)

    while True:
        now = datetime.now()
        if now >= target_time:
            for user_id in start_users:
                try:
                    await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=listening_album_id)
                except Exception as e:
                    logging.error(f"Failed to send message to {user_id}: {e}")
            break
        await asyncio.sleep(60)

async def album_notification(bot: Bot):
    target_time = convert(album_out_date)

    while True:
        now = datetime.now()
        if now >= target_time:
            for user_id in start_users:
                try:
                    await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=album_out_id)
                except Exception as e:
                    logging.error(f"Failed to send message to {user_id}: {e}")
            break
        await asyncio.sleep(60)


async def main() -> None:
    global start_users
    start_users = await load_users_from_file()

    asyncio.create_task(present_album_notification(bot))
    asyncio.create_task(album_notification(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
