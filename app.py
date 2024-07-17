import json
import itertools
import csv


# Функция для считывания данных
def read_data(path):
    with open(path, encoding='utf-8') as file:
        data_to_load = json.load(file)
    return data_to_load


# Функция для записи ответа
def write_answer(final, filename):
    if len(filename.strip()) == 0:
        filename = "output.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for feature in final:
            writer.writerow([feature])
    print(f"Answer written in: {filename}")


# Нахождение ответа для сочетаний заданной длины
# Мы хотим проверить есть ли ответ для комбинаций такой длины
def find_combination(res, combs, min_len):
    answer = tuple()
    found = 0
    for comb in combs:
        is_answer = True
        # Пройдем по массиву res, чтобы определить
        # Подходит ли данная комбинация под следующее условие:
        # у любой пары элементов, хотя бы 1 параметр будет иметь разные значения
        for i in range(len(res)):
            for j in range(i):
                found_diff = False
                for feature in comb:
                    # если значение параметра разное то разница найдена
                    if res[i][j][feature] == 1:
                        found_diff = True
                        break
                # Если разницу не нашли, то данная комбинация это не ответ
                if not found_diff:
                    is_answer = False
                    break
            if not is_answer:
                break
        # Если мы нашли ответ, длины меньшей чем имеющейся,
        # то мы его обновим
        if is_answer:
            found = 1
            if len(comb) < min_len:
                answer = comb
                min_len = len(comb)
            break
    return (answer, found)


# Функция для определения ращличия признаков в двух записях
def compare(data, features):
    res = [[[0] * len(features)
            for j in range(len(data))] for i in range(len(data))]
    for i, j in itertools.combinations(range(len(data)), 2):
        for ind, feature in enumerate(features):
            i_value = data[i].get(feature)
            j_value = data[j].get(feature)
            # Сравниваем значения признаков в парах
            if i_value != j_value:
                res[i][j][ind] = 1
                res[j][i][ind] = 1
    return res


def main(json_input):
    # Парсим JSON-строку
    params = json.loads(json_input)
    input_name = params['input_name']
    output_name = params['output_name']

    # Считываем данные
    data = read_data(input_name)

    # Заполняем признаки
    features = set()
    for i in data:
        features.update(i.keys())
    features = list(features)
    res = compare(data, features)
    num = len(features)
    iterate = list(range(num))
    min_len = len(features) + 1
    low_bound, high_bound = 0, num + 1
    first = 3 * num // 4
    second = num // 4
    answer = tuple()
    first_comb = itertools.combinations(iterate, first)
    ans_first = find_combination(res, first_comb, num)
    second_comb = itertools.combinations(iterate, second)
    ans_second = find_combination(res, second_comb, num)
    found_1 = ans_first[1]
    found_2 = ans_second[1]
    if (found_1 == 1 and found_2 == 1):
        high_bound = second
    elif (found_1 == 1 and found_2 == 0):
        high_bound = first
        low_bound = second
    else:
        low_bound = first

    while high_bound - low_bound > 1:
        middle = (low_bound + high_bound) // 2
        combs = itertools.combinations(iterate, middle)
        is_ans = find_combination(res, combs, min_len)
        if is_ans[1]:
            high_bound = middle
            answer = is_ans[0]
        else:
            low_bound = middle
    final = [features[i] for i in answer]
    write_answer(final, output_name)


if __name__ == '__main__':
    json_input = input("Enter json string: ")
    main(json_input)
