import customtkinter as ctk
from database import Database
from product_detail import ProductDetailWindow


class CatalogWindow:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        self.db = Database('sports_shop.db')
        self.filtered_products = []
        self.all_products = []

        # Переменные для фильтров
        self.price_min = ctk.StringVar(value="0")
        self.price_max = ctk.StringVar(value="15000")
        self.selected_category = ctk.StringVar(value="Все")
        self.selected_colors = []
        self.selected_sizes = []

        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        """Создает интерфейс каталога с фильтрами"""
        # Основной контейнер БЕЗ прокрутки
        main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Левая панель - фильтры (фиксированная ширина)
        self.filters_frame = ctk.CTkFrame(main_container, width=250, height=600)
        self.filters_frame.pack(side="left", fill="y", padx=(0, 20))
        self.filters_frame.pack_propagate(False)

        # Правая панель - товары
        self.products_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        self.products_frame.pack(side="right", fill="both", expand=True)

        self.create_filters_panel()
        self.create_products_panel()

    def create_filters_panel(self):
        """Создает панель фильтров"""
        # Заголовок
        ctk.CTkLabel(
            self.filters_frame,
            text="Фильтры",
            font=ctk.CTkFont("Arial", 18, weight="bold")
        ).pack(pady=15)

        # Фильтр по цене
        self.create_price_filter()

        # Фильтр по категориям
        self.create_category_filter()

        # Фильтр по цветам
        self.create_color_filter()

        # Фильтр по размерам
        self.create_size_filter()

        # Кнопка применения фильтров внизу
        apply_button = ctk.CTkButton(
            self.filters_frame,
            text="Применить фильтры",
            command=self.apply_filters,
            fg_color="#2E86AB",
            hover_color="#1B5E7D",
            height=40,
            font=ctk.CTkFont("Arial", 14, weight="bold")
        )
        apply_button.pack(fill="x", padx=15, pady=20, side="bottom")

    def create_price_filter(self):
        """Создает фильтр по цене"""
        price_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        price_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            price_frame,
            text="Цена, ₽",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        ).pack(anchor="w")

        # Контейнер для полей ввода
        inputs_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        inputs_frame.pack(fill="x", pady=8)

        # Минимальная цена
        min_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        min_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(min_frame, text="От:", width=30).pack(side="left")
        ctk.CTkEntry(
            min_frame,
            textvariable=self.price_min,
            width=80,
            placeholder_text="0"
        ).pack(side="left", padx=5)

        # Максимальная цена
        max_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        max_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(max_frame, text="До:", width=30).pack(side="left")
        ctk.CTkEntry(
            max_frame,
            textvariable=self.price_max,
            width=80,
            placeholder_text="15000"
        ).pack(side="left", padx=5)

    def create_category_filter(self):
        """Создает фильтр по категориям"""
        category_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        category_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            category_frame,
            text="Категория",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        ).pack(anchor="w")

        # Загружаем категории из базы
        try:
            categories = self.db.get_categories()
            category_names = ["Все"] + [cat[1] for cat in categories]

            for category in category_names:
                radio = ctk.CTkRadioButton(
                    category_frame,
                    text=category,
                    variable=self.selected_category,
                    value=category,
                    font=ctk.CTkFont("Arial", 13)
                )
                radio.pack(anchor="w", pady=2)
        except Exception as e:
            print(f"Ошибка загрузки категорий: {e}")

    def create_color_filter(self):
        """Создает фильтр по цветам"""
        color_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        color_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            color_frame,
            text="Цвет",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        ).pack(anchor="w")

        # Загружаем цвета из базы
        try:
            colors = self.db.get_unique_colors()
            self.color_vars = {}

            color_container = ctk.CTkFrame(color_frame, fg_color="transparent")
            color_container.pack(fill="x", pady=5)

            for i, color_tuple in enumerate(colors):
                color = color_tuple[0]
                if color:
                    var = ctk.BooleanVar()
                    self.color_vars[color] = var

                    checkbox = ctk.CTkCheckBox(
                        color_container,
                        text=color,
                        variable=var,
                        font=ctk.CTkFont("Arial", 13)
                    )
                    checkbox.pack(anchor="w", pady=1)
        except Exception as e:
            print(f"Ошибка загрузки цветов: {e}")

    def create_size_filter(self):
        """Создает фильтр по размерам"""
        size_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            size_frame,
            text="Размер",
            font=ctk.CTkFont("Arial", 14, weight="bold")
        ).pack(anchor="w")

        # Загружаем размеры из базы
        try:
            sizes = self.db.get_unique_sizes()
            self.size_vars = {}

            size_container = ctk.CTkFrame(size_frame, fg_color="transparent")
            size_container.pack(fill="x", pady=5)

            for size_tuple in sizes:
                size = size_tuple[0]
                if size:
                    var = ctk.BooleanVar()
                    self.size_vars[size] = var

                    checkbox = ctk.CTkCheckBox(
                        size_container,
                        text=size,
                        variable=var,
                        font=ctk.CTkFont("Arial", 13)
                    )
                    checkbox.pack(anchor="w", pady=1)
        except Exception as e:
            print(f"Ошибка загрузки размеров: {e}")

    def create_products_panel(self):
        """Создает панель товаров"""
        # Заголовок с количеством товаров
        title_frame = ctk.CTkFrame(self.products_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            title_frame,
            text="Каталог товаров",
            font=ctk.CTkFont("Arial", 24, weight="bold")
        ).pack(side="left")

        self.count_label = ctk.CTkLabel(
            title_frame,
            text="Найдено: 0",
            font=ctk.CTkFont("Arial", 14),
            text_color="#666666"
        )
        self.count_label.pack(side="right")

        # Контейнер для товаров С прокруткой
        self.products_scrollable = ctk.CTkScrollableFrame(
            self.products_frame,
            fg_color="transparent",
            scrollbar_button_color="#2E86AB"
        )
        self.products_scrollable.pack(fill="both", expand=True)

    def load_products(self):
        """Загружает товары из базы данных"""
        try:
            print("=== НАЧАЛО ЗАГРУЗКИ ТОВАРОВ ===")
            self.all_products = self.db.get_products_grouped()
            print(f"Получено товаров из базы: {len(self.all_products)}")

            if self.all_products:
                print("Первый товар для примера:")
                print(self.all_products[0])

            self.apply_filters()

        except Exception as e:
            print(f"Ошибка загрузки товаров: {e}")
            import traceback
            traceback.print_exc()
            self.show_error("Ошибка загрузки каталога")

    def apply_filters(self):
        """Применяет фильтры к товарам"""
        try:
            if not self.all_products:
                print("Нет товаров для фильтрации!")
                self.filtered_products = []
                self.display_products()
                return

            self.update_selected_colors()
            self.update_selected_sizes()

            filtered = []

            for product in self.all_products:
                try:
                    # Распаковываем с учетом product_id как первого элемента
                    if len(product) == 10:  # Новый формат с product_id
                        product_id, name, description, min_price, max_price, colors, sizes, category, variants_count, avg_rating = product
                    else:  # Старый формат без product_id
                        name, description, min_price, max_price, colors, sizes, category, variants_count, avg_rating = product
                        product_id = None

                    # Фильтр по цене
                    try:
                        price_min_val = float(self.price_min.get() or 0)
                        price_max_val = float(self.price_max.get() or 15000)

                        # Проверяем цену
                        if min_price is None or min_price < price_min_val:
                            continue
                        if max_price and max_price > price_max_val:
                            continue
                    except (ValueError, TypeError) as e:
                        print(f"Ошибка фильтрации по цене: {e}")
                        continue

                    # Фильтр по категории
                    if self.selected_category.get() != "Все" and category != self.selected_category.get():
                        continue

                    # Фильтр по цветам
                    if self.selected_colors:
                        product_colors = colors.split(',') if colors else []
                        if not any(color in product_colors for color in self.selected_colors):
                            continue

                    # Фильтр по размерам
                    if self.selected_sizes:
                        product_sizes = sizes.split(',') if sizes else []
                        if not any(size in product_sizes for size in self.selected_sizes):
                            continue

                    filtered.append(product)

                except Exception as e:
                    print(f"Ошибка обработки товара {product}: {e}")
                    continue

            self.filtered_products = filtered
            print(f"После фильтрации осталось товаров: {len(self.filtered_products)}")
            self.display_products()

        except Exception as e:
            print(f"Ошибка применения фильтров: {e}")
            import traceback
            traceback.print_exc()

    def display_products(self):
        """Отображает отфильтрованные товары"""
        # Очищаем контейнер
        for widget in self.products_scrollable.winfo_children():
            widget.destroy()

        # Обновляем счетчик
        self.count_label.configure(text=f"Найдено: {len(self.filtered_products)}")

        if not self.filtered_products:
            self.show_error("Товары не найдены")
            return

        # Отображаем товары в сетке 3 колонки
        row_frame = None
        for i, product in enumerate(self.filtered_products):
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(self.products_scrollable, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)

            product_card = self.create_product_card(row_frame, product)
            product_card.pack(side="left", padx=5, expand=True)

    def create_product_card(self, parent, product):
        """Создает карточку товара"""
        try:
            # Распаковываем с учетом product_id как первого элемента
            if len(product) == 10:  # Новый формат с product_id
                product_id, name, description, min_price, max_price, colors, sizes, category, variants_count, avg_rating = product
            else:  # Старый формат без product_id
                name, description, min_price, max_price, colors, sizes, category, variants_count, avg_rating = product
                product_id = None

            print(f"Создание карточки для: {name}, ID: {product_id}")

            card = ctk.CTkFrame(
                parent,
                width=250,
                height=380,
                border_width=1,
                border_color="#E0E0E0",
                corner_radius=12
            )
            card.pack_propagate(False)

            # Изображение
            img_frame = ctk.CTkFrame(card, height=150, fg_color="#F8F9FA", corner_radius=8)
            img_frame.pack(fill="x", padx=10, pady=10)
            img_frame.pack_propagate(False)

            # Эмодзи для категории
            emoji_map = {'Обувь': '👟', 'Одежда': '👕', 'Аксессуары': '🎒'}
            emoji = emoji_map.get(category, '🛍️')

            ctk.CTkLabel(
                img_frame,
                text=emoji,
                font=ctk.CTkFont("Arial", 28),
                text_color="#6C757D"
            ).place(relx=0.5, rely=0.5, anchor="center")

            # Кнопка избранного
            is_fav = False
            if self.user_id and product_id:
                is_fav = self.db.is_product_in_favorites(self.user_id, product_id)

            fav_button = ctk.CTkButton(
                img_frame,
                text="❤️" if is_fav else "🤍",
                width=30,
                height=30,
                fg_color="white",
                hover_color="#F0F0F0",
                text_color="#FF4444" if is_fav else "#666666",
                font=ctk.CTkFont("Arial", 12),
                command=lambda pid=product_id, pname=name: self.toggle_favorite(pid, pname)
            )
            fav_button.place(relx=0.85, rely=0.2, anchor="center")

            # Информация
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="both", expand=True, padx=12, pady=8)

            # Категория
            ctk.CTkLabel(
                info_frame,
                text=category if category else "Без категории",
                font=ctk.CTkFont("Arial", 11),
                text_color="#666666"
            ).pack(anchor="w")

            # Название товара (кликабельное)
            name_label = ctk.CTkLabel(
                info_frame,
                text=name,
                font=ctk.CTkFont("Arial", 14, weight="bold"),
                text_color="#333333",
                cursor="hand2",
                wraplength=220
            )
            name_label.pack(anchor="w", pady=(3, 0))
            name_label.bind("<Button-1>", lambda e, pname=name: self.show_product_detail(pname))

            # Характеристики
            if colors and colors != 'None':
                ctk.CTkLabel(
                    info_frame,
                    text=f"Цвет: {colors}",
                    font=ctk.CTkFont("Arial", 11),
                    text_color="#666666"
                ).pack(anchor="w", pady=1)

            if sizes and sizes != 'None':
                ctk.CTkLabel(
                    info_frame,
                    text=f"Размер: {sizes}",
                    font=ctk.CTkFont("Arial", 11),
                    text_color="#666666"
                ).pack(anchor="w", pady=1)

            # Цена и кнопка
            price_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            price_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(
                price_frame,
                text=f"{min_price} ₽",
                font=ctk.CTkFont("Arial", 16, weight="bold"),
                text_color="#2E86AB"
            ).pack(side="left")

            # Кнопка "В корзину"
            ctk.CTkButton(
                price_frame,
                text="В корзину",
                command=lambda pid=product_id, pname=name: self.add_to_cart(pid, pname),
                width=80,
                height=28,
                fg_color="#2E86AB",
                hover_color="#1B5E7D",
                font=ctk.CTkFont("Arial", 12, weight="bold")
            ).pack(side="right")

            return card

        except Exception as e:
            print(f"Ошибка создания карточки товара: {e}")
            # Возвращаем пустую карточку в случае ошибки
            error_card = ctk.CTkFrame(parent, width=250, height=380)
            ctk.CTkLabel(error_card, text="Ошибка загрузки").pack(expand=True)
            return error_card

    def update_selected_colors(self):
        """Обновляет выбранные цвета"""
        self.selected_colors = [color for color, var in self.color_vars.items() if var.get()]

    def update_selected_sizes(self):
        """Обновляет выбранные размеры"""
        self.selected_sizes = [size for size, var in self.size_vars.items() if var.get()]

    def show_product_detail(self, product_name):
        """Показывает детальную информацию о товаре"""
        # Очищаем основную область и показываем детали товара
        for widget in self.parent.winfo_children():
            widget.destroy()

        ProductDetailWindow(self.parent, product_name, self.user_id, self.show_catalog)

    def show_catalog(self):
        """Возвращает к каталогу"""
        # Очищаем основную область и показываем каталог
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.__init__(self.parent, self.user_id)

    def show_error(self, message):
        """Показывает сообщение об ошибке"""
        error_frame = ctk.CTkFrame(self.products_scrollable, fg_color="transparent")
        error_frame.pack(expand=True, pady=50)

        ctk.CTkLabel(
            error_frame,
            text=message,
            font=ctk.CTkFont("Arial", 16),
            text_color="red"
        ).pack()

    def get_product_id_by_name(self, product_name):
        """Получает ID товара по названию"""
        try:
            query = "SELECT product_id FROM products WHERE name = ? LIMIT 1"
            result = self.db.execute_query(query, (product_name,))
            return result[0][0] if result else None
        except Exception as e:
            print(f"Ошибка получения ID товара: {e}")
            return None

    def toggle_favorite(self, product_id, product_name):
        """Добавление/удаление из избранного"""
        if not self.user_id:
            self.show_notification("Сначала войдите в систему!")
            return

        if product_id is None:
            self.show_notification("Ошибка: товар не найден")
            return

        if self.db.is_product_in_favorites(self.user_id, product_id):
            # Удаляем из избранного
            if self.db.remove_from_favorites(self.user_id, product_id):
                self.show_notification("Товар удален из избранного")
                # Обновляем отображение
                self.apply_filters()
        else:
            # Добавляем в избранное
            if self.db.add_to_favorites(self.user_id, product_id):
                self.show_notification("Товар добавлен в избранное")
                # Обновляем отображение
                self.apply_filters()

    def add_to_cart(self, product_id, product_name):
        """Добавление в корзину"""
        if not self.user_id:
            self.show_notification("Сначала войдите в систему!")
            return

        if product_id is None:
            self.show_notification("Ошибка: товар не найден")
            return

        if self.db.add_to_cart(self.user_id, product_id):
            self.show_notification(f"Товар '{product_name}' добавлен в корзину!")
        else:
            self.show_notification("Ошибка добавления в корзину")

    def show_notification(self, message):
        """Показывает уведомление"""
        # Создаем временное уведомление
        notification = ctk.CTkLabel(
            self.parent,
            text=message,
            font=ctk.CTkFont("Arial", 14),
            fg_color="#2E86AB",
            text_color="white",
            corner_radius=10
        )
        notification.place(relx=0.5, rely=0.1, anchor="center")
        self.parent.after(2000, notification.destroy)
