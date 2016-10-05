from datetime import datetime, time

import requests


API_URL = 'http://devman.org/api/challenges/solution_attempts/'


def get_data(page):
    req = requests.get(API_URL, params={'page': page})
    if req.status_code == 200:
        return req.json()['records']


def load_attempts():
    req = requests.get(API_URL)
    if req.status_code == 200:
        page_count = req.json()['number_of_pages']
        for page in range(page_count):
            yield get_data(page + 1)


def is_midnighter(user):
    user_datetime = datetime.fromtimestamp(user['timestamp'])
    return(time(5, 0, 0) > user_datetime.time() > time(0, 0, 0))


def get_midnighters():
    midnighters = []
    for i in load_attempts():
        midnighters += list(filter(is_midnighter, i))
    return set(map(lambda a: a['username'], midnighters))


if __name__ == '__main__':
    for midnighter in get_midnighters():
        print(midnighter)
