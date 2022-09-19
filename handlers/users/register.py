from aiogram import types
from states.States import Registr
from utils.db_api.database import DBcommands
from aiogram.dispatcher import FSMContext
import pprint

db = DBcommands()
from loader import dp

@dp.message_handler(content_types=types.ContentTypes.TEXT,state=Registr.name)
async def get_name(message:types.Message, state: FSMContext ):
    await db.update_user_name(str(message.from_user.id),message.text)
    await message.answer("To'liq ismingizni kiriting:")
    await Registr.next()

@dp.message_handler(content_types=types.ContentTypes.TEXT,state=Registr.fullname)
async def get_name(message:types.Message, state: FSMContext ):
    await db.update_user_fullname(str(message.from_user.id),message.text)
    await message.answer("Yoshingizni kiriting:")
    await Registr.next()


@dp.message_handler(content_types=types.ContentTypes.TEXT,state=Registr.age)
async def get_name(message:types.Message, state: FSMContext ):
    await db.update_user_age(str(message.from_user.id),int(message.text))
    a = await db.get_user_info(str(message.from_user.id))
    await message.answer(f"Ismingiz:{a.full_name}\nYoshingiz:{a.age}")


