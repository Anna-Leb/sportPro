import customtkinter as ctk
from database import Database


class ProductDetailWindow:
    def __init__(self, parent, product_name, user_id, back_callback):
        self.parent = parent
        self.product_name = product_name
        self.user_id = user_id
        self.back_callback = back_callback
        self.db = Database('sports_shop.db')
        self.selected_color = None
        self.selected_size = None

        self.create_widgets()
        self.load_product_data()

    def create_widgets(self):
        # Основной контейнер с прокруткой
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent",
            scrollbar_button_color="#2E86AB"
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Кнопка назад
        back_button = ctk.CTkButton(
            self.main_frame,
            text="← Назад к каталогу",
            command=self.back_callback,
            fg_color="transparent",
            hover_color="#F0F0F0",
            text_color="#2E86AB",
            font=ctk.CTkFont("Arial", 14)
        )
        back_button.pack(anchor="w", pady=(0, 20))

    def load_product_data(self):
        """Загружает данные о товаре"""
        try:
            variants = self.db.get_product_variants(self.product_name)
            if not variants:
                self.show_error("Товар не найден")
                return

            # Берем первый вариант для основной информации
            first_variant = variants[0]
            product_id, name, description, price, size, color, model, category, supplier, stock = first_variant

            # Основная информация о товаре
            title_label = ctk.CTkLabel(
                self.main_frame,
                text=name,
                font=ctk.CTkFont("Arial", 24, weight="bold"),
                justify="left"
            )
            title_label.pack(anchor="w", pady=(0, 10))

            # Рейтинг и артикул
            info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            info_frame.pack(anchor="w", pady=(0, 20))

            rating_label = ctk.CTkLabel(
                info_frame,
                text="⭐ 4,8 · 320 оценок",
                font=ctk.CTkFont("Arial", 14),
                text_color="#666666"
            )
            rating_label.pack(side="left")

            article_label = ctk.CTkLabel(
                info_frame,
                text=f"Арт: {product_id}",
                font=ctk.CTkFont("Arial", 14),
                text_color="#666666"
            )
            article_label.pack(side="left", padx=(20, 0))

            # Разделитель
            separator1 = ctk.CTkFrame(self.main_frame, height=2, fg_color="#E0E0E0")
            separator1.pack(fill='x', pady=10)

            # Цена
            price_label = ctk.CTkLabel(
                self.main_frame,
                text=f"{price} ₽",
                font=ctk.CTkFont("Arial", 28, weight="bold"),
                text_color="#2E86AB"
            )
            price_label.pack(anchor="w", pady=(0, 20))

            # Описание
            if description:
                desc_label = ctk.CTkLabel(
                    self.main_frame,
                    text=description,
                    font=ctk.CTkFont("Arial", 14),
                    justify="left",
                    wraplength=800
                )
                desc_label.pack(anchor="w", pady=(0, 20))

            # Выбор цвета
            self.create_color_selector(variants)

            # Выбор размера
            self.create_size_selector(variants)

            # Кнопка добавления в корзину
            add_button = ctk.CTkButton(
                self.main_frame,
                text="Добавить в корзину",
                command=self.add_to_cart,
                fg_color="#2E86AB",
                hover_color="#1B5E7D",
                font=ctk.CTkFont("Arial", 16, weight="bold"),
                height=45
            )
            add_button.pack(anchor="w", pady=20)

            # Информация о доставке и возврате
            self.create_additional_info()

        except Exception as e:
            print(f"Ошибка загрузки данных товара: {e}")
            self.show_error("Ошибка загрузки данных товара")

    def create_color_selector(self, variants):
        """Создает селектор цвета"""
        color_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        color_frame.pack(anchor="w", pady=(0, 20))

        color_label = ctk.CTkLabel(
            color_frame,
            text="Цвет:",
            font=ctk.CTkFont("Arial", 16, weight="bold")
        )
        color_label.pack(anchor="w")

        # Уникальные цвета
        unique_colors = list(set([variant[5] for variant in variants if variant[5]]))

        self.color_var = ctk.StringVar()
        color_options = ctk.CTkFrame(color_frame, fg_color="transparent")
        color_options.pack(anchor="w", pady=5)

        for i, color in enumerate(unique_colors):
            if color:
                radio = ctk.CTkRadioButton(
                    color_options,
                    text=color,
                    variable=self.color_var,
                    value=color,
                    font=ctk.CTkFont("Arial", 14),
                    command=self.on_color_selected
                )
                radio.pack(anchor="w", pady=2)
                if i == 0:
                    radio.select()
                    self.selected_color = color

    def create_size_selector(self, variants):
        """Создает селектор размера"""
        size_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        size_frame.pack(anchor="w", pady=(0, 20))

        size_label = ctk.CTkLabel(
            size_frame,
            text="Размер:",
            font=ctk.CTkFont("Arial", 16, weight="bold")
        )
        size_label.pack(anchor="w")

        # Уникальные размеры
        unique_sizes = list(set([variant[4] for variant in variants if variant[4]]))

        self.size_var = ctk.StringVar()
        size_options = ctk.CTkFrame(size_frame, fg_color="transparent")
        size_options.pack(anchor="w", pady=5)

        for i, size in enumerate(unique_sizes):
            if size:
                radio = ctk.CTkRadioButton(
                    size_options,
                    text=size,
                    variable=self.size_var,
                    value=size,
                    font=ctk.CTkFont("Arial", 14),
                    command=self.on_size_selected
                )
                radio.pack(anchor="w", pady=2)
                if i == 0:
                    radio.select()
                    self.selected_size = size

    def on_color_selected(self):
        """Обработчик выбора цвета"""
        self.selected_color = self.color_var.get()

    def on_size_selected(self):
        """Обработчик выбора размера"""
        self.selected_size = self.size_var.get()

    def add_to_cart(self):
        """Добавляет выбранный вариант в корзину"""
        if not self.user_id:
            self.show_error("Для добавления в корзину необходимо авторизоваться")
            return

        if not self.selected_color or not self.selected_size:
            self.show_error("Выберите цвет и размер")
            return

        try:
            # Находим конкретный вариант товара
            variants = self.db.get_product_variants(self.product_name)
            selected_variant = None

            for variant in variants:
                product_id, name, description, price, size, color, model, category, supplier, stock = variant
                if color == self.selected_color and size == self.selected_size:
                    selected_variant = variant
                    break

            if not selected_variant:
                self.show_error("Выбранный вариант недоступен")
                return

            # Проверяем наличие на складе
            stock_quantity = self.db.check_product_availability(
                selected_variant[0], self.selected_color, self.selected_size
            )

            if stock_quantity == 0:
                self.show_error("Товара нет в наличии")
                return

            # Добавляем в корзину
            if self.db.add_to_cart(self.user_id, selected_variant[0]):
                self.show_success("Товар добавлен в корзину!")
            else:
                self.show_error("Ошибка добавления в корзину")

        except Exception as e:
            print(f"Ошибка добавления в корзину: {e}")
            self.show_error("Ошибка добавления в корзину")

    def create_additional_info(self):
        """Создает блок с дополнительной информацией"""
        info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        info_frame.pack(anchor="w", pady=20)

        # Гарантии
        guarantees = [
            "✓ 14 дней на возврат",
            "✓ Есть примерка",
            "✓ Бесплатная доставка от 3000 ₽"
        ]

        for guarantee in guarantees:
            label = ctk.CTkLabel(
                info_frame,
                text=guarantee,
                font=ctk.CTkFont("Arial", 14),
                justify="left"
            )
            label.pack(anchor="w", pady=2)

    def show_error(self, message):
        """Показывает сообщение об ошибке"""
        error_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            font=ctk.CTkFont("Arial", 14),
            text_color="red"
        )
        error_label.pack(anchor="w", pady=10)

    def show_success(self, message):
        """Показывает сообщение об успехе"""
        success_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            font=ctk.CTkFont("Arial", 14),
            text_color="green"
        )
        success_label.pack(anchor="w", pady=10)