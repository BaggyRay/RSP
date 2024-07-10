from aiogram import Router, F, Bot
from aiogram.types import Message
# from aiogram.filters import Command
from config import users
from handlers import keyboards as kb


router_in_game = Router()


@router_in_game.message(F.text == 'Камень')
@router_in_game.message(F.text == 'Ножницы')
@router_in_game.message(F.text == 'Бумага')
async def game(message: Message, bot: Bot):

    user = message.from_user.id
    if users[user]['status'] == 2:
        utake = users[user]['versus']['take'] = message.text
        rid = users[user]['versus']['rid']
        rtake = users[rid]['versus']['take']

        if rtake == '':
            await message.answer('Соперник еще не сделал выбор')
            return

        result = ["Ничья🤝", "Победа🏆", "Поражение😢"]
        result_to_write = ['draws', 'wins', 'loses']
        utake_int, rtake_int = chek_the_winner(utake=utake, rtake=rtake)

        users[user]['stats'][result_to_write[utake_int]] += 1
        users[rid]['stats'][result_to_write[rtake_int]] += 1
        users[user]['versus']['res'] = result[utake_int]
        users[rid]['versus']['res'] = result[rtake_int]

        for player in [user, rid]:
            users[player]['versus']['retry'] = False
            await bot.send_message(
                chat_id=player,
                text=f'{users[user]["name"]} - {utake}\n'
                     f'{users[rid]["name"]} - {rtake}\n'
                     f'{users[player]["versus"]["res"]}',
                reply_markup=kb.create_markup(btn_text=["Реванш", "Выход"])
            )

            users[player]['versus']['take'] = ''
            users[player]['versus']['res'] = ''
    else:
        await message.answer("Начните поиск игры, пропишите команду: /start")


@router_in_game.message(F.text == 'Реванш')
async def retry(message: Message, bot: Bot):
    user = message.from_user.id
    rid = users[user]['versus']['rid']
    users[user]['versus']['retry'] = True

    if not users[rid]['versus']['retry']:
        await message.reply('Ошидаем ответ от соперника...')
        await bot.send_message(
            chat_id=rid,
            text='Соперник, хочет сыграть еще раз.\n'
                 'Нажмите "Реванш", если готовы сыграть еще раз.'
        )
        return

    for plyer in [user, rid]:
        await bot.send_message(
            chat_id=plyer,
            text='Делаем выбор: ',
            reply_markup=kb.create_markup(
                            btn_text=['Камень', 'Ножницы', 'Бумага']
                            )
        )


@router_in_game.message(F.text)
async def chat(message: Message, bot: Bot):
    user = message.from_user.id
    if users[user]['status'] != 2:
        return
    await bot.send_message(
        chat_id=users[user]['versus']['rid'],
        text=f'{users[user]["name"]}: {message.text}'
    )


def chek_the_winner(utake: str, rtake: str):
    if (
        (utake == 'Камень' and rtake == 'Ножницы') or
        (utake == 'Ножницы' and rtake == 'Бумага') or
        (utake == 'Бумага' and rtake == 'Камень')
    ):
        return 1, -1
    elif (
        (utake == 'Камень' and rtake == 'Бумага') or
        (utake == 'Ножницы' and rtake == 'Камень') or
        (utake == 'Бумага' and rtake == 'Ножницы')
    ):
        return -1, 1
    elif (
        (utake == 'Камень' and rtake == 'Камень') or
        (utake == 'Ножницы' and rtake == 'Ножницы') or
        (utake == 'Бумага' and rtake == 'Бумага')
    ):
        return 0, 0
