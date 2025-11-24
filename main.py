import sqlite3
import customtkinter as ctk

class SportsShopApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Интернет-магазин спортивных товаров")
        self.window.geometry("800x600")

        # Создаем вкладки
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Добавляем вкладки
        self.tabview.add("Товары")
        self.tabview.add("Корзина")
        self.tabview.add("Заказы")
        self.tabview.add("Пользователи")

        self.setup_products_tab()
        self.setup_cart_tab()

    def setup_products_tab(self):
        """Вкладка с товарами"""
        tab = self.tabview.tab("Товары")

        # Заголовок
        title = ctk.CTkLabel(tab, text="Каталог товаров", font=("Arial", 20))
        title.pack(pady=10)

        # Фрейм для товаров
        self.products_frame = ctk.CTkScrollableFrame(tab)
        self.products_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_products()

    def load_products(self):
        """Загрузка товаров из базы"""
        conn = sqlite3.connect('sports_shop.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT product_id, name, price, description 
            FROM products
        ''')

        products = cursor.fetchall()

        for product in products:
            product_id, name, price, description = product

            product_frame = ctk.CTkFrame(self.products_frame)
            product_frame.pack(fill="x", padx=5, pady=5)

            # Информация о товаре
            info_text = f"{name}\nЦена: ${price}\n{description}"
            label = ctk.CTkLabel(product_frame, text=info_text, justify="left")
            label.pack(side="left", padx=10, pady=10)

            # Кнопка добавления в корзину
            add_btn = ctk.CTkButton(
                product_frame,
                text="В корзину",
                command=lambda pid=product_id: self.add_to_cart(pid)
            )
            add_btn.pack(side="right", padx=10, pady=10)

        conn.close()

    def add_to_cart(self, product_id):
        """Добавление товара в корзину"""
        print(f"Товар {product_id} добавлен в корзину")
        # Здесь код для добавления в базу данных

    def setup_cart_tab(self):
        """Вкладка корзины"""
        tab = self.tabview.tab("Корзина")

        title = ctk.CTkLabel(tab, text="Ваша корзина", font=("Arial", 20))
        title.pack(pady=10)

    def run(self):
        self.window.mainloop()


# Установка: pip install customtkinter
# Запуск:
if __name__ == "__main__":
    app = SportsShopApp()
    app.run()


if __name__ == "__main__":

    print("\nБаза данных готова к использованию! Файл: sports_shop.db")