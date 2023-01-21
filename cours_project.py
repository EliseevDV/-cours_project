import json
import requests
from tqdm import tqdm
from id_vk import token
user_id = input('Введите id VK: ')
yandex_disk_token = ('Введите токен с Полигона Яндекс.Диска: ')

yandex_disk_url ='https://cloud-api.yandex.net/v1/disk/resources'

# Авторизация на Вконтакте

vk = requests.get(f'https://api.vk.com/method/{token}/')

# Получение фотографий с профиля
photos = vk.photos.get(owner_id=user_id, album_id='profile', count=5)

# Авторизация на Яндекс.Диске
headers = {'Authorization': 'OAuth ' + yandex_disk_token}

# Создание папки для загруженных фотографий
requests.put(yandex_disk_url + '/photos', headers=headers)

# Сохранение фотографий и информации по ним в json-файл
data = []
for photo in tqdm(photos['items']):
    size = max(photo['width'], photo['height'])
    url = f"https://vk.com/photo{photo['owner_id']}_{photo['id']}_{photo['access_key']}"
    response = requests.get(url, stream=True)
    file_name = f"{photo['likes']['count']}.jpg"
    with open(file_name, "wb", encoding='utf-8') as f:
        f.write(response.content)
    data.append({'file_name': file_name, 'size': size})

    # Загрузка фотографий на Яндекс.Диск
    with open(file_name, 'rb', encoding='utf-8') as f:
        requests.put(yandex_disk_url + '/photos/' + file_name, data=f, headers=headers)

    # Сохранение информации по фотографиям в json-файл
    with open('photos_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
