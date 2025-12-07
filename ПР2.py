import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator_core import CalculatorCore


class TestCalculatorBasicOperations(unittest.TestCase):
    """Тесты базовых арифметических операций калькулятора"""

    def setUp(self):
        """
        Метод setUp выполняется ПЕРЕД КАЖДЫМ тестом.
        Здесь мы создаем новый экземпляр калькулятора для каждого теста.
        Это гарантирует, что тесты не влияют друг на друга.
        """
        self.calc = CalculatorCore()
        print("Создан новый калькулятор для теста")
        print ("Тесты запущены")

    def tearDown(self):
        """
        Метод tearDown выполняется ПОСЛЕ КАЖДОГО теста.
        Здесь можно освобождать ресурсы, закрывать файлы и т.д.
        """
        print("Тест завершен")

    def test_addition(self):
        """Тестируем сложение"""
        result = self.calc.calculate_expression("2+3")
        self.assertEqual(result, 5)

    def test_subtraction(self):
        """Тестируем вычитание"""
        result = self.calc.calculate_expression("5-2")
        self.assertEqual(result, 3)

    def test_multiplication(self):
        """Тестируем умножение"""
        result = self.calc.calculate_expression("3*4")
        self.assertEqual(result, 12)

    def test_division(self):
        """Тестируем деление"""
        result = self.calc.calculate_expression("10/2")
        self.assertEqual(result, 5)

    def test_division_by_zero(self):
        """Тестируем обработку деления на ноль"""
        # Проверяем, что возникает ошибка ValueError
        with self.assertRaises(ValueError) as context:
            self.calc.calculate_expression("5/0")

        # Проверяем текст ошибки
        self.assertIn("division by zero", str(context.exception))

    def test_float_operations(self):
        """Тестируем операции с дробными числами"""
        result = self.calc.calculate_expression("2.5 + 3.5")
        self.assertEqual(result, 6.0)

    def test_parentheses_priority(self):
        """Тестируем приоритет операций со скобками"""
        result_with_parentheses = self.calc.calculate_expression("(2+3)*4")
        result_without_parentheses = self.calc.calculate_expression("2+3*4")

        self.assertEqual(result_with_parentheses, 20)
        self.assertEqual(result_without_parentheses, 14)



class TestCalculatorAdvancedOperations(unittest.TestCase):
    """Тесты расширенных операций калькулятора"""

    def setUp(self):
        self.calc = CalculatorCore()

    def test_power_operation(self):
        """Тестируем возведение в степень"""
        result = self.calc.calculate_expression("2**3")
        self.assertEqual(result, 8)

    def test_square_root(self):
        """Тестируем квадратный корень"""
        result = self.calc.calculate_expression("sqrt(16)")
        self.assertEqual(result, 4)

    def test_modulo_operation(self):
        """Тестируем остаток от деления"""
        result = self.calc.calculate_expression("5 mod 2")
        self.assertEqual(result, 1)


# Дополнительные методы unittest:
class ExampleUnittestMethods(unittest.TestCase):
    """Примеры различных assert методов в unittest"""

    def test_assert_methods(self):
        """Демонстрация различных методов проверки"""
        # Проверка равенства
        self.assertEqual(5, 5)

        # Проверка неравенства
        self.assertNotEqual(5, 10)

        # Проверка на True/False
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)

        # Проверка на None
        self.assertIsNone(None)
        self.assertIsNotNone("text")

        # Проверка вхождения
        self.assertIn(3, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])

        # Проверка типа
        self.assertIsInstance(5, int)
        self.assertIsInstance("hello", str)


if __name__ == '__main__':
    # Запуск тестов
    unittest.main(verbosity=2)