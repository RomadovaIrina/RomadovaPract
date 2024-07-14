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
    print(f"Answer: {filename}")


# Нахождение ответа для сочетаний заданной длины
def find_combination(res, combs, min_len):
    answer = tuple()
    found = 0
    for comb in combs:
        is_answer = True
        for i in range(len(res)):
            for j in range(i):
                found_diff = False
                for feature in comb:
                    if res[i][j][feature] == 1:
                        found_diff = True
                        break
                if not found_diff:
                    is_answer = False
                    break
            if not is_answer:
                break
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


def main():
    # Считываем данные
    input_name = input()
    data = read_data(input_name)
    output_name = input()
    # Заполняем признаки
    features = set()
    for i in data:
        features.update(i.keys())
    features = list(features)
    res = compare(data, features)
    num = len(features)
    # iterate- массив, для которого будут составляться сочетания разной длинны
    iterate = list(range(num))
    min_len = len(features) + 1
    # задаем верхнюю и нижнюю границы для бинарного поиска
    low_bound, high_bound = 0, num + 1
    first = num // 4
    second = 3 * num // 4
    answer = tuple()
    # Проверяем: есть ли ответ длины first
    first_comb = itertools.combinations(iterate, first)
    ans_first = find_combination(res, first_comb, num)
    found_1 = ans_first[1]
    # Если не нашли ответ, то для (0, 1, ... first-1) ответа так же не будет
    if (found_1 == 0):
        # Сдвигаем верхнюю и нижнюю границы, так как перебирать 
        # от 0 до first больше нет смысла
        low_bound = first
        high_bound = second + 1
    # Если ответ найден, то пытаемся найти ответ короче first    
    else:
        high_bound = first

    # Используем бинарный поиск чтобы найти ответ.
    while high_bound - low_bound > 1:
        middle = (low_bound + high_bound) // 2
        combs = itertools.combinations(iterate, middle)
        # Ищем ответ для сочетаний заданной длинны
        is_ans = find_combination(res, combs, min_len)
        if is_ans[1]:
            high_bound = middle
            answer = is_ans[0]
        else:
            low_bound = middle
    final = [features[i] for i in answer]
    # записываем ответ
    write_answer(final, output_name)


if __name__ == '__main__':
    main()
