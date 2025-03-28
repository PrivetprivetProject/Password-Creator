import random
import string
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip  # Для копирования в буфер обмена


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Параметры пароля по умолчанию
        self.params = {
            'length': 12,
            'digits': True,
            'special': True,
            'uppercase': True,
            'lowercase': True,
            'exclude_similar': True
        }

        self.create_widgets()

    def create_widgets(self):
        # Стиль
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 9))
        style.configure('Toggle.TButton', font=('Arial', 9))
        style.map('Toggle.TButton',
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '#45a049'), ('active', '#4CAF50')])

        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(main_frame, text="Генератор паролей", font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 15))

        # Фрейм для длины пароля
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill=tk.X, pady=5)

        ttk.Label(length_frame, text="Длина пароля:").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=self.params['length'])
        length_spinbox = tk.Spinbox(length_frame, from_=8, to=64, textvariable=self.length_var, width=5)
        length_spinbox.pack(side=tk.LEFT, padx=5)

        # Фрейм для кнопок параметров
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)

        # Кнопки параметров (переключатели)
        self.digits_btn = ttk.Button(options_frame, text="Цифры (вкл)", style='Toggle.TButton',
                                     command=lambda: self.toggle_param('digits'))
        self.digits_btn.pack(fill=tk.X, pady=2)

        self.special_btn = ttk.Button(options_frame, text="Спецсимволы (вкл)", style='Toggle.TButton',
                                      command=lambda: self.toggle_param('special'))
        self.special_btn.pack(fill=tk.X, pady=2)

        self.upper_btn = ttk.Button(options_frame, text="Заглавные буквы (вкл)", style='Toggle.TButton',
                                    command=lambda: self.toggle_param('uppercase'))
        self.upper_btn.pack(fill=tk.X, pady=2)

        self.lower_btn = ttk.Button(options_frame, text="Строчные буквы (вкл)", style='Toggle.TButton',
                                    command=lambda: self.toggle_param('lowercase'))
        self.lower_btn.pack(fill=tk.X, pady=2)

        self.similar_btn = ttk.Button(options_frame, text="Исключить похожие символы (вкл)", style='Toggle.TButton',
                                      command=lambda: self.toggle_param('exclude_similar'))
        self.similar_btn.pack(fill=tk.X, pady=2)

        # Кнопка генерации
        generate_btn = ttk.Button(main_frame, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.pack(pady=15)

        # Поле для отображения пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, font=('Arial', 12), state='readonly')
        password_entry.pack(fill=tk.X, pady=5)

        # Кнопка копирования
        copy_btn = ttk.Button(main_frame, text="Копировать в буфер", command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)

    def toggle_param(self, param):
        """Переключает параметр и обновляет кнопку"""
        self.params[param] = not self.params[param]
        status = "вкл" if self.params[param] else "выкл"

        if param == 'digits':
            self.digits_btn.config(text=f"Цифры ({status})")
        elif param == 'special':
            self.special_btn.config(text=f"Спецсимволы ({status})")
        elif param == 'uppercase':
            self.upper_btn.config(text=f"Заглавные буквы ({status})")
        elif param == 'lowercase':
            self.lower_btn.config(text=f"Строчные буквы ({status})")
        elif param == 'exclude_similar':
            self.similar_btn.config(text=f"Исключить похожие символы ({status})")

    def generate_password(self):
        """Генерирует пароль на основе выбранных параметров"""
        self.params['length'] = self.length_var.get()

        characters = ""

        if self.params['digits']:
            characters += string.digits
        if self.params['uppercase']:
            characters += string.ascii_uppercase
        if self.params['lowercase']:
            characters += string.ascii_lowercase
        if self.params['special']:
            characters += string.punctuation

        if self.params['exclude_similar']:
            similar_chars = 'l1IioO0'
            characters = ''.join([c for c in characters if c not in similar_chars])

        if not characters:
            messagebox.showerror("Ошибка", "Не выбрано ни одного типа символов!")
            return

        # Гарантируем хотя бы один символ каждого выбранного типа
        password = []
        if self.params['digits']:
            password.append(random.choice(string.digits))
        if self.params['uppercase']:
            password.append(random.choice(string.ascii_uppercase))
        if self.params['lowercase']:
            password.append(random.choice(string.ascii_lowercase))
        if self.params['special']:
            password.append(random.choice(string.punctuation))

        # Добираем остальные символы
        remaining_length = self.params['length'] - len(password)
        if remaining_length > 0:
            password.extend(random.choice(characters) for _ in range(remaining_length))

        # Перемешиваем символы
        random.shuffle(password)

        self.password_var.set(''.join(password))

    def copy_to_clipboard(self):
        """Копирует пароль в буфер обмена"""
        password = self.password_var.get()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
            except:
                messagebox.showerror("Ошибка", "Не удалось скопировать пароль")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()