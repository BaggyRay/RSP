from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from handlers import keyboards as kb
from pprint import pprint
import time
from config import users, DB


router_not_in_game = Router()


@router_not_in_game.message(CommandStart())
async def command_start(message: Message, bot: Bot):

    user = message.from_user.id
    if user not in users.keys():
        await message.answer('Привет, давай сыграем в '
                             '✊, ✌, 🖐\n',
                             reply_markup=kb.start_game_btn)
        users[user] = DB(
            name=message.from_user.first_name,
            username=message.from_user.username,
        )
        pprint(users)
    elif users[user]['status'] == 1:
        await message.answer('У тебя идет поиск.')
    elif users[user]['status'] == 2:
        await message.answer('Ты в игре')
    else:
        await message.answer('Нажимай "Поехали" и в БОЙ'
                             '✊, ✌, 🖐\n',
                             reply_markup=kb.start_game_btn)


@router_not_in_game.message(Command(commands=['help']))
async def command_help(message: Message):
    await message.answer('Начать -> ошидаешь соперника -> играешь')


@router_not_in_game.message(Command(commands=['rules']))
async def command_rules(message: Message):
    await message.answer('✊->✌->🖐->✊')


@router_not_in_game.message(F.text == 'Поехали')
async def satrt_game(message: Message, bot: Bot):
    user = message.from_user.id
    if user not in users.keys():
        await message.answer('Вы еще не нажали /start')
        return
    if users[user]['status'] == 1:
        await message.answer('Вы уже находитесь в поиске!')
        return

    users['online'] += 1
    users[user]['status'] = 1
    await message.answer(
        text='Статистика:\n'
             f"Побед🏆 = {users[user]['stats']['wins']}\n"
             f"Поражений😢 = {users[user]['stats']['loses']}\n"
             f"Ничьих🤝 = {users[user]['stats']['draws']}",
        reply_markup=kb.create_markup(['Отмена'])

    )
    msg = await message.answer(
        text='Поиск соперника 🕛\n'
             f'Соперников в поиске : {users["online"]-1}'
    )
    users[user]['msg_id'] = msg.message_id
    pprint(users.keys())

    for user_id in users.keys():
        if (
            user == user_id or
            isinstance(user_id, str) or
            users[user_id]['status'] == 0 or
            users[user_id]['status'] == 2
        ):
            continue
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=users[user_id]['msg_id'],
            text='Поиск соперника 🕛\n'
                 f'Соперников в поиске : {users["online"]-1}',
        )

    time.sleep(1)
    if users['online'] >= 2:
        users[user]['status'] = 2
        for rid in users.keys():
            if isinstance(rid, str):
                continue
            if users[rid]['status'] == 1:
                users[user]['versus']['rid'] = rid
                users[rid]['versus']['rid'] = user
                users[rid]['status'] = 2
                rival = rid
                break

        for i in range(4):
            for players in [user, rival]:
                if users[players]['status'] == 0:
                    return
                await bot.edit_message_text(
                    chat_id=players,
                    message_id=users[players]['msg_id'],
                    text=f'Игра начнется через: {3-i}'
                    if i != 3 else 'Приятной игры! '
                )
                time.sleep(1)

        users['online'] -= 2
        for players in [user, rival]:
            await bot.send_message(
                chat_id=players,
                text='Твой соперник - '
                     f'{users[users[players]["versus"]["rid"]]["name"]}\n'
                     'Делаем выбор...',
                reply_markup=kb.create_markup(btn_text=[
                        'Камень', 'Ножницы', 'Бумага'])
                )
    pprint(users)


@router_not_in_game.message(F.text == 'Отмена')
async def cancel(message: Message, bot: Bot):
    user = message.from_user.id
    if user not in users.keys():
        await message.answer('Вы еще не нажали /start')
        return
    if users[user]['status'] != 1:
        await message.answer('Вы в поиске игры')
        return
    rid = users[user]['versus']['rid']
    users[user]['status'] = 0
    users[user]['versus']['rid'] = 0
    await message.answer(
        text='Поиск отменен',
        reply_markup=kb.start_game_btn
    )
    if rid == 0:
        return
    users[rid]['status'] = 1
    users[rid]['versus']['rid'] = 0
    await bot.send_message(
        chat_id=rid,
        text='Соперник отменил поиск'
    )
    users['online'] -= 1

    await bot.send_message(
        chat_id=rid,
        text='Поиск соперника 🕛\n'
             f'Соперников в поиске : {users["online"]-1}',
    )

    pprint(users)


@router_not_in_game.message(F.text == 'Выход')
async def escape(message: Message, bot: Bot):
    user = message.from_user.id
    if user not in users.keys():
        await message.answer('Вы еще не нажали /start')
        return
    if users[user]['status'] != 2:
        await message.answer('Вы не в игре')
        return

    users[user]['status'] = 0
    rid = users[user]['versus']['rid']
    await bot.send_message(chat_id=users[user]['versus']['rid'],
                           text="Соперник вышел!\n"
                                "Выхожу из лобби!")
    await message.answer(text="Выхожу из лобби!")
    users[rid]['status'] = 0
    users[rid]['versus']['retry'] = False
    users[user]['versus']['rid'] = 0
    users[rid]['versus']['rid'] = 0
    for player in [user, rid]:
        await bot.send_message(
            chat_id=player,
            text='Твоя статистика:\n'
                 f"Побед🏆 = {users[player]['stats']['wins']}\n"
                 f"Поражений😢 = {users[player]['stats']['loses']}\n "
                 f"Ничьих🤝 = {users[player]['stats']['draws']}",
            reply_markup=kb.start_game_btn
        )
