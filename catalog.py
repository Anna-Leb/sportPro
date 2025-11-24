import customtkinter as ctk
from database import Database


class CatalogWindow:
    def __init__(self, parent, user_id=None):
        self.parent = parent
        self.user_id = user_id
        self.db = Database('sports_shop.db')

        # Переменные для фильтров
        self.selected_categories = []
        self.selected_colors = []
        self.selected_sizes = []
        self.min_price = 0
        self.max_price = 15000

        self.create_widgets()
        self.load_filters_data()
        self.apply_filters()

    def create_widgets(self):
        # Основной контейнер
        main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_container,
            text="# Каталог товаров",
            font=ctk.CTkFont("Arial", 20, weight="bold"),
            justify="left"
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # Контейнер для фильтров и товаров
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Левая панель - фильтры (20% ширины)
        self.filters_frame = ctk.CTkFrame(content_frame, width=300)
        self.filters_frame.pack(side="left", fill="y", padx=(0, 20))
        self.filters_frame.pack_propagate(False)

        # Правая панель - товары (80% ширины)
        self.products_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.products_frame.pack(side="right", fill="both", expand=True)

        # Создаем фильтры
        self.create_filters()

    def create_filters(self):
        # Заголовок фильтров
        filters_title = ctk.CTkLabel(
            self.filters_frame,
            text="Фильтры",
            font=ctk.CTkFont("Arial", 18, weight="bold")
        )
        filters_title.pack(pady=10)

        # Цена
        self.create_price_filter()

        # Разделитель
        separator1 = ctk.CTkFrame(self.filters_frame, height=1, fg_color="#E0E0E0")
        separator1.pack(fill='x', pady=10, padx=10)

        # Категория
        self.create_category_filter()

        # Разделитель
        separator2 = ctk.CTkFrame(self.filters_frame, height=1, fg_color="#E0E0E0")
        separator2.pack(fill='x', pady=10, padx=10)

        # Цвет
        self.create_color_filter()

        # Разделитель
        separator3 = ctk.CTkFrame(self.filters_frame, height=1, fg_color="#E0E0E0")
        separator3.pack(fill='x', pady=10, padx=10)

        # Размер
        self.create_size_filter()

        # Кнопка применения фильтров
        apply_btn = ctk.CTkButton(
            self.filters_frame,
            text="Применить фильтры",
            command=self.apply_filters,
            fg_color="#2E86AB",
            hover_color="#1B5E7D"
        )
        apply_btn.pack(pady=20, padx=10, fill="x")

        # Кнопка сброса
        reset_btn = ctk.CTkButton(
            self.filters_frame,
            text="Сбросить фильтры",
            command=self.reset_filters,
            fg_color="#6C757D",
            hover_color="#5A6268"
        )
        reset_btn.pack(pady=(0, 20), padx=10, fill="x")

    def create_price_filter(self):
        price_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        price_frame.pack(fill="x", padx=10, pady=5)

        price_label = ctk.CTkLabel(
            price_frame,
            text="Цена, ₽",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        )
        price_label.pack(anchor="w")

        # Поля ввода цены
        price_input_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        price_input_frame.pack(fill="x", pady=5)

        self.min_price_entry = ctk.CTkEntry(
            price_input_frame,
            placeholder_text="0",
            width=80
        )
        self.min_price_entry.pack(side="left")
        self.min_price_entry.insert(0, "0")

        ctk.CTkLabel(price_input_frame, text="-").pack(side="left", padx=5)

        self.max_price_entry = ctk.CTkEntry(
            price_input_frame,
            placeholder_text="15000",
            width=80
        )
        self.max_price_entry.pack(side="left")
        self.max_price_entry.insert(0, "15000")

    def create_category_filter(self):
        category_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        category_frame.pack(fill="x", padx=10, pady=5)

        category_label = ctk.CTkLabel(
            category_frame,
            text="Категория",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        )
        category_label.pack(anchor="w")

        self.category_checkboxes = {}
        self.category_var = {}

        # Заглушка - данные загрузятся позже
        loading_label = ctk.CTkLabel(
            category_frame,
            text="Загрузка...",
            font=ctk.CTkFont("Arial", 12)
        )
        loading_label.pack(anchor="w", pady=2)
        self.category_loading_label = loading_label

    def create_color_filter(self):
        color_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        color_frame.pack(fill="x", padx=10, pady=5)

        color_label = ctk.CTkLabel(
            color_frame,
            text="Цвет",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        )
        color_label.pack(anchor="w")

        self.color_checkboxes = {}
        self.color_var = {}

        # Заглушка - данные загрузятся позже
        loading_label = ctk.CTkLabel(
            color_frame,
            text="Загрузка...",
            font=ctk.CTkFont("Arial", 12)
        )
        loading_label.pack(anchor="w", pady=2)
        self.color_loading_label = loading_label

    def create_size_filter(self):
        size_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=10, pady=5)

        size_label = ctk.CTkLabel(
            size_frame,
            text="Размер",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        )
        size_label.pack(anchor="w")

        self.size_checkboxes = {}
        self.size_var = {}

        # Заглушка - данные загрузятся позже
        loading_label = ctk.CTkLabel(
            size_frame,
            text="Загрузка...",
            font=ctk.CTkFont("Arial", 12)
        )
        loading_label.pack(anchor="w", pady=2)
        self.size_loading_label = loading_label

    def load_filters_data(self):
        """Загружает данные для фильтров из базы"""
        try:
            # Категории
            categories = self.db.get_categories()
            self.category_loading_label.destroy()

            for category in categories:
                category_id, name, description = category
                var = ctk.BooleanVar()
                checkbox = ctk.CTkCheckBox(
                    self.category_checkboxes.master,  # parent frame
                    text=name,
                    variable=var,
                    font=ctk.CTkFont("Arial", 12)
                )
                checkbox.pack(anchor="w", pady=2)
                self.category_checkboxes[category_id] = checkbox
                self.category_var[category_id] = var

            # Цвета
            colors_data = self.db.get_unique_colors()
            self.color_loading_label.destroy()

            for color_data in colors_data:
                color = color_data[0]
                if color and color != 'Не указан':
                    var = ctk.BooleanVar()
                    checkbox = ctk.CTkCheckBox(
                        self.color_checkboxes.master,
                        text=color,
                        variable=var,
                        font=ctk.CTkFont("Arial", 12)
                    )
                    checkbox.pack(anchor="w", pady=2)
                    self.color_checkboxes[color] = checkbox
                    self.color_var[color] = var

            # Размеры
            sizes_data = self.db.get_unique_sizes()
            self.size_loading_label.destroy()

            for size_data in sizes_data:
                size = size_data[0]
                if size:
                    var = ctk.BooleanVar()
                    checkbox = ctk.CTkCheckBox(
                        self.size_checkboxes.master,
                        text=size,
                        variable=var,
                        font=ctk.CTkFont("Arial", 12)
                    )
                    checkbox.pack(anchor="w", pady=2)
                    self.size_checkboxes[size] = checkbox
                    self.size_var[size] = var

        except Exception as e:
            print(f"Ошибка загрузки фильтров: {e}")

    def apply_filters(self):
        """Применяет фильтры и обновляет список товаров"""
        try:
            # Получаем выбранные фильтры
            self.selected_categories = [
                category_id for category_id, var in self.category_var.items()
                if var.get()
            ] if hasattr(self, 'category_var') else []

            self.selected_colors = [
                color for color, var in self.color_var.items()
                if var.get()
            ] if hasattr(self, 'color_var') else []

            self.selected_sizes = [
                size for size, var in self.size_var.items()
                if var.get()
            ] if hasattr(self, 'size_var') else []

            # Получаем цену
            try:
                self.min_price = int(self.min_price_entry.get())
            except:
                self.min_price = 0

            try:
                self.max_price = int(self.max_price_entry.get())
            except:
                self.max_price = 15000

            # Загружаем отфильтрованные товары
            self.display_products()

        except Exception as e:
            print(f"Ошибка применения фильтров: {e}")

    def reset_filters(self):
        """Сбрасывает все фильтры"""
        # Сбрасываем чекбоксы
        for var in self.category_var.values():
            var.set(False)
        for var in self.color_var.values():
            var.set(False)
        for var in self.size_var.values():
            var.set(False)

        # Сбрасываем цену
        self.min_price_entry.delete(0, 'end')
        self.min_price_entry.insert(0, "0")
        self.max_price_entry.delete(0, 'end')
        self.max_price_entry.insert(0, "15000")

        # Применяем сброс
        self.apply_filters()

    def display_products(self):
        """Отображает товары с учетом фильтров"""
        # Очищаем предыдущие товары
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        # Заголовок с количеством
        count_label = ctk.CTkLabel(
            self.products_frame,
            text=f"Найдено товаров: {6}",  # Заглушка
            font=ctk.CTkFont("Arial", 16, weight="bold")
        )
        count_label.pack(anchor="w", pady=(0, 20))

        # Получаем товары из базы
        try:
            products_data = self.db.get_products_grouped()

            if not products_data:
                no_products_label = ctk.CTkLabel(
                    self.products_frame,
                    text="Товары не найдены",
                    font=ctk.CTkFont("Arial", 16),
                    text_color="#666666"
                )
                no_products_label.pack(pady=50)
                return

            # Обновляем счетчик
            count_label.configure(text=f"Найдено товаров: {len(products_data)}")

            # Отображаем товары
            for product in products_data:
                self.create_product_card(product)

        except Exception as e:
            print(f"Ошибка загрузки товаров: {e}")
            # Пример товаров если база недоступна
            example_products = [
                ("Футболка спортивная", "Удобная футболка для тренировок", 1500, 2000,
                 "Белый,Черный,Красный", "S,M,L,XL", "Classic", "Одежда", "Nike"),
                ("Кроссовки для бега", "Профессиональные беговые кроссовки", 8990, 8990,
                 "Черный,Синий", "42,43,44", "Air Max", "Обувь", "Nike"),
                ("Фитнес набор", "Комплект для домашних тренировок", 4500, 4500,
                 "Синий,Серый", "S,M", "Home Gym", "Аксессуары", "Adidas")
            ]

            count_label.configure(text=f"Найдено товаров: {len(example_products)}")

            for product in example_products:
                self.create_product_card(product)

    def create_product_card(self, product):
        """Создает карточку товара"""
        if len(product) >= 9:
            name, description, min_price, max_price, colors, sizes, models, category, supplier = product
        else:
            # Для примера товаров
            name, description, min_price, max_price, colors, sizes = product
            models, category, supplier = "", "Категория", "Поставщик"

        # Карточка товара
        product_frame = ctk.CTkFrame(
            self.products_frame,
            border_width=1,
            border_color="#E0E0E0",
            corner_radius=12
        )
        product_frame.pack(fill="x", pady=10)

        # Основной контент карточки
        content_frame = ctk.CTkFrame(product_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)

        # Верхняя часть - название и описание
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x")

        # Название и категория
        name_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        name_frame.pack(fill="x")

        name_label = ctk.CTkLabel(
            name_frame,
            text=name,
            font=ctk.CTkFont("Arial", 18, weight="bold"),
            justify="left"
        )
        name_label.pack(side="left")

        category_label = ctk.CTkLabel(
            name_frame,
            text=category,
            font=ctk.CTkFont("Arial", 12),
            text_color="#666666"
        )
        category_label.pack(side="right")

        # Описание
        if description:
            desc_label = ctk.CTkLabel(
                top_frame,
                text=description,
                font=ctk.CTkFont("Arial", 14),
                justify="left",
                wraplength=600
            )
            desc_label.pack(anchor="w", pady=(5, 0))

        # Средняя часть - характеристики
        if colors or sizes:
            specs_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            specs_frame.pack(fill="x", pady=10)

            if colors and colors != 'Не указан':
                colors_text = colors.replace(',', ', ')
                color_label = ctk.CTkLabel(
                    specs_frame,
                    text=f"Цвета: {colors_text}",
                    font=ctk.CTkFont("Arial", 12),
                    justify="left"
                )
                color_label.pack(anchor="w")

            if sizes:
                sizes_text = sizes.replace(',', ', ')
                size_label = ctk.CTkLabel(
                    specs_frame,
                    text=f"Размеры: {sizes_text}",
                    font=ctk.CTkFont("Arial", 12),
                    justify="left"
                )
                size_label.pack(anchor="w", pady=(2, 0))

        # Нижняя часть - цена и кнопка
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")

        # Цена
        if min_price == max_price:
            price_text = f"{min_price:.0f} ₽"
        else:
            price_text = f"{min_price:.0f} - {max_price:.0f} ₽"

        price_label = ctk.CTkLabel(
            bottom_frame,
            text=price_text,
            font=ctk.CTkFont("Arial", 20, weight="bold"),
            text_color="#2E86AB"
        )
        price_label.pack(side="left")

        # Кнопка "В корзину"
        cart_button = ctk.CTkButton(
            bottom_frame,
            text="В корзину",
            command=lambda p=name: self.add_to_cart(p),
            fg_color="#2E86AB",
            hover_color="#1B5E7D",
            width=120,
            height=35
        )
        cart_button.pack(side="right")

    def add_to_cart(self, product_name):
        if self.user_id:
            try:
                # Находим первый товар с таким названием
                products = self.db.get_products()
                product_id = None
                for product in products:
                    if product[1] == product_name:  # product[1] - название
                        product_id = product[0]
                        break

                if product_id:
                    if self.db.add_to_cart(self.user_id, product_id):
                        print(f"Товар {product_name} добавлен в корзину")
                    else:
                        print("Ошибка добавления в корзину")
                else:
                    print("Товар не найден в базе данных")

            except Exception as e:
                print(f"Ошибка базы данных: {e}")
        else:
            print("Для добавления в корзину необходимо авторизоваться")