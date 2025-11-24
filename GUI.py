import customtkinter as ctk
from database import Database

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SportsShopApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("SportShop - Магазин спортивных товаров")
        self.window.geometry("1400x900")

        self.db = Database('sports_shop.db')
        self.current_user_id = None
        self.current_user_login = None
        self.products = []
        # Убираем локальное хранение избранного, будем работать с БД
        # self.favorites = set()

        self.load_products_data()
        self.create_navbar()
        self.create_main_content()

        self.show_home()

    def load_products_data(self):
        """Загрузка товаров из базы"""
        try:
            self.products = self.db.get_products()
            print(f"Загружено товаров: {len(self.products)}")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.products = []

    def create_navbar(self):
        """Создание навигационной панели"""
        nav_frame = ctk.CTkFrame(self.window, height=70, fg_color="#2E86AB")
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        # Левая часть
        left_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=20)

        ctk.CTkLabel(
            left_frame, text="SPORTSHOP",
            font=ctk.CTkFont("Arial", 22, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=(0, 40))

        # Кнопки навигации
        for text, command in [
            ("Главная", self.show_home),
            ("Каталог", self.show_catalog),
            ("Корзина", self.show_cart),
            ("Избранное", self.show_favorites),
            ("Адреса", self.show_addresses)
        ]:
            btn = ctk.CTkButton(
                left_frame, text=text,
                font=ctk.CTkFont("Arial", 15),
                fg_color="transparent", hover_color="#1B5E7D",
                text_color="white", width=90, height=30,
                command=command
            )
            btn.pack(side="left", padx=10)

        # Правая часть с иконками
        right_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=20)

        # Кнопка профиля
        self.profile_btn = ctk.CTkButton(
            right_frame, text="👤 Войти",
            font=ctk.CTkFont("Arial", 14),
            fg_color="transparent", hover_color="#1B5E7D",
            text_color="white", width=100, height=35,
            command=self.show_auth
        )
        self.profile_btn.pack(side="left", padx=10)

        # Остальные иконки
        for icon, command in [
            ("❤️ Избранное", self.show_favorites),
            ("🛒 Корзина", self.show_cart)
        ]:
            btn = ctk.CTkButton(
                right_frame, text=icon,
                font=ctk.CTkFont("Arial", 14),
                fg_color="transparent", hover_color="#1B5E7D",
                text_color="white", width=120, height=35,
                command=command
            )
            btn.pack(side="left", padx=10)

    def create_main_content(self):
        """Создание основной области"""
        self.main_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color="transparent",
            scrollbar_button_color="#2E86AB"
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def clear_main_frame(self):
        """Очистка основной области"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Главная страница"""
        self.clear_main_frame()

        # Баннер
        banner = ctk.CTkFrame(
            self.main_frame, height=300,
            fg_color="#E63946", corner_radius=0
        )
        banner.pack(fill="x", pady=(0, 30))
        banner.pack_propagate(False)

        content = ctk.CTkFrame(banner, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            content, text="Добро пожаловать в SportShop!",
            font=ctk.CTkFont("Arial", 32, weight="bold"),
            text_color="white"
        ).pack(pady=10)

        ctk.CTkLabel(
            content, text="СКИДКИ ДО 50% НА СПОРТИВНЫЕ ТОВАРЫ",
            font=ctk.CTkFont("Arial", 24, weight="bold"),
            text_color="white"
        ).pack(pady=5)

        # Товары
        self.show_products()

    def show_products(self):
        """Показ товаров"""
        if not self.products:
            ctk.CTkLabel(
                self.main_frame, text="Товары не найдены",
                font=ctk.CTkFont("Arial", 16), text_color="red"
            ).pack(pady=50)
            return

        # Заголовок
        ctk.CTkLabel(
            self.main_frame, text="Популярные товары",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        ).pack(pady=20)

        # Сетка товаров
        products_grid = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        products_grid.pack(fill="both", expand=True, padx=40, pady=20)

        # Создаем 4 колонки
        row, col = 0, 0
        for i, product in enumerate(self.products):
            if i % 4 == 0:
                row_frame = ctk.CTkFrame(products_grid, fg_color="transparent")
                row_frame.pack(fill="x", pady=10)
                col = 0

            product_card = self.create_product_card(row_frame, product)
            product_card.pack(side="left", padx=10)
            col += 1

    def create_product_card(self, parent, product):
        """Создание карточки товара"""
        (product_id, name, description, price, size, model,
         category, supplier, image_path) = product

        card = ctk.CTkFrame(
            parent, width=300, height=400,
            border_width=1, border_color="#E0E0E0", corner_radius=12
        )
        card.pack_propagate(False)

        # Изображение
        img_frame = ctk.CTkFrame(card, height=180, fg_color="#F8F9FA", corner_radius=8)
        img_frame.pack(fill="x", padx=10, pady=10)
        img_frame.pack_propagate(False)

        # Проверяем, в избранном ли товар
        is_fav = False
        if self.current_user_id:
            is_fav = self.db.is_product_in_favorites(self.current_user_id, product_id)

        # Кнопка избранного
        fav_btn = ctk.CTkButton(
            img_frame, text="❤️" if is_fav else "🤍",
            font=ctk.CTkFont("Arial", 12), width=30, height=30,
            fg_color="white", hover_color="#F0F0F0",
            text_color="#FF4444" if is_fav else "#666666",
            command=lambda pid=product_id: self.toggle_favorite(pid)
        )
        fav_btn.place(relx=0.9, rely=0.2, anchor="center")

        ctk.CTkLabel(
            img_frame, text="🛍️", font=ctk.CTkFont("Arial", 36),
            text_color="#6C757D"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Информация
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Цена
        ctk.CTkLabel(
            info_frame, text=f"{price} ₽",
            font=ctk.CTkFont("Arial", 20, weight="bold"),
            text_color="#2E86AB"
        ).pack(anchor="w", pady=(0, 5))

        # Название
        short_name = name[:35] + "..." if len(name) > 35 else name
        ctk.CTkLabel(
            info_frame, text=short_name,
            font=ctk.CTkFont("Arial", 14), wraplength=250,
            justify="left", text_color="#333333"
        ).pack(anchor="w", pady=(0, 8))

        # Характеристики
        if size:
            ctk.CTkLabel(
                info_frame, text=f"Размер: {size}",
                font=ctk.CTkFont("Arial", 12), text_color="#666666"
            ).pack(anchor="w", pady=2)

        if model:
            ctk.CTkLabel(
                info_frame, text=f"Модель: {model}",
                font=ctk.CTkFont("Arial", 12), text_color="#666666"
            ).pack(anchor="w", pady=2)

        # Кнопка "В корзину"
        ctk.CTkButton(
            info_frame, text="В корзину",
            command=lambda pid=product_id: self.add_to_cart(pid),
            fg_color="#2E86AB", hover_color="#1B5E7D",
            height=35, font=ctk.CTkFont("Arial", 14, weight="bold")
        ).pack(fill="x", pady=(15, 0))

        return card

    def toggle_favorite(self, product_id):
        """Добавление/удаление из избранного"""
        if not self.current_user_id:
            self.show_notification("Сначала войдите в систему!")
            self.show_auth()
            return

        if self.db.is_product_in_favorites(self.current_user_id, product_id):
            # Удаляем из избранного
            if self.db.remove_from_favorites(self.current_user_id, product_id):
                self.show_notification("Товар удален из избранного")
        else:
            # Добавляем в избранное
            if self.db.add_to_favorites(self.current_user_id, product_id):
                self.show_notification("Товар добавлен в избранное")

        # Обновляем отображение
        self.show_home()

    def add_to_cart(self, product_id):
        """Добавление в корзину"""
        if not self.current_user_id:
            self.show_notification("Сначала войдите в систему!")
            self.show_auth()
            return

        if self.db.add_to_cart(self.current_user_id, product_id):
            self.show_notification("Товар добавлен в корзину!")
        else:
            self.show_notification("Ошибка!")

    def show_favorites(self):
        """Показ избранных товаров"""
        self.clear_main_frame()

        if not self.current_user_id:
            ctk.CTkLabel(
                self.main_frame, text="Войдите в систему, чтобы просмотреть избранное",
                font=ctk.CTkFont("Arial", 16), text_color="red"
            ).pack(pady=50)
            return

        ctk.CTkLabel(
            self.main_frame, text="Избранное",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        ).pack(pady=20)

        favorites = self.db.get_user_favorites(self.current_user_id)

        if not favorites:
            ctk.CTkLabel(
                self.main_frame, text="В избранном пока ничего нет",
                font=ctk.CTkFont("Arial", 16), text_color="#666666"
            ).pack(pady=50)
            return

        # Сетка избранных товаров
        favorites_grid = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        favorites_grid.pack(fill="both", expand=True, padx=40, pady=20)

        # Создаем 4 колонки
        for i, fav in enumerate(favorites):
            if i % 4 == 0:
                row_frame = ctk.CTkFrame(favorites_grid, fg_color="transparent")
                row_frame.pack(fill="x", pady=10)

            # Создаем карточку товара для избранного
            product_data = self.db.get_product_by_id(fav[1])  # fav[1] - product_id
            if product_data:
                product_card = self.create_favorite_card(row_frame, fav, product_data)
                product_card.pack(side="left", padx=10)

    def create_favorite_card(self, parent, fav_item, product_data):
        """Создание карточки для избранного"""
        cart_id, product_id, name, description, price, size, model, quantity, total, image_path = fav_item

        card = ctk.CTkFrame(
            parent, width=300, height=400,
            border_width=1, border_color="#E0E0E0", corner_radius=12
        )
        card.pack_propagate(False)

        # Изображение
        img_frame = ctk.CTkFrame(card, height=180, fg_color="#F8F9FA", corner_radius=8)
        img_frame.pack(fill="x", padx=10, pady=10)
        img_frame.pack_propagate(False)

        ctk.CTkLabel(
            img_frame, text="🛍️", font=ctk.CTkFont("Arial", 36),
            text_color="#6C757D"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Кнопка удаления из избранного
        remove_btn = ctk.CTkButton(
            img_frame, text="❌",
            font=ctk.CTkFont("Arial", 12), width=30, height=30,
            fg_color="white", hover_color="#F0F0F0",
            text_color="#FF4444",
            command=lambda pid=product_id: self.remove_from_favorites(pid)
        )
        remove_btn.place(relx=0.9, rely=0.2, anchor="center")

        # Информация
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Цена
        ctk.CTkLabel(
            info_frame, text=f"{price} ₽",
            font=ctk.CTkFont("Arial", 20, weight="bold"),
            text_color="#2E86AB"
        ).pack(anchor="w", pady=(0, 5))

        # Название
        short_name = name[:35] + "..." if len(name) > 35 else name
        ctk.CTkLabel(
            info_frame, text=short_name,
            font=ctk.CTkFont("Arial", 14), wraplength=250,
            justify="left", text_color="#333333"
        ).pack(anchor="w", pady=(0, 8))

        # Кнопка "В корзину"
        ctk.CTkButton(
            info_frame, text="В корзину",
            command=lambda pid=product_id: self.add_to_cart(pid),
            fg_color="#2E86AB", hover_color="#1B5E7D",
            height=35, font=ctk.CTkFont("Arial", 14, weight="bold")
        ).pack(fill="x", pady=(15, 0))

        return card

    def remove_from_favorites(self, product_id):
        """Удаление из избранного"""
        if self.db.remove_from_favorites(self.current_user_id, product_id):
            self.show_notification("Товар удален из избранного")
            self.show_favorites()  # Обновляем отображение

    def show_cart(self):
        """Показ корзины"""
        self.clear_main_frame()

        if not self.current_user_id:
            ctk.CTkLabel(
                self.main_frame, text="Войдите в систему, чтобы просмотреть корзину",
                font=ctk.CTkFont("Arial", 16), text_color="red"
            ).pack(pady=50)
            return

        ctk.CTkLabel(
            self.main_frame, text="Корзина",
            font=ctk.CTkFont("Arial", 28, weight="bold")
        ).pack(pady=20)

        cart_items = self.db.get_user_cart(self.current_user_id)

        if not cart_items:
            ctk.CTkLabel(
                self.main_frame, text="Корзина пуста",
                font=ctk.CTkFont("Arial", 16), text_color="#666666"
            ).pack(pady=50)
            return

        # Отображение товаров в корзине
        total_amount = 0
        for item in cart_items:
            cart_id, product_id, name, price, quantity, total, image_path = item
            total_amount += total

            item_frame = ctk.CTkFrame(self.main_frame, height=120)
            item_frame.pack(fill="x", padx=40, pady=5)
            item_frame.pack_propagate(False)

            # Информация о товаре
            info_text = f"{name}\nЦена: {price} ₽ × {quantity} = {total} ₽"
            ctk.CTkLabel(
                item_frame, text=info_text,
                font=ctk.CTkFont("Arial", 14),
                justify="left"
            ).pack(side="left", padx=20, pady=20)

            # Кнопка удаления
            ctk.CTkButton(
                item_frame, text="❌ Удалить",
                command=lambda cid=cart_id: self.remove_from_cart(cid),
                fg_color="#E63946", hover_color="#C1121F",
                width=100
            ).pack(side="right", padx=20, pady=20)

        # Общая сумма и кнопка оформления заказа
        total_frame = ctk.CTkFrame(self.main_frame)
        total_frame.pack(fill="x", padx=40, pady=20)

        ctk.CTkLabel(
            total_frame, text=f"Общая сумма: {total_amount} ₽",
            font=ctk.CTkFont("Arial", 20, weight="bold")
        ).pack(side="left", padx=20, pady=10)

        ctk.CTkButton(
            total_frame, text="Оформить заказ",
            command=lambda: self.create_order(cart_items),
            fg_color="#2E86AB", hover_color="#1B5E7D",
            font=ctk.CTkFont("Arial", 16, weight="bold"),
            height=40
        ).pack(side="right", padx=20, pady=10)

    def remove_from_cart(self, cart_id):
        """Удаление из корзины"""
        if self.db.remove_from_cart(cart_id):
            self.show_notification("Товар удален из корзины")
            self.show_cart()  # Обновляем отображение

    def create_order(self, cart_items):
        """Создание заказа"""
        order_id = self.db.create_order(self.current_user_id, cart_items)
        if order_id:
            self.show_notification(f"Заказ #{order_id} успешно оформлен!")
            self.show_cart()  # Обновляем корзину

    def show_auth(self):
        """Показ авторизации"""
        auth_window = ctk.CTkToplevel(self.window)
        auth_window.title("Вход / Регистрация")
        auth_window.geometry("400x500")
        auth_window.resizable(False, False)
        auth_window.transient(self.window)  # Делаем окно модальным
        auth_window.grab_set()  # Блокируем главное окно
        auth_window.focus_set()  # Устанавливаем фокус

        # Центрируем окно
        auth_window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - auth_window.winfo_width()) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - auth_window.winfo_height()) // 2
        auth_window.geometry(f"+{x}+{y}")

        # Вкладки
        tabview = ctk.CTkTabview(auth_window)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)

        tabview.add("Вход")
        tabview.add("Регистрация")

        # ВКЛАДКА ВХОДА
        login_frame = tabview.tab("Вход")

        ctk.CTkLabel(
            login_frame, text="Вход в аккаунт",
            font=ctk.CTkFont("Arial", 20, weight="bold")
        ).pack(pady=20)

        login_entry = ctk.CTkEntry(login_frame, placeholder_text="Логин", width=300, height=45)
        login_entry.pack(pady=10)
        login_entry.focus()  # Фокус на поле ввода

        password_entry = ctk.CTkEntry(login_frame, placeholder_text="Пароль", show="*", width=300, height=45)
        password_entry.pack(pady=10)

        login_msg = ctk.CTkLabel(login_frame, text="", text_color="red")
        login_msg.pack(pady=5)

        def try_login():
            login = login_entry.get().strip()
            password = password_entry.get().strip()

            if not login or not password:
                login_msg.configure(text="Заполните все поля")
                return

            user = self.db.get_user_by_credentials(login, password)
            if user:
                self.current_user_id = user[0]
                self.current_user_login = user[1]
                self.profile_btn.configure(text=f"👤 {user[1]}")
                auth_window.destroy()
                self.show_notification(f"Добро пожаловать, {user[1]}!")
            else:
                login_msg.configure(text="Неверный логин или пароль")

        # Обработка нажатия Enter
        def on_enter(event):
            try_login()

        login_entry.bind('<Return>', on_enter)
        password_entry.bind('<Return>', on_enter)

        ctk.CTkButton(
            login_frame, text="Войти", command=try_login,
            width=300, height=45, fg_color="#2E86AB", hover_color="#1B5E7D"
        ).pack(pady=20)

        # ВКЛАДКА РЕГИСТРАЦИИ
        reg_frame = tabview.tab("Регистрация")

        ctk.CTkLabel(
            reg_frame, text="Регистрация",
            font=ctk.CTkFont("Arial", 20, weight="bold")
        ).pack(pady=20)

        reg_login = ctk.CTkEntry(reg_frame, placeholder_text="Логин", width=300, height=45)
        reg_login.pack(pady=8)

        reg_password = ctk.CTkEntry(reg_frame, placeholder_text="Пароль", show="*", width=300, height=45)
        reg_password.pack(pady=8)

        reg_confirm = ctk.CTkEntry(reg_frame, placeholder_text="Подтвердите пароль", show="*", width=300, height=45)
        reg_confirm.pack(pady=8)

        reg_msg = ctk.CTkLabel(reg_frame, text="", text_color="red")
        reg_msg.pack(pady=5)

        def try_register():
            login = reg_login.get().strip()
            password = reg_password.get().strip()
            confirm = reg_confirm.get().strip()

            if not login or not password:
                reg_msg.configure(text="Заполните все поля")
                return

            if password != confirm:
                reg_msg.configure(text="Пароли не совпадают")
                return

            if self.db.check_user_exists(login):
                reg_msg.configure(text="Логин уже занят")
                return

            if self.db.create_user(login, password):
                # Автоматический вход после регистрации
                user = self.db.get_user_by_credentials(login, password)
                if user:
                    self.current_user_id = user[0]
                    self.current_user_login = user[1]
                    self.profile_btn.configure(text=f"👤 {user[1]}")
                    auth_window.destroy()
                    self.show_notification("Регистрация успешна!")
            else:
                reg_msg.configure(text="Ошибка регистрации")

        ctk.CTkButton(
            reg_frame, text="Зарегистрироваться", command=try_register,
            width=300, height=45, fg_color="#2E86AB", hover_color="#1B5E7D"
        ).pack(pady=20)

        # Обработка закрытия окна
        def on_closing():
            auth_window.destroy()

        auth_window.protocol("WM_DELETE_WINDOW", on_closing)

    def show_notification(self, message):
        notification = ctk.CTkLabel(
            self.window, text=message,
            font=ctk.CTkFont("Arial", 14),
            fg_color="#2E86AB", text_color="white",
            corner_radius=10
        )
        notification.place(relx=0.5, rely=0.1, anchor="center")
        self.window.after(2000, notification.destroy)

    def show_catalog(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Каталог", font=ctk.CTkFont("Arial", 28, weight="bold")).pack(pady=50)

    def show_addresses(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.main_frame, text="Адреса магазинов", font=ctk.CTkFont("Arial", 28, weight="bold")).pack(
            pady=50)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = SportsShopApp()
    app.run()