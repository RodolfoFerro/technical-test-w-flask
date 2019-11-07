import requests


def test_create(data):
    """Utility function to test CREATE method."""

    url = 'http://0.0.0.0:5000/create'

    for item in data:
        response = requests.post(url, json=item)
        print(response.text)

    return


def test_read(ids):
    """Utility function to test READ method."""

    url = 'http://0.0.0.0:5000/read'

    for id in ids:
        response = requests.get(url + f'/{id}')
        print(response.text)

    return


def test_update(id, data):
    """Utility function to test UPDATE method."""

    url = 'http://0.0.0.0:5000/update'

    response = requests.put(url + f'/{id}', json=data)
    print(response.text)

    return


def test_delete(ids):
    """Utility function to test DELETE method."""

    url = 'http://0.0.0.0:5000/delete'

    for id in ids:
        response = requests.delete(url + f'/{id}')
        print(response.text)

    return


if __name__ == '__main__':
    # ================== Test CREATE ==================
    data = [
        {
            'name': 'Rodolfo',
            'first_last_name': 'Ferro',
            'second_last_name': 'Pérez',
            'email': 'rodolfoferroperez@gmail.com',
            'birth_date': '01/11/1992',
            'gender': 'M',
            'password': '1234567890'
        },
        {
            'name': 'Madara',
            'first_last_name': 'Uchiha',
            'email': 'madara@uchiha.com',
            'birth_date': '24/12/1980',
            'gender': 'M',
            'password': '123'
        },
        {
            'name': 'Itachi',
            'first_last_name': 'Uchiha',
            'email': 'itachi@uchiha.com',
            'birth_date': '09/06/1980',
            'gender': 'M',
            'password': '456'
        }
    ]
    test_create(data)


    # =================== Test READ ===================
    ids = [2, 3, 4]
    test_read(ids)


    # ================== Test UPDATE ==================
    id, user = 2, {
        'birth_date': '24/12/1960'
    }
    test_update(id, user)


    # ================== Test UPDATE ==================
    ids = [3, 4]
    test_delete(ids)
