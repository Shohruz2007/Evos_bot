from ast import And
from itertools import product
from gino import Gino
from data.config import DB_HOST,DB_NAME,DB_PASS,DB_USER
from aiogram import types

db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.String)
    username = db.Column(db.String)
    full_name = db.Column(db.String)
    age = db.Column(db.Integer)
    location = db.Column(db.String)
    # time = db.Column(db.DateTime)
    # phone = db.Column(db.String)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    # discreption = db.Column(db.String)
    image = db.Column(db.String)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))

class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    # ord_time = db.Column(db.String)
    us_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    pd_name = db.Column(db.String)





class DBcommands():
    async def join_user(self,tg_id):
        if not await self.get_user(tg_id):
            await User.create(tg_id = tg_id)


    async def update_user_name(self, tg_id, username):
        user = await User.query.where(User.tg_id==tg_id).gino.first()
        await user.update(username=username).apply()
        return
    
    async def update_user_fullname(self,tg_id,fullname):
        user = await User.query.where(User.tg_id==tg_id).gino.first()
        await user.update(full_name=fullname).apply()
        return

    async def update_user_age(self,tg_id,age):
        user = await User.query.where(User.tg_id==tg_id).gino.first()
        await user.update(age=age).apply()
        return

    async def get_user(self, tg_id):
        user = await User.query.where(User.tg_id==tg_id).gino.first()
        if user:
            return True
        return False

    async def get_user_info(self, tg_id):
        user = await User.query.where(User.tg_id==tg_id).gino.first()
        return user
    
    # '2 DARS'
    async def add_category(self,name,image):
        if not await Category.query.where(Category.name==name).gino.all():
            category = await Category.create(name=name,image=image)
            return category.id
    
    async def add_order(self,product_id,user_id,quantity,pd_name):
        if not await Card.query.where(Card.us_id==user_id).gino.all():
            if not await Card.query.where(Card.product_id==product_id).gino.all():
                order = await Card.create(product_id = product_id,us_id=user_id,quantity=quantity,pd_name=pd_name)
        else:
            if await Card.query.where(Card.product_id==product_id).gino.all():
                old_order = await Card.query.where(Card.us_id==id and Card.product_id==product_id).gino.first()
                quanty = old_order.quantity
                await old_order.update(quantity=quantity+quanty).apply()
            else:
                order = await Card.create(product_id = product_id,us_id=id,quantity=quantity,pd_name=pd_name)


    async def add_product(self,name,image):
        if not await Product.query.where(Product.name == name).gino.all():
            await Product.create(name=name,image=image,category_id=1,price=23000)
    
    async def get_categories(self):
        cats = await Category.query.gino.all()
        return cats
        
    async def get_category(self,id):
        cat = await Category.query.where(Category.id==id).gino.first()
        return cat
        
    async def get_products(self,cat_id):
        pds = await Product.query.where(Product.category_id==int(cat_id)).gino.all()
        return pds

    async def get_product(self,id):
        pd = await Product.query.where(Product.id==id).gino.first()
        return pd
    async def get_orders(self,id):
        ord = await Card.query.where(Card.us_id==id).gino.all()
        return ord
    async def del_orders(self):
        await Card.delete.gino.status()
    async def del_order(self,pd_name):
        await Card.delete.where(Card.pd_name == pd_name).gino.status()
    async def check_orders(self,id):
        ord = await Card.query.where(Card.us_id==id).gino.all()
        try:
            ord.pd_name
            return True
        except:
            return False

    # async def add_user(self):
    #     user = types.User.get_current()
    #     old_user  = await self.get_user(str(user.id))
    #     if old_user:
    #         return old_user
    #     new_user = User()
    #     new_user.tg_id = str(user.id)
    #     await new_user.create()
    #     return 

# class category(db.Model):
#     __tablename__ = 'category'

#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String)

# class Product(db.Model):
#     __tablename__='products'

#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String)
#     category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))



async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    # await db.gino.create_all()
    # await db.gino.drop_all()