import requests
import numpy as np
import matplotlib.pyplot as plt
import time


def get_data():
    token = ''            # сюда надо ввести токен, свой я убрал
    version = 5.103
    group_id = 'hse_university'  # в качестве группы я выбрал группу ВШЭ в вк
    step = 0
    group_data = []

    url = 'https://api.vk.com/method/groups.getMembers'     # при такой архитектуре будет проще в дальнейшем интегрировать запросы для любого токена, версии  API VK и группы
    while True:
        response = requests.get(url,
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'group_id': group_id,
                                    'offset': step,
                                    'count': 1000,
                                    'fields': 'bdate'
                                })

        group_data.extend(response.json()["response"]['items'])
        step += 1000
        if step > response.json()["response"]['count']:
            break
        time.sleep(0.05)

    return group_data


def get_id(data_dict):
    id_array = []
    day_array = []
    month_array = []

    for user in data_dict:
        if 'bdate' in user:

            l = list(map(int, user['bdate'].split('.')))

            day_array.append(l[0])          # берем только день и месяц
            month_array.append(l[1])
            id_array.append(user['id'])

    id_array = np.array(id_array)
    day_array = np.array(day_array)
    month_array = np.array(month_array)
    return id_array, day_array, month_array


def make_histgram(month_array):
    month = np.arange(1, 13)
    count = np.array([0] * 12)

    for i in range(len(month_array)):
        count[month_array[i] - 1] += 1

    plt.bar(month, count)

    maxx = max(count)
    index = 0
    for i in range(len(count)):
        if count[i] == maxx:
            index = i
    plt.bar(month[index], count[index], color='red')

    plt.xlabel("Month")
    plt.ylabel("Number of people")

    plt.title("Birth month of people in the HSE group")
    plt.show()                 # как можем увидеть по гистограмме, больше всего людей из группы вышки родилось в июле


def match_check(day_cur_array, month_cur_array):
    for i in range(50):
        for j in range(i + 1, 50):
            if day_cur_array[i] == day_cur_array[j] and month_cur_array[i] == month_cur_array[j]:
                return 1
    return 0

def percentage_ratio(day_array, month_array):
    index = np.arange(len(day_array))         # индекс - это 'уникальный' человек, так все наши массивы связаны по индексу

    matches = 0
    for i in range(20000):
        random_people = np.random.choice(index, 50)
        day_cur_array = day_array[random_people]
        month_cur_array = month_array[random_people]

        if match_check(day_cur_array, month_cur_array) == 1:
            matches += 1

    print("Вероятность, полученная экспериментальным путем: ", matches / 20000 * 100)


def main():
    data_dict = get_data()
    id_array, day_array, month_array = get_id(data_dict)    # все 3 numpy массива связаны по индексу, то есть по индексу i находится один и тот же человек во всех 3 массивах

    make_histgram(month_array)
    percentage_ratio(day_array, month_array)


if __name__ == '__main__':
    main()
