from ast import Delete
from aiogram import types
from keyboards.inline.buttons_inline import productsBtn,order_quantityBtn,orderBtn
from utils.db_api.database import DBcommands
from loader import dp
from states.States import Registr,Category,Order
from keyboards.inline.buttons_inline import categoriesBtn
from aiogram.dispatcher import FSMContext


db = DBcommands()

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def get_photo(message:types.Message):
        await message.reply(text=message.photo[0].file_id)
        await message.answer_photo(photo="AgACAgIAAxkBAAIFMWMnNH0PeRvnx52Ees_Uhfbm84BcAAI-vjEbsuxBSaIoInrzZYtlAQADAgADcwADKQQ")

@dp.callback_query_handler(state=Category.ctg_menu)
async def make_menu(call = types.CallbackQuery,state = FSMContext):
    
    if call.data == 'orders_list':
        
        await call.message.delete()
        ords = await db.get_orders(int(call.message.chat.id))
        sum = 0
        a = ''
        for i in ords:
            pd = await db.get_product(i.product_id)
            sum = sum + pd.price*i.quantity
            await state.update_data({
                'product':f"{i.quantity} ✖️ {i.pd_name}\n"
            })
            sdata = await state.get_data()
            a += sdata['product']
        
        await call.message.answer(text=f"Savatda:\n{a}Mahsulotlar: {sum} so'm\nYetkazib berish: 10 000 so'm\nJami: {sum+10000} so'm",reply_markup=await orderBtn(call.message.chat.id))
        await Order.final.set()
        await sdata.finish()
        return

    await call.message.delete()
    cat = await db.get_category(int(call.data))
    await call.message.answer_photo(photo=cat.image,caption=f"{cat.name}lardan birontasini xohlaysizmi?",reply_markup=await productsBtn(int(cat.id)))
    await Category.prods_about.set()

@dp.callback_query_handler(state=Category.prods_about)
async def prods(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await call.message.delete()
        await call.message.answer(text='Menyu:',reply_markup=await categoriesBtn())
        await Category.ctg_menu.set()
        return
    await call.message.delete()
    pd = await db.get_product(int(call.data))

    await state.update_data({
        'pd_id':pd.id,
        'quantity':1,
        'price':pd.price,
        'name':pd.name
    })
    quantity = 1
    await call.message.answer_photo(photo=pd.image, caption=f"{pd.name}", reply_markup=await order_quantityBtn(quantity))
    await call.answer(cache_time=1)
    await Order.order.set()
    

@dp.callback_query_handler(state=Order.order)
async def prods(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    sdata =await state.get_data()
    if call.data =='up':
        await call.answer(cache_time=1)
        await state.update_data({
            
            'quantity':sdata['quantity']+1
        })

    elif call.data =='down':
        if sdata['quantity']>1:
            await call.answer(cache_time=1)
            await state.update_data({
                'quantity':sdata['quantity']-1
            })
        else:
            call.answer('Minimum miqdor 1 ta')
    
    elif call.data == 'order':
        await call.message.delete()
        sdata2 = await state.get_data()
       
        # await call.message.answer(text=f'{call.message.chat.id}')
        await db.add_order(sdata2['pd_id'],int(call.message.chat.id),sdata2['quantity'],sdata2['name'])
        await call.message.answer(text='Menyu:',reply_markup=await categoriesBtn())
        await Category.ctg_menu.set()



    elif call.data == '1':
        await call.message.delete()
        await call.message.edit_reply_markup(reply_markup= await productsBtn(1))
        await Order.order.set()
    
    sdata3 = await state.get_data()
    try:
        await call.message.edit_reply_markup(reply_markup=await order_quantityBtn(sdata3['quantity']))
    except:
        pass
    await call.answer(cache_time=1)

@dp.callback_query_handler(state=Order.final)
async def order(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await call.message.delete()
        await call.message.answer(text='Menyu:',reply_markup=await categoriesBtn())
        await Category.ctg_menu.set()
        return
    if call.data == 'clr':
        await call.message.delete()
        await db.del_orders()
        await call.message.answer(text='Menyu:',reply_markup=await categoriesBtn())
        await Category.ctg_menu.set()
        return
    if call.data == 'finish_ord':
        await call.message.answer(text='Buyurtma qabul qilindi')
    ords = await db.get_orders(int(call.message.chat.id))
    check = await db.check_orders(int(call.message.chat.id))
    for i in ords:
        if call.data == f'{i.product_id}':
            await db.del_order(i.pd_name)
            await call.message.delete()
            ords = await db.get_orders(int(call.message.chat.id))
            sum = 0
            a = ''
            
            for i in ords:
                pd = await db.get_product(i.product_id)
                sum = sum + pd.price*i.quantity
                await state.update_data({
                    'product':f"{i.quantity} ✖️ {i.pd_name}\n"
                })
                sdata = await state.get_data()
                a += sdata['product']
            # if check:
            await call.message.answer(text=f"Savatda:\n{a}Mahsulotlar: {sum} so'm\nYetkazib berish: 10 000 so'm\nJami: {sum+10000} so'm",reply_markup=await orderBtn(call.message.chat.id))
            await Order.final.set()
            # else:
            #     await call.message.answer(text='Sizda hechqanday mahsulot tanlanmagan')
            #     await call.message.answer(text='Menyu:',reply_markup=await categoriesBtn())
            #     await Category.ctg_menu.set()








# @dp.callback_query_handler(state='*')
# async def prods(call: types.CallbackQuery, state: FSMContext):
    # if call.data == 'orders_list':
    #     data =await state.get_data()
    #     await call.message.answer(text = f"Savatda:\n {data['quantity']} ✖️ {data['name']}\nMahsulotlar: {data['price']*data['quantity']} so'm\nYetkazib berish: 10 000 so'm\nJami: {data['price']*data['quantity']+10000} so'm")

# @dp.callback_query_handler(state=Category.prods_about)
# async def make_prods(call=types.CallbackQuery,state = FSMContext):
#     await