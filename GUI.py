import customtkinter as ctk
from database import Database
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
        self.db = Database('sports_shop.db')
        self.current_user_id = None
        self.current_user_login = None

        # Загрузка данных
        self.load_products_data()

        # Создаем верхнюю панель навигации
        self.create_top_navbar()

        # Основная область контента
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Фрейм для авторизации (изначально скрыт)
        self.auth_frame = None

        # По умолчанию показываем главную страницу
        self.show_home()

    # === МЕТОДЫ АВТОРИЗАЦИИ ===
    def create_auth_frame(self):
        """Создает фрейм авторизации/регистрации"""
        if self.auth_frame:
            self.auth_frame.destroy()

        self.auth_frame = ctk.CTkFrame(
            self.window,
            width=300,
            height=400,
            corner_radius=15,
            fg_color="white",
            border_width=1,
            border_color="#E0E0E0"
        )
        self.auth_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.auth_frame.pack_propagate(False)

        # По умолчанию показываем форму входа
        self.show_login_form()

    def show_login_form(self):
        """Показывает форму входа"""
        if not self.auth_frame:
            return

        # Очищаем фрейм
        for widget in self.auth_frame.winfo_children():
            widget.destroy()

        # Заголовок
        title_label = ctk.CTkLabel(
            self.auth_frame,
            text="Вход в аккаунт",
            font=ctk.CTkFont("Arial", 20, weight="bold"),
            text_color="#333333"
        )
        title_label.pack(pady=30)

        # Поле логина
        self.login_entry = ctk.CTkEntry(
            self.auth_frame,
            placeholder_text="Логин",
            width=220,
            height=40,
            fg_color="#F8F9FA",
            border_color="#E0E0E0"
        )
        self.login_entry.pack(pady=10)

        # Поле пароля
        self.password_entry = ctk.CTkEntry(
            self.auth_frame,
            placeholder_text="Пароль",
            show="*",
            width=220,
            height=40,
            fg_color="#F8F9FA",
            border_color="#E0E0E0"
        )
        self.password_entry.pack(pady=10)

        # Кнопка входа
        login_btn = ctk.CTkButton(
            self.auth_frame,
            text="Войти",
            command=self.login,
            width=220,
            height=40,
            fg_color="#2E86AB",
            hover_color="#1B5E7D"
        )
        login_btn.pack(pady=10)

        # Ссылка на регистрацию
        register_label = ctk.CTkLabel(
            self.auth_frame,
            text="Нет аккаунта? Зарегистрироваться",
            text_color="#2E86AB",
            cursor="hand2",
            font=ctk.CTkFont("Arial", 12)
        )
        register_label.pack(pady=10)
        register_label.bind("<Button-1>", lambda e: self.show_register_form())

        # Сообщение об ошибке
        self.error_label = ctk.CTkLabel(
            self.auth_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont("Arial", 11)
        )
        self.error_label.pack(pady=5)

        # Кнопка закрытия
        close_btn = ctk.CTkButton(
            self.auth_frame,
            text="✕",
            command=self.hide_auth_frame,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#F0F0F0",
            text_color="#666666",
            font=ctk.CTkFont("Arial", 14)
        )
        close_btn.place(relx=0.9, rely=0.05, anchor="center")

    def show_register_form(self):
        """Показывает форму регистрации"""
        if not self.auth_frame:
            return

        # Очищаем фрейм
        for widget in self.auth_frame.winfo_children():
            widget.destroy()

        # Заголовок
        title_label = ctk.CTkLabel(
            self.auth_frame,
            text="Регистрация",
            font=ctk.CTkFont("Arial", 20, weight="bold"),
            text_color="#333333"
        )
        title_label.pack(pady=25)

        # Поле логина
        self.reg_login_entry = ctk.CTkEntry(
            self.auth_frame,
            placeholder_text="Логин",
            width=220,
            height=40,
            fg_color="#F8F9FA",
            border_color="#E0E0E0"
        )
        self.reg_login_entry.pack(pady=8)

        # Поле пароля
        self.reg_password_entry = ctk.CTkEntry(
            self.auth_frame,
            placeholder_text="Пароль",
            show="*",
            width=220,
            height=40,
            fg_color="#F8F9FA",
            border_color="#E0E0E0"
        )
        self.reg_password_entry.pack(pady=8)

        # Подтверждение пароля
        self.reg_confirm_password_entry = ctk.CTkEntry(
            self.auth_frame,
            placeholder_text="Подтвердите пароль",
            show="*",
            width=220,
            height=40,
            fg_color="#F8F9FA",
            border_color="#E0E0E0"
        )
        self.reg_confirm_password_entry.pack(pady=8)

        # Кнопка регистрации
        register_btn = ctk.CTkButton(
            self.auth_frame,
            text="Зарегистрироваться",
            command=self.register,
            width=220,
            height=40,
            fg_color="#2E86AB",
            hover_color="#1B5E7D"
        )
        register_btn.pack(pady=10)

        # Ссылка на вход
        login_label = ctk.CTkLabel(
            self.auth_frame,
            text="Уже есть аккаунт? Войти",
            text_color="#2E86AB",
            cursor="hand2",
            font=ctk.CTkFont("Arial", 12)
        )
        login_label.pack(pady=10)
        login_label.bind("<Button-1>", lambda e: self.show_login_form())

        # Сообщение
        self.reg_message_label = ctk.CTkLabel(
            self.auth_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont("Arial", 11)
        )
        self.reg_message_label.pack(pady=5)

        # Кнопка закрытия
        close_btn = ctk.CTkButton(
            self.auth_frame,
            text="✕",
            command=self.hide_auth_frame,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#F0F0F0",
            text_color="#666666",
            font=ctk.CTkFont("Arial", 14)
        )
        close_btn.place(relx=0.9, rely=0.05, anchor="center")

    def login(self):
        """Обработка входа"""
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if not login or not password:
            self.error_label.configure(text="Заполните все поля")
            return

        user = self.db.get_user_by_credentials(login, password)
        if user:
            self.on_login_success(user[0], user[1])
            self.hide_auth_frame()
        else:
            self.error_label.configure(text="Неверный логин или пароль")

    def register(self):
        """Обработка регистрации"""
        login = self.reg_login_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm_password = self.reg_confirm_password_entry.get().strip()

        if not login or not password:
            self.reg_message_label.configure(text="Заполните все поля", text_color="red")
            return

        if password != confirm_password:
            self.reg_message_label.configure(text="Пароли не совпадают", text_color="red")
            return

        if self.db.check_user_exists(login):
            self.reg_message_label.configure(text="Пользователь с таким логином уже существует", text_color="red")
            return

        result = self.db.create_user(login, password)
        if result:
            # Автоматически входим после регистрации
            user = self.db.get_user_by_credentials(login, password)
            if user:
                self.on_login_success(user[0], user[1])
                self.hide_auth_frame()
                self.show_notification("Регистрация успешна!")
        else:
            self.reg_message_label.configure(text="Ошибка регистрации", text_color="red")

    def hide_auth_frame(self):
        """Скрывает фрейм авторизации"""
        if self.auth_frame:
            self.auth_frame.destroy()
            self.auth_frame = None

    def show_profile_dialog(self):
        """Показывает диалог профиля или авторизации"""
        if self.current_user_id:
            # Показываем меню для авторизованного пользователя
            self.show_user_menu()
        else:
            # Показываем форму авторизации
            self.create_auth_frame()

    def show_user_menu(self):
        """Показывает меню пользователя"""
        menu_frame = ctk.CTkFrame(
            self.window,
            width=200,
            height=120,
            corner_radius=10,
            fg_color="white",
            border_width=1,
            border_color="#E0E0E0"
        )
        menu_frame.place(relx=0.9, rely=0.1, anchor="ne")
        menu_frame.pack_propagate(False)

        user_label = ctk.CTkLabel(
            menu_frame,
            text=f"👤 {self.current_user_login}",
            font=ctk.CTkFont("Arial", 14, weight="bold"),
            text_color="#333333"
        )
        user_label.pack(pady=15)

        logout_btn = ctk.CTkButton(
            menu_frame,
            text="Выйти",
            command=lambda: [menu_frame.destroy(), self.logout()],
            width=160,
            height=35,
            fg_color="#E63946",
            hover_color="#C1121F"
        )
        logout_btn.pack(pady=5)

        close_btn = ctk.CTkButton(
            menu_frame,
            text="Закрыть",
            command=menu_frame.destroy,
            width=160,
            height=35,
            fg_color="transparent",
            hover_color="#F0F0F0",
            text_color="#666666",
            border_color="#E0E0E0",
            border_width=1
        )
        close_btn.pack(pady=5)

    def on_login_success(self, user_id, login):
        """Обработка успешного входа"""
        self.current_user_id = user_id
        self.current_user_login = login
        self.update_navbar_profile()
        self.show_notification(f"Добро пожаловать, {login}!")

    def logout(self):
        """Выход из системы"""
        self.current_user_id = None
        self.current_user_login = None
        self.update_navbar_profile()
        self.show_notification("Вы вышли из системы")

    def update_navbar_profile(self):
        """Обновляет отображение профиля в навбаре"""
        if self.current_user_id:
            self.profile_btn.configure(text=f"👤 {self.current_user_login}")
        else:
            self.profile_btn.configure(text="👤")

    # === ОСНОВНЫЕ МЕТОДЫ ПРИЛОЖЕНИЯ ===
    def load_products_data(self):
        """Загрузка данных о товарах из базы"""
        try:
            self.products = self.db.get_products()
            self.categories = self.db.get_categories()
            print(f"Загружено товаров: {len(self.products)}")

        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.products = []
            self.categories = []

        # Избранные товары
        self.favorites = set()

    def create_top_navbar(self):
        """Создание верхней навигационной панели"""
        self.nav_frame = ctk.CTkFrame(self.window, height=70, corner_radius=0, fg_color="#2E86AB")
        self.nav_frame.pack(fill="x", padx=0, pady=0)
        self.nav_frame.pack_propagate(False)

        # Левая часть навигации
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

        # Правая часть навигации (иконки)
        right_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=30, pady=20)

        # Иконка профиля
        self.profile_btn = ctk.CTkButton(
            right_frame,
            text="👤",
            font=ctk.CTkFont("Arial", 18),
            width=45,
            height=35,
            fg_color="transparent",
            hover_color="#1B5E7D",
            text_color="white",
            command=self.show_profile_dialog
        )
        self.profile_btn.pack(side="left", padx=10)

        # Остальные иконки
        icon_buttons = [
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
        self.profile_btn = ctk.CTkButton(
            right_frame,
            text="👤",
            font=ctk.CTkFont("Arial", 18),
            width=45,
            height=35,
            fg_color="transparent",
            hover_color="#1B5E7D",
            text_color="white",
            command=self.show_profile_dialog
        )
        self.profile_btn.pack(side="left", padx=10)

        icon_buttons = [
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

    def show_profile_dialog(self):
        """Показывает диалог профиля (вход/выход)"""
        if self.current_user_id:
            # Показываем меню для авторизованного пользователя
            menu = ctk.CTk()
            menu.title("Профиль")
            menu.geometry("200x150")
            menu.resizable(False, False)

            user_label = ctk.CTkLabel(menu, text=f"Пользователь:\n{self.current_user_login}",
                                      font=ctk.CTkFont("Arial", 14))
            user_label.pack(pady=20)

            logout_btn = ctk.CTkButton(menu, text="Выйти", command=lambda: [menu.destroy(), self.logout()])
            logout_btn.pack(pady=10)

            close_btn = ctk.CTkButton(menu, text="Закрыть", command=menu.destroy)
            close_btn.pack(pady=5)

            menu.mainloop()
        else:
            self.show_login_window()

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

        # Баннерная плашка
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
        """Показать популярные товары на главной в стиле Wildberries"""
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

        # Контейнер для товаров с горизонтальной прокруткой
        scroll_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            orientation="horizontal",
            height=350
        )
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Отображаем товары из базы данных
        for product in self.products:
            product_frame = self.create_wb_product_card(scroll_frame, product)
            product_frame.pack(side="left", padx=10, pady=5)

        # Добавляем кнопку "В корзину" внизу экрана
        self.add_bottom_cart_button()

    def add_bottom_cart_button(self):
        """Добавляет кнопку перехода в корзину внизу экрана"""
        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=60)
        bottom_frame.pack(fill="x", side="bottom", pady=10)
        bottom_frame.pack_propagate(False)

        # Кнопка перехода в корзину
        cart_button = ctk.CTkButton(
            bottom_frame,
            text="🛒 Перейти в корзину",
            command=self.show_cart,
            fg_color="#2E86AB",
            hover_color="#1B5E7D",
            height=45,
            font=ctk.CTkFont("Arial", 16, weight="bold")
        )
        cart_button.pack(pady=10)

        # Информация о количестве товаров в корзине (если пользователь авторизован)
        if self.current_user_id:
            cart_items = self.db.get_user_cart(self.current_user_id)
            cart_count = len(cart_items)
            if cart_count > 0:
                count_label = ctk.CTkLabel(
                    bottom_frame,
                    text=f"В вашей корзине {cart_count} товар(ов)",
                    font=ctk.CTkFont("Arial", 14),
                    text_color="#666666"
                )
                count_label.pack(pady=5)

    def create_wb_product_card(self, parent, product):
        """Создание карточки товара в стиле Wildberries"""
        (product_id, name, description, price, size, model,
         category, supplier, image_path) = product

        # Основной фрейм карточки
        card_frame = ctk.CTkFrame(
            parent,
            width=220,
            height=320,
            border_width=1,
            border_color="#E0E0E0",
            corner_radius=8
        )
        card_frame.pack_propagate(False)

        # Верхняя часть с изображением
        image_frame = ctk.CTkFrame(
            card_frame,
            height=140,
            fg_color="#F8F9FA",
            corner_radius=8
        )
        image_frame.pack(fill="x", padx=8, pady=8)
        image_frame.pack_propagate(False)

        # Кнопка избранного в правом верхнем углу
        is_favorite = product_id in self.favorites
        favorite_btn = ctk.CTkButton(
            image_frame,
            text="❤️" if is_favorite else "🤍",
            font=ctk.CTkFont("Arial", 12),
            width=28,
            height=28,
            fg_color="white",
            hover_color="#F0F0F0",
            text_color="#FF4444" if is_favorite else "#666666",
            command=lambda pid=product_id: self.toggle_favorite_simple(pid)
        )
        favorite_btn.place(relx=0.85, rely=0.2, anchor="center")

        # Заглушка изображения
        image_label = ctk.CTkLabel(
            image_frame,
            text="🛍️",
            font=ctk.CTkFont("Arial", 24),
            text_color="#6C757D"
        )
        image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Информация о товаре
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=12, pady=8)

        # Цена (крупно)
        price_label = ctk.CTkLabel(
            info_frame,
            text=f"{int(price)} ₽",
            font=ctk.CTkFont("Arial", 18, weight="bold"),
            text_color="#2E86AB"
        )
        price_label.pack(anchor="w", pady=(0, 5))

        # Название товара (обрезанное)
        short_name = name[:30] + "..." if len(name) > 30 else name
        name_label = ctk.CTkLabel(
            info_frame,
            text=short_name,
            font=ctk.CTkFont("Arial", 12),
            wraplength=180,
            justify="left",
            text_color="#333333"
        )
        name_label.pack(anchor="w", pady=(0, 5))

        # Характеристики
        if size:
            size_label = ctk.CTkLabel(
                info_frame,
                text=f"Размер: {size}",
                font=ctk.CTkFont("Arial", 10),
                text_color="#666666"
            )
            size_label.pack(anchor="w", pady=(0, 2))

        if model:
            model_label = ctk.CTkLabel(
                info_frame,
                text=f"Модель: {model}",
                font=ctk.CTkFont("Arial", 10),
                text_color="#666666"
            )
            model_label.pack(anchor="w", pady=(0, 2))

        # Бренд/поставщик
        if supplier:
            supplier_label = ctk.CTkLabel(
                info_frame,
                text=supplier,
                font=ctk.CTkFont("Arial", 10, weight="bold"),
                text_color="#333333"
            )
            supplier_label.pack(anchor="w", pady=(0, 10))

        # Кнопка добавления в корзину
        add_btn = ctk.CTkButton(
            info_frame,
            text="В корзину",
            command=lambda pid=product_id: self.add_to_cart(pid),
            fg_color="#2E86AB",
            hover_color="#1B5E7D",
            height=32,
            font=ctk.CTkFont("Arial", 12, weight="bold")
        )
        add_btn.pack(fill="x", pady=(5, 0))

        return card_frame

    def toggle_favorite_simple(self, product_id):
        """Простой метод для переключения избранного"""
        if product_id in self.favorites:
            self.favorites.remove(product_id)
        else:
            self.favorites.add(product_id)

        # Пересоздаем блок товаров для обновления состояния
        self.show_popular_products()

        # Показываем уведомление
        action = "добавлен" if product_id in self.favorites else "удален"
        self.show_notification(f"Товар {action} в избранное")

    def add_to_cart(self, product_id):
        """Добавить товар в корзину"""
        if not self.current_user_id:
            self.show_notification("Сначала войдите в систему!")
            self.show_login_window()
            return

        try:
            result = self.db.add_to_cart(self.current_user_id, product_id)
            if result:
                self.show_notification("Товар добавлен в корзину!")
            else:
                self.show_notification("Ошибка при добавлении в корзину")
        except Exception as e:
            print(f"Ошибка: {e}")

    def show_notification(self, message):
        """Показывает временное уведомление"""
        notification = ctk.CTkLabel(
            self.window,
            text=message,
            font=ctk.CTkFont("Arial", 14),
            fg_color="#2E86AB",
            text_color="white",
            corner_radius=10
        )
        notification.place(relx=0.5, rely=0.1, anchor="center")

        self.window.after(2000, notification.destroy)

    def show_catalog(self):
        """Показать полный каталог товаров"""
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Каталог товаров",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        )
        title.pack(pady=20)

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

        if not self.current_user_id:
            login_prompt = ctk.CTkLabel(
                self.main_frame,
                text="Войдите в систему, чтобы просмотреть корзину",
                font=ctk.CTkFont("Arial", 16)
            )
            login_prompt.pack(pady=50)
            return

        cart_items = self.db.get_user_cart(self.current_user_id)

        if not cart_items:
            empty_label = ctk.CTkLabel(
                self.main_frame,
                text="Корзина пуста",
                font=ctk.CTkFont("Arial", 16)
            )
            empty_label.pack(pady=50)
            return

        # Здесь будет реализация отображения корзины
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

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

    def __del__(self):
        """Закрытие соединения с базой данных при уничтожении объекта"""
        if hasattr(self, 'db'):
            self.db.get_connection().close()


if __name__ == "__main__":
    app = SportsShopApp()
    app.run()