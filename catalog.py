import tkinter as tk
from tkinter import ttk, Scrollbar, Frame, Label, Button
import sqlite3


class CatalogWindow:
    def __init__(self, parent, user_id=None):
        self.parent = parent
        self.user_id = user_id
        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм с прокруткой
        self.main_frame = Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Canvas и Scrollbar для прокрутки
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Заголовок
        title_label = Label(self.scrollable_frame, text="# Каталог товаров",
                            font=("Arial", 16, "bold"), justify="left")
        title_label.pack(anchor="w", pady=(0, 20))

        # Фильтры
        self.create_filters()

        # Количество найденных товаров
        self.items_count_label = Label(self.scrollable_frame,
                                       text="## Найдено товаров: 6",
                                       font=("Arial", 12, "bold"),
                                       justify="left")
        self.items_count_label.pack(anchor="w", pady=10)

        # Разделитель
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.pack(fill='x', pady=10)

        # Товары
        self.display_products()

    def create_filters(self):
        # Фрейм для фильтров
        filters_frame = Frame(self.scrollable_frame)
        filters_frame.pack(fill="x", pady=(0, 20))

        # Цена
        price_frame = Frame(filters_frame)
        price_frame.pack(anchor="w", pady=5)

        price_label = Label(price_frame, text="## Цена", font=("Arial", 12, "bold"))
        price_label.pack(anchor="w")

        price_options = Frame(price_frame)
        price_options.pack(anchor="w", padx=20)

        Label(price_options, text="- ○ 0 ₽", justify="left").pack(anchor="w")
        Label(price_options, text="  15000 ₽", justify="left").pack(anchor="w")

        # Категория
        category_frame = Frame(filters_frame)
        category_frame.pack(anchor="w", pady=5)

        category_label = Label(category_frame, text="## Категория", font=("Arial", 12, "bold"))
        category_label.pack(anchor="w")

        category_options = Frame(category_frame)
        category_options.pack(anchor="w", padx=20)

        categories = ["Обувь", "Одежда", "Аксессуары"]
        for category in categories:
            Label(category_options, text=f"- ○ {category}", justify="left").pack(anchor="w")

        # Цвет
        color_frame = Frame(filters_frame)
        color_frame.pack(anchor="w", pady=5)

        color_label = Label(color_frame, text="## Цвет", font=("Arial", 12, "bold"))
        color_label.pack(anchor="w")

        color_options = Frame(color_frame)
        color_options.pack(anchor="w", padx=20)

        colors = ["Черный", "Белый", "Синий", "Серый"]
        for color in colors:
            Label(color_options, text=f"- ○ {color}", justify="left").pack(anchor="w")

        # Размер
        size_frame = Frame(filters_frame)
        size_frame.pack(anchor="w", pady=5)

        size_label = Label(size_frame, text="## Размер", font=("Arial", 12, "bold"))
        size_label.pack(anchor="w")

        size_options = Frame(size_frame)
        size_options.pack(anchor="w", padx=20)

        sizes = ["S", "M", "L", "XL", "42", "43", "44"]
        for size in sizes:
            Label(size_options, text=f"- ○ {size}", justify="left").pack(anchor="w")

    def display_products(self):
        # Пример товаров
        products = [
            {
                "name": "Кроссовки для бета Pro",
                "description": "Профессиональные бетовые кроссовки",
                "color": "Черный",
                "size": "42",
                "price": "8 990 ₽"
            },
            {
                "name": "Фитнес набор",
                "description": "Комплект для домашних тренировок",
                "color": "Синий",
                "size": "S",
                "price": "4 500 ₽"
            },
            {
                "name": "Опекть",
                "description": "Спортивная куртка\nЛегкая ветрозащитная куртка",
                "color": "Серый",
                "size": "L",
                "price": "6 790 ₽"
            }
        ]

        for product in products:
            self.create_product_card(product)

    def create_product_card(self, product):
        # Карточка товара
        product_frame = Frame(self.scrollable_frame, relief="groove", borderwidth=1)
        product_frame.pack(fill="x", pady=10, padx=10)

        # Информация о товаре
        info_frame = Frame(product_frame)
        info_frame.pack(fill="x", padx=10, pady=10)

        name_label = Label(info_frame, text=f"### {product['name']}",
                           font=("Arial", 11, "bold"), justify="left")
        name_label.pack(anchor="w")

        desc_label = Label(info_frame, text=product['description'],
                           justify="left")
        desc_label.pack(anchor="w")

        details_label = Label(info_frame,
                              text=f"{product['color']}\n{product['size']}",
                              justify="left")
        details_label.pack(anchor="w")

        # Цена и кнопка
        price_frame = Frame(product_frame)
        price_frame.pack(fill="x", padx=10, pady=10)

        price_label = Label(price_frame, text=f"### {product['price']}",
                            font=("Arial", 11, "bold"))
        price_label.pack(side="left")

        cart_button = Button(price_frame, text="В корзину",
                             command=lambda p=product: self.add_to_cart(p))
        cart_button.pack(side="right")

        # Разделитель
        separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)

    def add_to_cart(self, product):
        if self.user_id:
            # Добавление в корзину для зарегистрированного пользователя
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                # Проверяем, есть ли уже такой товар в корзине
                cursor.execute('''SELECT quantity FROM cart 
                                WHERE user_id = ? AND product_name = ?''',
                               (self.user_id, product['name']))
                result = cursor.fetchone()

                if result:
                    # Увеличиваем количество
                    cursor.execute('''UPDATE cart SET quantity = quantity + 1 
                                    WHERE user_id = ? AND product_name = ?''',
                                   (self.user_id, product['name']))
                else:
                    # Добавляем новый товар
                    cursor.execute('''INSERT INTO cart (user_id, product_name, price, quantity)
                                    VALUES (?, ?, ?, 1)''',
                                   (self.user_id, product['name'],
                                    float(product['price'].split()[0].replace(' ', ''))))

                conn.commit()
                conn.close()
                print(f"Товар {product['name']} добавлен в корзину")

            except sqlite3.Error as e:
                print(f"Ошибка базы данных: {e}")
        else:
            print("Для добавления в корзину необходимо авторизоваться")