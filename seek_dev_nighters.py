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
        yield from req.json()['records']
        for page in range(1, page_count):
            yield from get_data(page + 1)


def is_midnighter(user):
    if user['timestamp'] is None:
        return False
    user_datetime = datetime.fromtimestamp(user['timestamp'])
    return(time(5, 0, 0) > user_datetime.time() > time(0, 0, 0))


if __name__ == '__main__':
    midnighters = set([user['username'] for user in load_attempts() if is_midnighter(user)])
    for midnighter in midnighters:
        print(midnighter)
