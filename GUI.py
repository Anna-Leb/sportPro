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
        self.current_user_id = 1  # Для демонстрации, в реальном приложении - из системы авторизации

        # Загрузка данных
        self.load_products_data()

        # Создаем верхнюю панель навигации
        self.create_top_navbar()

        # Основная область контента
        self.create_main_content()

    def load_products_data(self):
        """Загрузка данных о товарах из базы"""
        try:
            self.products = self.db.get_products()
            self.categories = self.db.get_categories()

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
        """Создание карточки товара"""
        (product_id, name, price, description, size, model,
         category, supplier, image_path) = product

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

        # Верхняя часть с изображением
        image_frame = ctk.CTkFrame(
            card_frame,
            height=200,
            fg_color="#F8F9FA",
            corner_radius=12
        )
        image_frame.pack(fill="x", padx=10, pady=10)
        image_frame.pack_propagate(False)

        # Загрузка изображения (если есть)
        if image_path and os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                image_label = ctk.CTkLabel(
                    image_frame,
                    image=photo,
                    text=""
                )
                image_label.image = photo  # Сохраняем ссылку
                image_label.place(relx=0.5, rely=0.5, anchor="center")

            except Exception as e:
                # Если не удалось загрузить изображение, показываем заглушку
                self._create_image_placeholder(image_frame)
        else:
            self._create_image_placeholder(image_frame)

        # ... остальной код метода без изменений ...

        return card_frame

    def _create_image_placeholder(self, parent):
        """Создает заглушку для изображения"""
        placeholder = ctk.CTkLabel(
            parent,
            text="🛍️",
            font=ctk.CTkFont("Arial", 48),
            text_color="#6C757D"
        )
        placeholder.place(relx=0.5, rely=0.5, anchor="center")

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

        # Загружаем данные корзины из БД
        cart_items = self.db.get_user_cart(self.current_user_id)

        if not cart_items:
            empty_label = ctk.CTkLabel(
                self.main_frame,
                text="Корзина пуста",
                font=ctk.CTkFont("Arial", 16),
                text_color="#666666"
            )
            empty_label.pack(pady=50)
            return

        # Контейнер для товаров в корзине
        cart_container = ctk.CTkScrollableFrame(self.main_frame)
        cart_container.pack(fill="both", expand=True, padx=40, pady=20)

        total_amount = 0

        for item in cart_items:
            (cart_id, product_id, name, price, quantity, total, image_path) = item
            total_amount += total

            item_frame = ctk.CTkFrame(cart_container)
            item_frame.pack(fill="x", padx=10, pady=5)

            # Информация о товаре
            info_text = f"{name}\nЦена: ${price} × {quantity} = ${total}"
            info_label = ctk.CTkLabel(item_frame, text=info_text, justify="left")
            info_label.pack(side="left", padx=10, pady=10)

            # Кнопка удаления
            remove_btn = ctk.CTkButton(
                item_frame,
                text="❌",
                width=30,
                height=30,
                command=lambda cid=cart_id: self.remove_from_cart(cid)
            )
            remove_btn.pack(side="right", padx=10, pady=10)

        # Общая сумма
        total_frame = ctk.CTkFrame(self.main_frame)
        total_frame.pack(fill="x", padx=40, pady=20)

        total_label = ctk.CTkLabel(
            total_frame,
            text=f"Общая сумма: ${total_amount:.2f}",
            font=ctk.CTkFont("Arial", 20, weight="bold")
        )
        total_label.pack(side="left")

        # Кнопка оформления заказа
        order_btn = ctk.CTkButton(
            total_frame,
            text="Оформить заказ",
            fg_color="#2E86AB",
            hover_color="#1B5E7D",
            command=self.create_order
        )
        order_btn.pack(side="right", padx=10)

    def remove_from_cart(self, cart_item_id):
        """Удаляет товар из корзины"""
        try:
            self.db.remove_from_cart(cart_item_id)
            self.show_cart()  # Обновляем отображение
            self.show_notification("Товар удален из корзины")
        except Exception as e:
            print(f"Ошибка при удалении из корзины: {e}")

    def create_order(self):
        """Создает заказ из корзины"""
        try:
            cart_items = self.db.get_user_cart(self.current_user_id)
            if not cart_items:
                self.show_notification("Корзина пуста!")
                return

            total_amount = sum(item[5] for item in cart_items)  # item[5] - это total

            # Создаем заказ
            order_id = self.db.create_order(self.current_user_id, total_amount)

            if order_id:
                self.show_notification(f"Заказ #{order_id} оформлен успешно!")
                self.show_cart()  # Обновляем корзину (она должна стать пустой)
            else:
                self.show_notification("Ошибка при создании заказа")

        except Exception as e:
            print(f"Ошибка при создании заказа: {e}")
            self.show_notification("Ошибка при создании заказа")

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
            result = self.db.add_to_cart(self.current_user_id, product_id)
            if result:
                print(f"Товар {product_id} добавлен в корзину")
                # Можно показать уведомление
                self.show_notification("Товар добавлен в корзину!")
            else:
                print("Ошибка при добавлении в корзину")
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

        # Убираем уведомление через 2 секунды
        self.window.after(2000, notification.destroy)

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

    def __del__(self):
        """Закрытие соединения с базой данных при уничтожении объекта"""
        if hasattr(self, 'conn'):
            self.conn.close()



app = SportsShopApp()
app.run()