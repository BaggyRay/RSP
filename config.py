# from csv_work import csv_to_dict


# users = csv_to_dict('users.csv')


users = {
    'online': 0
}


def DB(name: str, username: str):
    return {
        'name':     name,
        'username': username,
        'status':   0,  # 0-нажал старт, 1-в поиске, 2-в игре
        'stats':    {
                'draws':     0,
                'wins':     0,
                'loses':    0
                    },
        'versus':   {
                'rid':      0,  # id соперника
                'take':     '',
                'retry':    False,
                'res':      ''
                    }

    }
