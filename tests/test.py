from django.test import TestCase
from app import read_data, write_answer, find_combination, main, compare
import itertools


class AppTestCase(TestCase):

    def setUp(self):
        # Подготовка данных для тестов
        self.sample_data = [
            {'фамилия': 'Смирнов', 'имя': 'Евгений', 'класс': '6'},
            {'фамилия': 'Смирнов', 'имя': 'Алексей', 'класс': '7'},
            {'фамилия': 'Смирнов', 'имя': 'Евгений', 'класс': '8'}
        ]
        self.sample_res = [
            [[0, 0, 0], [0, 1, 1], [0, 0, 1]],
            [[0, 1, 1], [0, 0, 0], [0, 1, 1]],
            [[0, 0, 1], [0, 1, 1], [0, 0, 0]]
        ]
        self.sample_features = ["фамилия", "имя", "класс"]

    def test_read_data(self):
        data = read_data('unit_test.json')
        self.assertEqual(data, self.sample_data)

    def test_write_answer(self):
        answer = ["feature1", "feature2"]
        write_answer(answer, "output.csv")
        with open("output.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
        self.assertEqual(lines, ["feature1\n", "feature2\n"])

    def test_compare(self):
        result = compare(self.sample_data, ["фамилия", "имя", "класс"])
        self.assertEqual(result, self.sample_res)

    def test_find_combination(self):
        combs = itertools.combinations([0, 1, 2], 1)
        answer = find_combination(self.sample_res, combs, 2)
        self.assertEqual(answer, (((2,), 1)))

