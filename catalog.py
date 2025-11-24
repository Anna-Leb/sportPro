import customtkinter as ctk
from database import Database


class ProductDetailWindow:
    def __init__(self, parent, product_name, user_id, back_callback):
        self.parent = parent
        self.product_name = product_name
        self.user_id = user_id
        self.back_callback = back_callback
        self.db = Database('sports_shop.db')

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
            # Ищем товар в базе
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT product_id, name, description, price, size, model
                FROM products WHERE name = ? LIMIT 1
            ''', (self.product_name,))
            product = cursor.fetchone()
            conn.close()

            if product:
                self.display_product(product)
            else:
                self.show_error("Товар не найден")

        except Exception as e:
            print(f"Ошибка загрузки товара: {e}")
            self.show_error("Ошибка загрузки данных товара")

    def display_product(self, product):
        """Отображает информацию о товаре"""
        product_id, name, description, price, size, model = product

        # Название товара
        title_label = ctk.CTkLabel(
            self.main_frame,
            text=name,
            font=ctk.CTkFont("Arial", 24, weight="bold"),
            justify="left"
        )
        title_label.pack(anchor="w", pady=(0, 10))

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
                font=ctk.CTkFont("Arial", 16),
                justify="left",
                wraplength=800
            )
            desc_label.pack(anchor="w", pady=(0, 20))

        # Характеристики
        specs_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        specs_frame.pack(anchor="w", pady=(0, 20))

        if size:
            size_label = ctk.CTkLabel(
                specs_frame,
                text=f"Размер: {size}",
                font=ctk.CTkFont("Arial", 14),
                justify="left"
            )
            size_label.pack(anchor="w")

        if model:
            model_label = ctk.CTkLabel(
                specs_frame,
                text=f"Модель: {model}",
                font=ctk.CTkFont("Arial", 14),
                justify="left"
            )
            model_label.pack(anchor="w", pady=(5, 0))

        # Кнопка добавления в корзину
        if self.user_id:
            add_button = ctk.CTkButton(
                self.main_frame,
                text="Добавить в корзину",
                command=lambda: self.add_to_cart(product_id),
                fg_color="#2E86AB",
                hover_color="#1B5E7D",
                font=ctk.CTkFont("Arial", 16, weight="bold"),
                height=45
            )
            add_button.pack(anchor="w", pady=20)
        else:
            auth_label = ctk.CTkLabel(
                self.main_frame,
                text="Для покупки необходимо авторизоваться",
                font=ctk.CTkFont("Arial", 14),
                text_color="red"
            )
            auth_label.pack(anchor="w", pady=20)

    def add_to_cart(self, product_id):
        """Добавляет товар в корзину"""
        try:
            if self.db.add_to_cart(self.user_id, product_id):
                self.show_success("Товар добавлен в корзину!")
            else:
                self.show_error("Ошибка добавления в корзину")
        except Exception as e:
            print(f"Ошибка добавления в корзину: {e}")
            self.show_error("Ошибка добавления в корзину")

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