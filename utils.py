def parse_users(query):
    users = [{
        key: ( getattr(item, key) if key != 'birth_date' \
                else getattr(item, key).strftime("%d/%m/%Y") ) \
            for key in item.__table__.columns.keys()
    } for item in query] if query else None

    if users:
        for user in users:
            name = user['name']
            fst_ln = user['first_last_name']
            snd_ln = user['second_last_name']
            user['username'] = f'{name} {fst_ln} {snd_ln}' if snd_ln \
                                else f'{name} {fst_ln}'

    return users
