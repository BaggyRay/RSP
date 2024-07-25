import csv


def csv_to_dict(filename):
    data = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок

        for row in reader:
            key, value = row
            # Разделение ключа на уровни, если необходимо
            levels = key.split('.')
            current_level = data

            for level in levels[:-1]:
                if level not in current_level:
                    current_level[level] = {}
                current_level = current_level[level]

            # Добавляем последний уровень (значение)
            current_level[levels[-1]] = value

    return data


def dict_to_csv(users: dict):
    with open('users_rsp.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Запись заголовков столбцов
        headers = ['Key', 'Value']
        writer.writerow(headers)

        # Перебор словаря users и запись его содержимого в CSV
        for key, value in users.items():
            if isinstance(value, dict):  # Если значение является другим словарем
                for sub_key, sub_value in value.items():
                    row = [f"{key}.{sub_key}", sub_value]
                    writer.writerow(row)
            else:
                row = [key, value]
                writer.writerow(row)
