from aiogram.dispatcher.filters.state import State , StatesGroup

class Category(StatesGroup):
    ctg_menu = State()
    prods_about = State()

class Order(StatesGroup):
    order = State()
    final = State()

class Registr(StatesGroup):
    name = State()
    fullname = State()
    age = State()
    location = State()
