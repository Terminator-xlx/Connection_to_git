import tkinter as tk
from tkinter import messagebox
import math


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("400x500")
        self.window.resizable(False, False)

        self.current_input = ""
        self.result_var = tk.StringVar()
        self.use_degrees = False  # По умолчанию радианы

        self.create_widgets()
        self.bind_keyboard()

    def create_widgets(self):
        # Поле для ввода и результата
        entry_frame = tk.Frame(self.window)
        entry_frame.pack(pady=20)

        self.entry = tk.Entry(entry_frame, textvariable=self.result_var,
                              font=('Arial', 16), justify='right', width=25)
        self.entry.pack()
        self.entry.focus_set()

        # Переключатель градусы/радианы
        mode_frame = tk.Frame(self.window)
        mode_frame.pack(pady=5)

        self.mode_var = tk.StringVar(value="RAD")
        deg_radio = tk.Radiobutton(mode_frame, text="Градусы", variable=self.mode_var,
                                   value="DEG", command=self.toggle_mode)
        rad_radio = tk.Radiobutton(mode_frame, text="Радианы", variable=self.mode_var,
                                   value="RAD", command=self.toggle_mode)
        deg_radio.pack(side=tk.LEFT)
        rad_radio.pack(side=tk.LEFT)

        # Кнопки калькулятора
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack()

        buttons = [
            ['sin', 'cos', 'tan', '⌫', 'C'],
            ['asin', 'acos', 'atan', '(', ')'],
            ['log', 'ln', 'sqrt', 'x²', 'x^y'],
            ['7', '8', '9', '/', 'π'],
            ['4', '5', '6', '*', 'e'],
            ['1', '2', '3', '-', 'mod'],
            ['0', '.', '=', '+', '%']
        ]

        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                width = 6 if len(button_text) > 3 else 5
                height = 2

                button = tk.Button(buttons_frame, text=button_text,
                                   font=('Arial', 11), width=width, height=height,
                                   command=lambda text=button_text: self.button_click(text))
                button.grid(row=i, column=j, padx=2, pady=2)

    def toggle_mode(self):
        self.use_degrees = (self.mode_var.get() == "DEG")

    def button_click(self, text):
        if text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == 'π':
            self.current_input += 'π'
            self.result_var.set(self.current_input)
        elif text == 'e':
            self.current_input += 'e'
            self.result_var.set(self.current_input)
        elif text == 'x²':
            self.current_input += '²'
            self.result_var.set(self.current_input)
        elif text == 'x^y':
            self.current_input += '^'
            self.result_var.set(self.current_input)
        elif text == 'mod':
            self.current_input += ' mod '
            self.result_var.set(self.current_input)
        else:
            # Для функций добавляем скобки автоматически
            if text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'ln', 'sqrt']:
                self.current_input += text + '('
            else:
                self.current_input += text
            self.result_var.set(self.current_input)

    def calculate(self):
        try:
            expression = self.current_input

            # Предварительная обработка выражения
            expression = self.preprocess_expression(expression)

            # Вычисление
            result = self.safe_eval(expression)

            if result is not None:
                formatted_result = self.format_result(result)
                self.result_var.set(formatted_result)
                self.current_input = str(formatted_result)

        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверное выражение: {str(e)}")
            self.clear()

    def preprocess_expression(self, expr):
        """Предварительная обработка выражения"""
        # Заменяем специальные символы и функции
        expr = expr.replace('π', 'pi')
        expr = expr.replace('e', 'e')
        expr = expr.replace('²', '**2')
        expr = expr.replace('^', '**')
        expr = expr.replace(' mod ', '%')

        return expr

    def safe_eval(self, expression):
        """Безопасное вычисление выражения с поддержкой математических функций"""

        # Создаем безопасное окружение для eval
        safe_dict = {
            # Математические константы
            'pi': math.pi,
            'e': math.e,

            # Основные математические функции
            'sin': self.safe_sin,
            'cos': self.safe_cos,
            'tan': self.safe_tan,
            'asin': self.safe_asin,
            'acos': self.safe_acos,
            'atan': self.safe_atan,
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,

            # Базовые арифметические операции
            'abs': abs,
            'round': round,
        }

        # Добавляем базовые математические операции
        safe_dict.update({
            '__builtins__': {},
            'math': math
        })

        try:
            # Вычисляем выражение
            result = eval(expression, safe_dict)
            return result
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {e}")

    def convert_to_radians(self, value):
        """Конвертирует градусы в радианы если нужно"""
        if self.use_degrees:
            return math.radians(value)
        return value

    def convert_from_radians(self, value):
        """Конвертирует радианы в градусы если нужно"""
        if self.use_degrees:
            return math.degrees(value)
        return value

    # Безопасные обертки для тригонометрических функций
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

    def format_result(self, result):
        """Форматирует результат для отображения"""
        if result is None:
            return "Ошибка"

        if isinstance(result, (int, float)):
            # Проверяем на целое число
            if abs(result - round(result)) < 1e-10:
                return int(round(result))
            else:
                # Округляем до 10 знаков
                return round(result, 10)

        return str(result)

    def clear(self):
        self.current_input = ""
        self.result_var.set("")

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.result_var.set(self.current_input)

    def bind_keyboard(self):
        self.window.bind('<Key>', self.key_press)
        self.window.bind('<Return>', lambda e: self.button_click('='))
        self.window.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        self.window.bind('<Escape>', lambda e: self.button_click('C'))
        self.window.bind('<Delete>', lambda e: self.button_click('C'))

    def key_press(self, event):
        key = event.char

        # Разрешаем только безопасные символы
        allowed_chars = '0123456789+-*/.() '
        if key in allowed_chars:
            self.button_click(key)
        elif event.keysym == 'Return':
            self.button_click('=')

        # Блокируем прямой ввод в Entry для неразрешенных символов
        if event.keysym not in ['BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Return', 'Escape']:
            return "break"

    def run(self):
        self.window.mainloop()


# Запуск графического калькулятора
if __name__ == "__main__":
    calc = Calculator()
    calc.run()