import math


class CalculatorCore:
    def __init__(self):
        self.use_degrees = False

    def set_degrees_mode(self, use_degrees):
        self.use_degrees = use_degrees

    def preprocess_expression(self, expr):
        """Предварительная обработка выражения"""
        expr = expr.replace('π', 'pi')
        expr = expr.replace('e', 'e')
        expr = expr.replace('²', '**2')
        expr = expr.replace('^', '**')
        expr = expr.replace(' mod ', '%')
        return expr

    def convert_to_radians(self, value):
        if self.use_degrees:
            return math.radians(value)
        return value

    def convert_from_radians(self, value):
        if self.use_degrees:
            return math.degrees(value)
        return value

    def safe_sin(self, x):
        return math.sin(self.convert_to_radians(x))

    def safe_cos(self, x):
        return math.cos(self.convert_to_radians(x))

    def safe_tan(self, x):
        return math.tan(self.convert_to_radians(x))

    def safe_asin(self, x):
        result = math.asin(x)
        return self.convert_from_radians(result)

    def safe_acos(self, x):
        result = math.acos(x)
        return self.convert_from_radians(result)

    def safe_atan(self, x):
        result = math.atan(x)
        return self.convert_from_radians(result)

    def calculate_expression(self, expression):
        """Основной метод для вычисления выражения"""
        try:
            expression = self.preprocess_expression(expression)
            return self.safe_eval(expression)
        except ZeroDivisionError:
            raise ValueError("Деление на ноль!")
        except Exception as e:
            raise ValueError(f"Неверное выражение: {str(e)}")

    def safe_eval(self, expression):
        safe_dict = {
            'pi': math.pi,
            'e': math.e,
            'sin': self.safe_sin,
            'cos': self.safe_cos,
            'tan': self.safe_tan,
            'asin': self.safe_asin,
            'acos': self.safe_acos,
            'atan': self.safe_atan,
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'abs': abs,
            'round': round,
            '__builtins__': {},
            'math': math
        }

        try:
            result = eval(expression, safe_dict)
            return self.format_result(result)
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {e}")

    def format_result(self, result):
        if result is None:
            return "Ошибка"

        if isinstance(result, (int, float)):
            if abs(result - round(result)) < 1e-10:
                return int(round(result))
            else:
                return round(result, 10)

        return str(result)