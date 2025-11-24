import customtkinter as ctk
import sqlite3
from PIL import Image, ImageTk
import os

# Настройка внешнего вида
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SportsShopApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("SportShop - Магазин спортивных товаров")
        self.window.geometry("1400x900")

        # Инициализация базы данных
        self.init_database()

        # Загрузка данных
        self.load_products_data()

        # Создаем верхнюю панель навигации
        self.create_top_navbar()

        # Основная область контента
        self.create_main_content()

    def init_database(self):
        """Инициализация базы данных и создание таблиц если их нет"""
        try:
            self.conn = sqlite3.connect('sports_shop.db')
            self.cursor = self.conn.cursor()

            # Проверяем существование таблиц и создаем их если нужно
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
            if not self.cursor.fetchone():
                self.create_tables()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def create_tables(self):
        """Создание таблиц если они не существуют"""
        # Таблица категорий
        self.cursor.execute('''
            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

        # Таблица поставщиков
        self.cursor.execute('''
            CREATE TABLE suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Таблица товаров
        self.cursor.execute('''
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                category_id INTEGER,
                size TEXT,
                model TEXT,
                supplier_id INTEGER,
                image_url TEXT,
                FOREIGN KEY (category_id) REFERENCES categories (category_id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
            )
        ''')

        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Таблица корзины
        self.cursor.execute('''
            CREATE TABLE cart (
                cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')

        # Добавляем тестовые данные
        self.insert_sample_data()

        self.conn.commit()

    def insert_sample_data(self):
        """Вставка тестовых данных"""
        # Добавляем категории
        categories = [
            ('Кроссовки', 'Спортивная обувь для бега и тренировок'),
            ('Футболки', 'Спортивные футболки и майки'),
            ('Шорты', 'Спортивные шорты для тренировок'),
            ('Аксессуары', 'Спортивные аксессуары и инвентарь'),
            ('Мячи', 'Спортивные мячи для различных видов спорта')
        ]
        self.cursor.executemany(
            'INSERT INTO categories (name, description) VALUES (?, ?)',
            categories
        )

        # Добавляем поставщиков
        suppliers = [
            ('Nike',),
            ('Adidas',),
            ('Puma',),
            ('Reebok',)
        ]
        self.cursor.executemany(
            'INSERT INTO suppliers (name) VALUES (?)',
            suppliers
        )

        # Добавляем товары
        products = [
            ('Nike Air Max', 'Беговые кроссовки с технологией Air', 129.99, 1, '42', 'Air Max 270', 1,
             'nike_air_max.jpg'),
            ('Adidas Ultraboost', 'Кроссовки для бега с технологией Boost', 149.99, 1, '41', 'Ultraboost 22', 2,
             'adidas_ultraboost.jpg'),
            ('Puma DryCell T-shirt', 'Влагоотводящая футболка для тренировок', 34.99, 2, 'M', 'DryCell', 3,
             'puma_tshirt.jpg'),
            ('Nike Dri-FIT Shorts', 'Спортивные шорты с технологией Dri-FIT', 45.99, 3, 'L', 'Dri-FIT', 1,
             'nike_shorts.jpg'),
            ('Reebok Fitness Gloves', 'Тренировочные перчатки для фитнеса', 24.99, 4, 'Universal', 'Fitness', 4,
             'reebok_gloves.jpg'),
            ('Adidas Basketball', 'Профессиональный баскетбольный мяч', 89.99, 5, '7', 'Pro', 2,
             'adidas_basketball.jpg'),
            ('Nike Running Jacket', 'Ветровка для бега с светоотражающими элементами', 79.99, 2, 'L', 'Running', 1,
             'nike_jacket.jpg'),
            ('Puma Training Shoes', 'Кроссовки для кроссфита и тренировок', 119.99, 1, '43', 'Training Pro', 3,
             'puma_training.jpg')
        ]
        self.cursor.executemany(
            'INSERT INTO products (name, description, price, category_id, size, model, supplier_id, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            products
        )

        # Добавляем тестового пользователя
        self.cursor.execute(
            'INSERT INTO users (login, password) VALUES (?, ?)',
            ('test_user', 'password123')
        )

    def load_products_data(self):
        """Загрузка данных о товарах из базы"""
        try:
            self.cursor.execute('''
                SELECT p.product_id, p.name, p.price, p.description, 
                       c.name as category, p.size, p.model, s.name as supplier,
                       p.image_url
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                ORDER BY p.product_id
            ''')

            self.products = self.cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Ошибка загрузки товаров: {e}")
            self.products = []

        # Избранные товары (в реальном приложении - из базы данных)
        self.favorites = set()

    def create_top_navbar(self):
        """Создание верхней навигационной панели"""
        self.nav_frame = ctk.CTkFrame(self.window, height=70, corner_radius=0, fg_color="#2E86AB")
        self.nav_frame.pack(fill="x", padx=0, pady=0)
        self.nav_frame.pack_propagate(False)

        # Левая часть навигации
        self.create_left_nav()

        # Правая часть навигации (иконки)
        self.create_right_nav()

    def create_left_nav(self):
        """Левая часть навигационной панели"""
        left_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=30, pady=20)

        # Логотип
        self.logo_label = ctk.CTkLabel(
            left_frame,
            text="SPORTSHOP",
            font=ctk.CTkFont("Arial", 22, weight="bold"),
            text_color="white"
        )
        self.logo_label.pack(side="left", padx=(0, 40))

        # Основные вкладки навигации
        nav_buttons = [
            ("Главная", self.show_home),
            ("Каталог", self.show_catalog),
            ("Корзина", self.show_cart),
            ("Адреса", self.show_addresses)
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                left_frame,
                text=text,
                font=ctk.CTkFont("Arial", 15),
                fg_color="transparent",
                hover_color="#1B5E7D",
                text_color="white",
                command=command,
                width=90,
                height=30
            )
            btn.pack(side="left", padx=12)

    def create_right_nav(self):
        """Правая часть навигационной панели (иконки)"""
        right_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=30, pady=20)

        # Иконки профиля, избранного и корзины
        icon_buttons = [
            ("👤", "Профиль", self.show_profile),
            ("❤️", "Избранное", self.show_favorites),
            ("🛒", "Корзина", self.show_cart_icon)
        ]

        for icon, tooltip, command in icon_buttons:
            btn = ctk.CTkButton(
                right_frame,
                text=icon,
                font=ctk.CTkFont("Arial", 18),
                fg_color="transparent",
                hover_color="#1B5E7D",
                text_color="white",
                command=command,
                width=45,
                height=35
            )
            btn.pack(side="left", padx=10)

    def create_main_content(self):
        """Создание основной области контента"""
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # По умолчанию показываем главную страницу
        self.show_home()

    def clear_main_frame(self):
        """Очистка основной области контента"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Показать главную страницу"""
        self.clear_main_frame()

        # Баннерная плашка (имитация картинки)
        banner_frame = ctk.CTkFrame(
            self.main_frame,
            height=400,
            fg_color="#E63946",
            corner_radius=0
        )
        banner_frame.pack(fill="x", pady=(0, 30))
        banner_frame.pack_propagate(False)

        # Текст поверх баннера
        banner_content = ctk.CTkFrame(banner_frame, fg_color="transparent")
        banner_content.place(relx=0.5, rely=0.5, anchor="center")

        welcome_label = ctk.CTkLabel(
            banner_content,
            text="Добро пожаловать в SportShop!",
            font=ctk.CTkFont("Arial", 32, weight="bold"),
            text_color="white"
        )
        welcome_label.pack(pady=10)

        promo_label = ctk.CTkLabel(
            banner_content,
            text="СКИДКИ ДО 50% НА СПОРТИВНЫЕ ТОВАРЫ",
            font=ctk.CTkFont("Arial", 24, weight="bold"),
            text_color="white"
        )
        promo_label.pack(pady=5)

        # Блок популярных товаров
        self.show_popular_products()

    def show_popular_products(self):
        """Показать популярные товары на главной"""
        if not self.products:
            error_label = ctk.CTkLabel(
                self.main_frame,
                text="Товары не найдены в базе данных",
                font=ctk.CTkFont("Arial", 16),
                text_color="red"
            )
            error_label.pack(pady=50)
            return

        # Заголовок блока
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=40, pady=(0, 20))

        products_label = ctk.CTkLabel(
            title_frame,
            text="Популярные товары",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        products_label.pack(side="left")

        # Контейнер для сетки товаров
        products_container = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            orientation="horizontal"
        )
        products_container.pack(fill="both", expand=True, padx=40, pady=20)

        # Создаем товары в ряд
        row_frame = ctk.CTkFrame(products_container, fg_color="transparent")
        row_frame.pack(fill="x")

        # Отображаем товары из базы данных
        for product in self.products:
            product_frame = self.create_product_card(row_frame, product)
            product_frame.pack(side="left", padx=15, fill="y")

    def create_product_card(self, parent, product):
        """Создание карточки товара в стиле Golden Apple"""
        product_id, name, price, description, category, size, model, supplier, image_url = product

        # Основной фрейм карточки
        card_frame = ctk.CTkFrame(
            parent,
            width=280,
            height=380,
            border_width=1,
            border_color="#E0E0E0",
            corner_radius=12
        )
        card_frame.pack_propagate(False)

        # Верхняя часть с изображением (заглушка)
        image_frame = ctk.CTkFrame(
            card_frame,
            height=200,
            fg_color="#F8F9FA",
            corner_radius=12
        )
        image_frame.pack(fill="x", padx=10, pady=10)
        image_frame.pack_propagate(False)

        # Заглушка изображения
        image_label = ctk.CTkLabel(
            image_frame,
            text="🛍️",
            font=ctk.CTkFont("Arial", 48),
            text_color="#6C757D"
        )
        image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Кнопка "Добавить в избранное" в правом верхнем углу
        is_favorite = product_id in self.favorites
        heart_icon = "❤️" if is_favorite else "🤍"

        favorite_btn = ctk.CTkButton(
            image_frame,
            text=heart_icon,
            font=ctk.CTkFont("Arial", 16),
            width=35,
            height=35,
            fg_color="transparent" if not is_favorite else "#FF6B6B",
            hover_color="#FF6B6B" if not is_favorite else "#FF5252",
            text_color="white" if is_favorite else "#6C757D",
            command=lambda pid=product_id: self.toggle_favorite(pid, favorite_btn)
        )
        favorite_btn.place(relx=0.9, rely=0.2, anchor="center")

        # Информация о товаре
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Название товара (кликабельное)
        name_button = ctk.CTkButton(
            info_frame,
            text=name,
            font=ctk.CTkFont("Arial", 16, weight="bold"),
            fg_color="transparent",
            hover_color="#F8F9FA",
            text_color="#2E86AB",
            command=lambda pid=product_id: self.show_product_detail(pid),
            anchor="w",
            height=30
        )
        name_button.pack(fill="x", pady=(0, 5))

        # Описание
        desc_label = ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont("Arial", 12),
            wraplength=240,
            text_color="#666666",
            justify="left"
        )
        desc_label.pack(fill="x", pady=(0, 10))

        # Цена
        price_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=5)

        price_label = ctk.CTkLabel(
            price_frame,
            text=f"${price}",
            font=ctk.CTkFont("Arial", 20, weight="bold"),
            text_color="#2E86AB"
        )
        price_label.pack(side="left")

        # Кнопка добавления в корзину
        add_btn = ctk.CTkButton(
            info_frame,
            text="В корзину",
            command=lambda pid=product_id: self.add_to_cart(pid),
            fg_color="#2E86AB",
            hover_color="#1B5E7D",
            height=35
        )
        add_btn.pack(fill="x", pady=(10, 0))

        return card_frame

    def toggle_favorite(self, product_id, button):
        """Добавить/удалить из избранного"""
        if product_id in self.favorites:
            self.favorites.remove(product_id)
            button.configure(text="🤍", fg_color="transparent", text_color="#6C757D")
        else:
            self.favorites.add(product_id)
            button.configure(text="❤️", fg_color="#FF6B6B", text_color="white")

    def show_product_detail(self, product_id):
        """Показать детальную страницу товара"""
        self.clear_main_frame()

        # Находим товар в базе данных
        self.cursor.execute('''
            SELECT p.product_id, p.name, p.price, p.description, 
                   c.name as category, p.size, p.model, s.name as supplier,
                   p.image_url
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.product_id = ?
        ''', (product_id,))

        product = self.cursor.fetchone()

        if not product:
            error_label = ctk.CTkLabel(
                self.main_frame,
                text="Товар не найден",
                font=ctk.CTkFont("Arial", 20),
                text_color="red"
            )
            error_label.pack(pady=50)
            return

        product_id, name, price, description, category, size, model, supplier, image_url = product

        # Основной контейнер
        detail_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        detail_container.pack(fill="both", expand=True, padx=40, pady=30)

        # Левая часть - изображение
        left_frame = ctk.CTkFrame(detail_container, fg_color="transparent", width=500)
        left_frame.pack(side="left", fill="both", padx=(0, 30))

        image_display = ctk.CTkFrame(
            left_frame,
            height=400,
            fg_color="#F8F9FA",
            corner_radius=12
        )
        image_display.pack(fill="both", expand=True)
        image_display.pack_propagate(False)

        image_label = ctk.CTkLabel(
            image_display,
            text="🛍️\nИзображение товара",
            font=ctk.CTkFont("Arial", 24),
            text_color="#6C757D"
        )
        image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Правая часть - информация
        right_frame = ctk.CTkFrame(detail_container, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True)

        # Название товара
        name_label = ctk.CTkLabel(
            right_frame,
            text=name,
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        name_label.pack(anchor="w", pady=(0, 10))

        # Категория
        category_label = ctk.CTkLabel(
            right_frame,
            text=f"Категория: {category}",
            font=ctk.CTkFont("Arial", 16),
            text_color="#666666"
        )
        category_label.pack(anchor="w", pady=(0, 20))

        # Цена
        price_label = ctk.CTkLabel(
            right_frame,
            text=f"${price}",
            font=ctk.CTkFont("Arial", 32, weight="bold"),
            text_color="#2E86AB"
        )
        price_label.pack(anchor="w", pady=(0, 20))

        # Описание
        desc_label = ctk.CTkLabel(
            right_frame,
            text="Описание:",
            font=ctk.CTkFont("Arial", 18, weight="bold")
        )
        desc_label.pack(anchor="w", pady=(0, 10))

        desc_text = ctk.CTkLabel(
            right_frame,
            text=description,
            font=ctk.CTkFont("Arial", 14),
            wraplength=600,
            justify="left"
        )
        desc_text.pack(anchor="w", pady=(0, 20))

        # Характеристики
        specs_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        specs_frame.pack(anchor="w", fill="x", pady=(0, 20))

        specs = [
            ("Размер:", size),
            ("Модель:", model),
            ("Поставщик:", supplier)
        ]

        for spec_name, spec_value in specs:
            spec_frame = ctk.CTkFrame(specs_frame, fg_color="transparent")
            spec_frame.pack(anchor="w", pady=5)

            spec_name_label = ctk.CTkLabel(
                spec_frame,
                text=spec_name,
                font=ctk.CTkFont("Arial", 14, weight="bold"),
                width=100,
                anchor="w"
            )
            spec_name_label.pack(side="left")

            spec_value_label = ctk.CTkLabel(
                spec_frame,
                text=spec_value,
                font=ctk.CTkFont("Arial", 14)
            )
            spec_value_label.pack(side="left")

        # Кнопки действий
        actions_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        actions_frame.pack(anchor="w", fill="x", pady=20)

        add_to_cart_btn = ctk.CTkButton(
            actions_frame,
            text="Добавить в корзину",
            fg_color="#2E86AB",
            hover_color="#1B5E7D",
            height=45,
            width=200,
            font=ctk.CTkFont("Arial", 16),
            command=lambda pid=product_id: self.add_to_cart(pid)
        )
        add_to_cart_btn.pack(side="left", padx=(0, 15))

        is_favorite = product_id in self.favorites
        favorite_btn = ctk.CTkButton(
            actions_frame,
            text="❤️ В избранное" if is_favorite else "🤍 В избранное",
            fg_color="#FF6B6B" if is_favorite else "transparent",
            hover_color="#FF5252",
            text_color="white" if is_favorite else "#6C757D",
            border_color="#FF6B6B" if not is_favorite else "#FF5252",
            border_width=1 if not is_favorite else 0,
            height=45,
            width=150,
            font=ctk.CTkFont("Arial", 16),
            command=lambda: self.toggle_favorite(product_id, favorite_btn)
        )
        favorite_btn.pack(side="left")

        # Кнопка назад
        back_btn = ctk.CTkButton(
            actions_frame,
            text="← Назад",
            fg_color="transparent",
            hover_color="#F8F9FA",
            text_color="#666666",
            border_color="#666666",
            border_width=1,
            height=45,
            width=100,
            font=ctk.CTkFont("Arial", 14),
            command=self.show_home
        )
        back_btn.pack(side="left", padx=(20, 0))

    def show_catalog(self):
        """Показать полный каталог товаров"""
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Каталог товаров",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        title.pack(pady=20)

        # Здесь будет реализация полного каталога
        catalog_label = ctk.CTkLabel(
            self.main_frame,
            text="Полный каталог товаров будет здесь...",
            font=ctk.CTkFont("Arial", 16)
        )
        catalog_label.pack(pady=50)

    def show_cart(self):
        """Показать корзину"""
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Корзина",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        title.pack(pady=20)

        # Здесь будет содержимое корзины из базы данных
        cart_label = ctk.CTkLabel(
            self.main_frame,
            text="Содержимое вашей корзины...",
            font=ctk.CTkFont("Arial", 16)
        )
        cart_label.pack(pady=50)

    def show_addresses(self):
        """Показать адреса магазинов"""
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Наши магазины",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        title.pack(pady=20)

        addresses_label = ctk.CTkLabel(
            self.main_frame,
            text="Адреса наших магазинов будут здесь...",
            font=ctk.CTkFont("Arial", 16)
        )
        addresses_label.pack(pady=50)

    def show_profile(self):
        """Показать профиль пользователя"""
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Личный кабинет",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        title.pack(pady=20)

        profile_label = ctk.CTkLabel(
            self.main_frame,
            text="Информация о вашем профиле...",
            font=ctk.CTkFont("Arial", 16)
        )
        profile_label.pack(pady=50)

    def show_favorites(self):
        """Показать избранное"""
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Избранное",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        title.pack(pady=20)

        favorites_label = ctk.CTkLabel(
            self.main_frame,
            text="Ваши избранные товары...",
            font=ctk.CTkFont("Arial", 16)
        )
        favorites_label.pack(pady=50)

    def show_cart_icon(self):
        """Показать корзину (при клике на иконку)"""
        self.show_cart()

    def add_to_cart(self, product_id):
        """Добавить товар в корзину"""
        try:
            # Добавляем товар в корзину для текущего пользователя (user_id = 1 для демо)
            self.cursor.execute(
                'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)',
                (1, product_id)
            )
            self.conn.commit()
            print(f"Товар {product_id} добавлен в корзину")
        except sqlite3.Error as e:
            print(f"Ошибка добавления в корзину: {e}")

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

    def __del__(self):
        """Закрытие соединения с базой данных при уничтожении объекта"""
        if hasattr(self, 'conn'):
            self.conn.close()



app = SportsShopApp()
app.run()