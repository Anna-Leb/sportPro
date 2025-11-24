import sqlite3
import os
from datetime import datetime


class Database:
    def __init__(self, db_path='sports_shop.db'):
        self.db_path = db_path
        self._check_database()

    def _check_database(self):
        """Проверяет существование базы данных"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"База данных {self.db_path} не найдена!")

    def get_connection(self):
        """Возвращает соединение с базой данных"""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=None):
        """Выполняет запрос и возвращает результат"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid

            return result
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return None
        finally:
            conn.close()

    # === ПОЛЬЗОВАТЕЛИ ===
    def get_user_by_credentials(self, login, password):
        """Проверяет логин и пароль пользователя"""
        query = 'SELECT user_id, login FROM users WHERE login = ? AND password = ?'
        result = self.execute_query(query, (login, password))
        return result[0] if result else None

    def create_user(self, login, password):
        """Создает нового пользователя"""
        try:
            query = 'INSERT INTO users (login, password) VALUES (?, ?)'
            return self.execute_query(query, (login, password))
        except sqlite3.IntegrityError:
            return None  # Пользователь уже существует

    def check_user_exists(self, login):
        """Проверяет, существует ли пользователь с таким логином"""
        query = 'SELECT user_id FROM users WHERE login = ?'
        result = self.execute_query(query, (login,))
        return bool(result)

    # === ТОВАРЫ ===
    def get_products(self, category_id=None):
        """Получает список товаров"""
        query = '''
            SELECT p.product_id, p.name, p.description, p.price, p.size, p.model,
                   c.name as category_name, s.name as supplier_name, pic.pic_id as image_path
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            LEFT JOIN picture pic ON p.product_id = pic.product_id
        '''

        if category_id:
            query += ' WHERE p.category_id = ?'
            return self.execute_query(query, (category_id,))
        else:
            return self.execute_query(query)

    def get_product_by_id(self, product_id):
        """Получает товар по ID"""
        query = '''
            SELECT p.product_id, p.name, p.description, p.price, p.size, p.model,
                   c.name as category_name, s.name as supplier_name, pic.pic_id as image_path
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            LEFT JOIN picture pic ON p.product_id = pic.product_id
            WHERE p.product_id = ?
        '''
        result = self.execute_query(query, (product_id,))
        return result[0] if result else None

    # === КАТЕГОРИИ ===
    def get_categories(self):
        """Получает список категорий"""
        query = 'SELECT category_id, name, description FROM categories'
        return self.execute_query(query)

    # === КОРЗИНА ===
    def get_user_cart_active(self, user_id):
        """Получает корзину пользователя только с товарами quantity > 0"""
        query = '''
            SELECT c.cart_id, p.product_id, p.name, p.price, c.quantity, 
                   (p.price * c.quantity) as total, pic.pic_id as image_path
            FROM cart c
            JOIN products p ON c.product_id = p.product_id
            LEFT JOIN picture pic ON p.product_id = pic.product_id
            WHERE c.user_id = ? AND c.quantity > 0
        '''
        return self.execute_query(query, (user_id,))

    def add_to_cart(self, user_id, product_id, quantity=1):
        """Добавляет товар в корзину"""
        # Проверяем, есть ли уже товар в корзине
        check_query = 'SELECT cart_id, quantity FROM cart WHERE user_id = ? AND product_id = ?'
        existing = self.execute_query(check_query, (user_id, product_id))

        if existing:
            # Обновляем количество
            new_quantity = existing[0][1] + quantity
            update_query = 'UPDATE cart SET quantity = ? WHERE cart_id = ?'
            return self.execute_query(update_query, (new_quantity, existing[0][0]))
        else:
            # Добавляем новый товар
            insert_query = 'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)'
            return self.execute_query(insert_query, (user_id, product_id, quantity))

    def remove_from_cart(self, cart_id):
        """Удаляет товар из корзины"""
        query = 'DELETE FROM cart WHERE cart_id = ?'
        return self.execute_query(query, (cart_id,))

    def clear_user_cart(self, user_id):
        """Очищает корзину пользователя"""
        query = 'DELETE FROM cart WHERE user_id = ?'
        return self.execute_query(query, (user_id,))

    # === ИЗБРАННОЕ ===
    def add_to_favorites(self, user_id, product_id):
        """Добавляет товар в избранное (с quantity = 0)"""
        # Проверяем, есть ли уже товар в избранном
        check_query = 'SELECT cart_id FROM cart WHERE user_id = ? AND product_id = ? AND favorite = 1'
        existing = self.execute_query(check_query, (user_id, product_id))

        if not existing:
            # Добавляем в корзину с флагом favorite=1 и quantity=0
            insert_query = 'INSERT INTO cart (user_id, product_id, quantity, favorite) VALUES (?, ?, 0, 1)'
            return self.execute_query(insert_query, (user_id, product_id))
        return True

    def remove_from_favorites(self, user_id, product_id):
        """Удаляет товар из избранного"""
        query = 'DELETE FROM cart WHERE user_id = ? AND product_id = ? AND favorite = 1'
        return self.execute_query(query, (user_id, product_id))

    def get_user_favorites(self, user_id):
        """Получает избранные товары пользователя (только favorite=1)"""
        query = '''
            SELECT c.cart_id, p.product_id, p.name, p.description, p.price, p.size, p.model,
                   c.quantity, (p.price * c.quantity) as total, pic.pic_id as image_path
            FROM cart c
            JOIN products p ON c.product_id = p.product_id
            LEFT JOIN picture pic ON p.product_id = pic.product_id
            WHERE c.user_id = ? AND c.favorite = 1
        '''
        return self.execute_query(query, (user_id,))

    def is_product_in_favorites(self, user_id, product_id):
        """Проверяет, есть ли товар в избранном"""
        query = 'SELECT cart_id FROM cart WHERE user_id = ? AND product_id = ? AND favorite = 1'
        result = self.execute_query(query, (user_id, product_id))
        return bool(result)

    # === ЗАКАЗЫ ===
    def create_order(self, user_id, cart_items):
        """Создает новый заказ из корзины"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Рассчитываем общую сумму
            total_amount = sum(item[5] for item in cart_items)  # item[5] - это total

            # Создаем заказ
            cursor.execute(
                'INSERT INTO orders (order_date, total_amount, user_id) VALUES (?, ?, ?)',
                (datetime.now().date(), total_amount, user_id)
            )
            order_id = cursor.lastrowid

            # Добавляем товары в order_items
            for item in cart_items:
                cart_id, product_id, name, price, quantity, total, image_path = item
                cursor.execute(
                    'INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                    (order_id, product_id, quantity)
                )

            # Очищаем корзину
            cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))

            conn.commit()
            return order_id

        except sqlite3.Error as e:
            conn.rollback()
            print(f"Ошибка при создании заказа: {e}")
            return None
        finally:
            conn.close()

    def get_user_orders(self, user_id):
        """Получает заказы пользователя"""
        query = '''
            SELECT o.order_id, o.order_date, o.total_amount, 
                   GROUP_CONCAT(p.name || " (x" || oi.quantity || ")") as items
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.user_id = ?
            GROUP BY o.order_id
            ORDER BY o.order_date DESC
        '''
        return self.execute_query(query, (user_id,))

    def get_order_details(self, order_id):
        """Получает детали заказа"""
        query = '''
            SELECT p.name, p.price, oi.quantity, (p.price * oi.quantity) as total
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?
        '''
        return self.execute_query(query, (order_id,))

    # === МАГАЗИНЫ ===
    def get_unique_shop_addresses(self):
        """Получает уникальные адреса магазинов"""
        query = 'SELECT DISTINCT address FROM shops ORDER BY address'
        return self.execute_query(query)

    def get_shops_with_stock(self, product_id=None):
        """Получает информацию о магазинах и наличии товаров"""
        query = '''
            SELECT s.shop_id, s.address, s.product_id, s.quantity, p.name as product_name
            FROM shops s
            JOIN products p ON s.product_id = p.product_id
        '''

        if product_id:
            query += ' WHERE s.product_id = ?'
            return self.execute_query(query, (product_id,))
        else:
            return self.execute_query(query)

    # === ПОСТАВЩИКИ ===
    def get_suppliers(self):
        """Получает список поставщиков"""
        query = 'SELECT supplier_id, name FROM suppliers'
        return self.execute_query(query)

    # === ИЗОБРАЖЕНИЯ ===
    def get_product_image(self, product_id):
        """Получает путь к изображению товара"""
        query = 'SELECT pic_id FROM picture WHERE product_id = ?'
        result = self.execute_query(query, (product_id,))
        return result[0][0] if result else None

    # === ПОИСК И ФИЛЬТРАЦИЯ ===
    def search_products(self, search_term):
        """Поиск товаров по названию и описанию"""
        query = '''
            SELECT p.product_id, p.name, p.description, p.price, p.size, p.model,
                   c.name as category_name, s.name as supplier_name, pic.pic_id as image_path
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            LEFT JOIN picture pic ON p.product_id = pic.product_id
            WHERE p.name LIKE ? OR p.description LIKE ? OR p.model LIKE ?
        '''
        search_pattern = f'%{search_term}%'
        return self.execute_query(query, (search_pattern, search_pattern, search_pattern))

    def get_products_by_supplier(self, supplier_id):
        """Получает товары по поставщику"""
        query = '''
            SELECT p.product_id, p.name, p.description, p.price, p.size, p.model,
                   c.name as category_name, s.name as supplier_name, pic.pic_id as image_path
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            LEFT JOIN picture pic ON p.product_id = pic.product_id
            WHERE p.supplier_id = ?
        '''
        return self.execute_query(query, (supplier_id,))


# Добавьте эти методы в класс Database в database.py

def get_unique_colors(self):
    """Получает уникальные цвета товаров"""
    query = 'SELECT DISTINCT color FROM products WHERE color IS NOT NULL'
    return self.execute_query(query)


def get_unique_sizes(self):
    """Получает уникальные размеры товаров"""
    query = 'SELECT DISTINCT size FROM products WHERE size IS NOT NULL'
    return self.execute_query(query)


def get_products_grouped(self, filters=None):
    """Получает товары сгруппированные по названию"""
    query = '''
        SELECT 
            name,
            description,
            MIN(price) as min_price,
            MAX(price) as max_price,
            GROUP_CONCAT(DISTINCT color) as colors,
            GROUP_CONCAT(DISTINCT size) as sizes,
            GROUP_CONCAT(DISTINCT model) as models,
            category_name,
            supplier_name
        FROM (
            SELECT 
                p.product_id, p.name, p.description, p.price, p.size, p.model,
                c.name as category_name, s.name as supplier_name,
                COALESCE(p.color, 'Не указан') as color
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
        )
        GROUP BY name, description, category_name, supplier_name
    '''

    return self.execute_query(query)