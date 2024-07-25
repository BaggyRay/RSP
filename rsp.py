import asyncio
from aiogram import Dispatcher, Bot
from handlers.not_in_game_handlers import router_not_in_game
from handlers.in_game_handlers import router_in_game
import os


dp = Dispatcher()
bot = Bot(token=os.getenv('BOT_TOKEN'))


async def main():
    dp.include_routers(router_not_in_game,
                       router_in_game)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Quit')
# import csv
# import pprint
# # Пример словаря users
# users = {
#     'online': 0,
#     54654: {
#         'name': 'John Doe',
#         'username': 'johndoe',
#         'status': 0,
#         'stats': {'draws': 0, 'wins': 0, 'loses': 0},
#         'versus': {'rid': 0, 'take': '', 'retry': False, 'res': ''}
#     },
#     56657: {
#         'name': 'Ilia Doe',
#         'username': 'iohndoe',
#         'status': 0,
#         'stats': {'draws': 0, 'wins': 0, 'loses': 0},
#         'versus': {'rid': 0, 'take': '', 'retry': False, 'res': ''}
#     }
# }

# # Открытие файла CSV для записи
# with open('users_rsp.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)

#     # Запись заголовков столбцов
#     headers = ['Key', 'Value']
#     writer.writerow(headers)

#     # Перебор словаря users и запись его содержимого в CSV
#     for key, value in users.items():
#         if isinstance(value, dict):  # Если значение является другим словарем
#             for sub_key, sub_value in value.items():
#                 row = [f"{key}.{sub_key}", sub_value]
#                 writer.writerow(row)
#         else:
#             row = [key, value]
#             writer.writerow(row)


# def csv_to_dict(filename):
#     data = {}
#     with open(filename, mode='r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         next(reader)  # Пропускаем заголовок

#         for row in reader:
#             key, value = row
#             print(row)
#             # Разделение ключа на уровни, если необходимо
#             levels = key.split('.')
#             print(levels)
#             current_level = data

#             for level in levels[:-1]:
#                 if level not in current_level:
#                     try:
#                         current_level[int(level)] = {}
#                         current_level = current_level[int(level)]

#                     except Exception:
#                         current_level[level] = {}
#                         current_level = current_level[level]

#             # Добавляем последний уровень (значение)
#             current_level[levels[-1]] = value

#     return data

# # Пример использования функции
# filename = 'users_rsp.csv'
# reconstructed_data = csv_to_dict(filename)
# pprint.pprint(reconstructed_data)
