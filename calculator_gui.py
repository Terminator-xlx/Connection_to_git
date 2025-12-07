import tkinter as tk
from tkinter import messagebox
from calculator_core import CalculatorCore

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("400x500")
        self.window.resizable(False, False)

        self.current_input = ""
        self.result_var = tk.StringVar()
        self.core = CalculatorCore()

        self.create_widgets()
        self.bind_keyboard()

    def create_widgets(self):
        entry_frame = tk.Frame(self.window)
        entry_frame.pack(pady=20)

        self.entry = tk.Entry(entry_frame, textvariable=self.result_var,
                              font=('Arial', 16), justify='right', width=25)
        self.entry.pack()
        self.entry.focus_set()

        mode_frame = tk.Frame(self.window)
        mode_frame.pack(pady=5)

        self.mode_var = tk.StringVar(value="RAD")
        deg_radio = tk.Radiobutton(mode_frame, text="Градусы", variable=self.mode_var,
                                   value="DEG", command=self.toggle_mode)
        rad_radio = tk.Radiobutton(mode_frame, text="Радианы", variable=self.mode_var,
                                   value="RAD", command=self.toggle_mode)
        deg_radio.pack(side=tk.LEFT)
        rad_radio.pack(side=tk.LEFT)

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
        self.core.set_degrees_mode(self.mode_var.get() == "DEG")

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
            if text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'ln', 'sqrt']:
                self.current_input += text + '('
            else:
                self.current_input += text
            self.result_var.set(self.current_input)

    def calculate(self):
        try:
            result = self.core.calculate_expression(self.current_input)
            self.result_var.set(result)
            self.current_input = str(result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            self.clear()

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
        allowed_chars = '0123456789+-*/.() '
        if key in allowed_chars:
            self.button_click(key)
        elif event.keysym == 'Return':
            self.button_click('=')
        if event.keysym not in ['BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Return', 'Escape']:
            return "break"

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()