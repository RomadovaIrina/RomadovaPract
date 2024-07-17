from django.test import TestCase
from app import read_data, write_answer, find_combination, compare
import itertools
import os
import json


class AppTestCase(TestCase):

    def setUp(self):
        # Подготовка данных для тестов
        self.sample_data = [
            {'about': '1', 'фамилия': 'Смирнов', 'имя': 'Евгений', 'класс': '6'},
            {'about': '2', 'фамилия': 'Смирнов', 'имя': 'Алексей', 'класс': '7'},
            {'about': '3', 'фамилия': 'Смирнов', 'имя': 'Евгений', 'класс': '8'}
        ]
        self.sample_res = [
            [[0, 0, 0], [0, 1, 1], [0, 0, 1]],
            [[0, 1, 1], [0, 0, 0], [0, 1, 1]],
            [[0, 0, 1], [0, 1, 1], [0, 0, 0]]
        ]
        self.sample_features = ["фамилия", "имя", "класс"]

    def test_read_data(self):
        # Сохранение sample_data в файл
        with open('ut.json', 'w', encoding='utf-8') as file:
            json.dump(self.sample_data, file)
        data = read_data('ut.json')
        self.assertEqual(data, self.sample_data)
        os.remove('ut.json')  # Удаляем файл после теста

    def test_write_answer(self):
        answer = ["feature1", "feature2"]
        write_answer(answer, "output.csv")
        with open("output.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
        self.assertEqual(lines, ["feature1\n", "feature2\n"])
        os.remove("output.csv")  # Удаляем файл после теста

    def test_compare(self):
        result = compare(self.sample_data, ["фамилия", "имя", "класс"])
        self.assertEqual(result, self.sample_res)

    def test_find_combination(self):
        combs = itertools.combinations([0, 1, 2], 1)
        answer = find_combination(self.sample_res, combs, 2)
        self.assertEqual(answer, ((2,), 1))

    def test_find_combination_no_valid_comb(self):
        sample_res_no_diff = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ]
        combs = itertools.combinations([0, 1, 2], 1)
        answer = find_combination(sample_res_no_diff, combs, 2)
        self.assertEqual(answer, ((), 0))

    def test_compare_with_different_data(self):
        different_data = [
            {'about': '1', 'фамилия': 'Иванов', 'имя': 'Евгений', 'класс': '6'},
            {'about': '2', 'фамилия': 'Смирнов', 'имя': 'Алексей', 'класс': '7'},
            {'about': '3', 'фамилия': 'Петров', 'имя': 'Иван', 'класс': '8'}
        ]
        expected_res = [
            [[0, 0, 0], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [0, 0, 0], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [0, 0, 0]]
        ]
        result = compare(different_data, ["фамилия", "имя", "класс"])
        self.assertEqual(result, expected_res)
