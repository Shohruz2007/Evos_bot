from subprocess import call
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from utils.db_api.database import DBcommands

db = DBcommands()

async def categoriesBtn():
    cats = await db.get_categories()
    Cats = InlineKeyboardMarkup(row_width=2)
    for i in cats:
        Cats.insert(InlineKeyboardButton(i.name,callback_data=f'{i.id}'))
    Cats.add(InlineKeyboardButton('📥 Savat',callback_data='orders_list'))
    return Cats

async def productsBtn(cat_id):
    pds = await db.get_products(cat_id)
    Prds = InlineKeyboardMarkup(row_width=2)
    for i in pds:
        Prds.insert(InlineKeyboardButton(i.name,callback_data=f'{i.id}'))
    Prds.add(InlineKeyboardButton('◀️ Back', callback_data="back"))
    return Prds

async def order_quantityBtn(quantity = 1):
    order_quantity = InlineKeyboardMarkup(row_width=3)
    order_quantity.insert(InlineKeyboardButton('-', callback_data=f"down"))
    order_quantity.insert(InlineKeyboardButton(quantity, callback_data=f"{quantity}"))
    order_quantity.insert(InlineKeyboardButton('+', callback_data=f"up"))
    order_quantity.add(InlineKeyboardButton(text="📥 Savatga qo'shish", callback_data='order'))
    return order_quantity

async def orderBtn(id):
    forder = InlineKeyboardMarkup(row_width=2)
    forder.insert(InlineKeyboardButton('◀️ Back', callback_data=f"back"))
    forder.insert(InlineKeyboardButton('🚖 Buyurtma berish', callback_data=f"finish_ord"))
    forder.insert(InlineKeyboardButton('🗑 Savatni tozalash', callback_data=f"clr"))
    forder.insert(InlineKeyboardButton('⏳ Yetkazib berish vaqti', callback_data=f"ord_time"))
    ords = await db.get_orders(id)
    for i in ords:
        forder.add(InlineKeyboardButton(f"❌ {i.pd_name}ni ro'yxatdan olish",callback_data=f'{i.product_id}'))
    return forder

