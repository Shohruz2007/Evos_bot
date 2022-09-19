from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.database import DBcommands
from loader import dp
from states.States import Registr,Category
from keyboards.inline.buttons_inline import categoriesBtn


db = DBcommands()


category = [
    {
        'name':"Lavash",
        "image":"AgACAgIAAxkBAAIFMWMnNH0PeRvnx52Ees_Uhfbm84BcAAI-vjEbsuxBSaIoInrzZYtlAQADAgADcwADKQQ"
    },
    {
        'name':'Shaurma',
        "image":"None"
    }
        ]
product = [
    {
        "name":"Tovuq goʼshtli qalampir lavash",
        "image":"AgACAgIAAxkBAAIFTWMnQykWYUNtj_M1VD7or__Gp4HyAAJyvjEbsuxBSTih-hYnf6OFAQADAgADcwADKQQ",

    },
    {
        "name":"Mol goʼshtidan qalampir lavash",
        "image":"AgACAgIAAxkBAAIFUGMnQ4m8BQwibgpGn2e2-4W4h89dAAKTxTEbrXooSZq89_KwELlCAQADAgADcwADKQQ"
    },
    {
        "name":"Tovuq goʼshtidan pishloqli lavash",
        "image":"AgACAgIAAxkBAAIFU2MnQ7jTDaTxCPnb2u2-H1GfbCynAAIJvTEb60YoSdKvJQ1mGRlQAQADAgADcwADKQQ"
    },
    {
        "name":"Mol goʼshtidan pishloqli lavash",
        "image":"AgACAgIAAxkBAAIFVmMnQ8wbUZ8I5PMFZXd-QAQ6OheQAAIEvjEbQD4oSctiJzdLFZfmAQADAgADcwADKQQ"
    },
]

@dp.message_handler(CommandStart(),state = '*')
async def bot_start(message: types.Message):
    await db.join_user(str(message.from_user.id))

    

    for i in category:
        await db.add_category(i['name'],i['image'])
        for j in product:
            await db.add_product(j['name'],j['image'])
    
    await message.answer(text='Menyu:',reply_markup=await categoriesBtn())
    await Category.ctg_menu.set()

    # await db.update_user_info(str(message.from_user.id),'Shohruz','Murataliyev',32)
    # await message.answer(f"Salom, {message.from_user.full_name}! Iltimos ismingizni kiriting:")
    # await Registr.name.set()
