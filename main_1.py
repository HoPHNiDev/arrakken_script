from pyrogram import Client, filters, idle
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram.handlers import MessageHandler

from yaml import safe_load, safe_dump

from os import getcwd
import time
from datetime import datetime
import requests

print('Полный гайд по настройке в канале @HoPHNiArrakken | Coder: @HoPHNi')

def yaml_dump(key, value):
    with open(f'{getcwd()}/config.yaml', 'a') as cfg_for_write:
        safe_dump({key: value}, cfg_for_write)

def send_requst(username, password):
    try:
        main_client.start()
        main_client_info = main_client.get_users("me")
    except Exception as e:
        print(e)
    finally: main_client.stop()

    data = {
        'telegram_user_id': main_client_info.id,
        'username': username,
        'password': password
    }

    r = requests.post(url='https://arrakkenapi.pythonanywhere.com/arrakken/api', data=data).json()

    return r['success']

with open(f'{getcwd()}/config.yaml', 'r') as cfg:
    data = safe_load(cfg)
    channel_id = data['CHANNEL_ID']
    bot_id = data['BOT_ID']
    
    if 'ADMIN' not in data.keys():
        admin = input('Введите ваш телеграм айди (для получения пропишите /start в боте @getmyid_bot): ')
        yaml_dump('ADMIN', admin)
    else:
        admin = data['ADMIN']
    
    if 'USERNAME' in data.keys():
        username = data['USERNAME']

    if 'PASSWORD' in data.keys():
        password = data['PASSWORD']
    
    if 'TOKEN' not in data.keys():
        bot_token = input('Введите токен бота созданного через @botfather: ')
        yaml_dump('TOKEN', bot_token)
    else:
        bot_token = data['TOKEN']
    
    if 'API_ID' not in data.keys():
        api_id = input('Введите api_id из сайта my.telegram.org: ')
        yaml_dump('API_ID', api_id)
    else:
        api_id = data['API_ID']
    
    if 'API_HASH' not in data.keys():
        api_hash = input('Введите api_hash из сайта my.telegram.org: ')
        yaml_dump('API_HASH', api_hash)
    else:
        api_hash = data['API_HASH']

    if 'HOME_ID' not in data.keys():
        home_id = input('1-Акреитесы\n2-Хадроненны\n3-Корртессы\nВыберите ваш альянс(Введите цифру вашего дома из списка выше): ')
        yaml_dump('HOME_ID', home_id)
    else:
        home_id = data['HOME_ID']
    
bot = Client('assistant_bot', bot_token=bot_token, api_id=api_id, api_hash=api_hash, workdir=f'{getcwd()}/sessions')
main_client = Client('@HoPHNi', workdir=f'{getcwd()}/sessions')

if 'USERNAME' not in data.keys() and 'PASSWORD' not in data.keys():
    while True:
        username = input('Введите имя пользователя для доступа к скрипту: ')
        password = input('Введите пароль для доступа к скрипту: ')
        
        if send_requst(username, password):
            yaml_dump('USERNAME', username)
            yaml_dump('PASSWORD', password)
            break
        
        else:
            print('Попробуйте снова, что-то пошло не так...')

if send_requst(username, password):
    working_status = False

    async def check_new_fight():
        await main_client.send_message(bot_id, '/start')
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=1):
            try:
                await last_message.click(1)
            except: pass
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=1):
            if int(last_message.caption.split('через ')[1].split('ч')[0]) == 11:
                return True
            else:
                return False

    async def send_farming(winner_id):
        await main_client.send_message(bot_id, '/start')
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=1):
            try:
                await last_message.click(3)
            except: pass
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=2):
            if last_message.caption == 'Выберите действие': continue
            nft_id = last_message.text.split('ID ')[1].split(' /')[0]
            print(nft_id)
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=1):
            try:
                await last_message.click(4)
            except: pass
        time.sleep(1)
        await main_client.send_message(bot_id, str(nft_id))
        await bot.send_message(admin, f'💎⚔️✅ NFT ID {nft_id} - Успешно отправлен фармить \nВремя: {datetime.now().strftime("%H:%M:%S")}')

    async def send_fighting(winner_id):
        await main_client.send_message(bot_id, '/start')
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=1):
            try:
                await last_message.click(3)
            except: pass
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=2):
            if last_message.caption == 'Выберите действие': continue
            nft_id = last_message.text.split('ID ')[1].split(' /')[0]
            print(nft_id)
        time.sleep(1)
        async for last_message in main_client.get_chat_history(bot_id, limit=1):
            try:
                await last_message.click(5)
            except: pass
        time.sleep(1)
        await main_client.send_message(bot_id, str(nft_id))
        time.sleep(1)
        atacking_home = 'Акреитесов' if winner_id==2 and home_id==3 or winner_id==3 and home_id==2 else 'Хардроненнов' if winner_id==1 and home_id==3 or winner_id==3 and home_id==1 else "Корртессов"
        async for last_message in main_client.get_chat_history(bot_id, limit=1):
            try:
                await last_message.click(f'⚔️ Атаковать Дом {atacking_home}')
            except: pass
        await bot.send_message(admin, f'✅ NFT ID {nft_id} - Успешно отправлен сражаться против {atacking_home} \nВремя: {datetime.now().strftime("%H:%M:%S")}')

    @bot.on_message(filters.command("start"))
    async def reply(client, message):
        if int(message.from_user.id) == int(admin):
            await bot.send_message(
                message.from_user.id,
                f"Welcome, {message.from_user.first_name}! Glad to see you here!",
                reply_markup = ReplyKeyboardMarkup(
                        [
                            ["/change_status"]
                        ],
                        resize_keyboard=True
                    )
            )
        else:
            await bot.send_message(
                message.from_user.id,
                "Access denied! You are not an admin!",)
            
    @bot.on_message(filters.command("change_status"))
    async def reply(client, message):
        if int(message.from_user.id) == int(admin):
            global working_status
            if not working_status:
                working_status = True
                await bot.send_message(message.from_user.id, 'Автоотправка на фарм и на сражение успешно включено! Теперь можете спокойно идти спать :)')
            else:
                working_status = False
                await bot.send_message(message.from_user.id, 'Отправка на фарм и сражения теперь в ручном режиме, будьте начеку!')
        else:
            await bot.send_message(
                message.from_user.id,
                "Access denied! You are not an admin!",)

    @main_client.on_message(filters.chat(channel_id))
    async def _(client, message):
        if 'Битва за Арраккен завершена победой Дома' in message.text and await check_new_fight():
            time.sleep(15)
            winner_id = 1 if 'Акреитессов' in message.text else 2 if 'Хадроненнов' in message.text else 3
            
            if winner_id == int(home_id):
                await send_farming(winner_id)
            else:
                await send_fighting(winner_id)

    bot.start()
    main_client.start()

    idle()

    bot.stop()
    main_client.stop()