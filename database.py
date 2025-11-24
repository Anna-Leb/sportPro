import sqlite3
import os


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

    def get_products(self, category_id=None):
        """Получает список товаров"""
        query = '''
            SELECT p.id_товара, p.название, p.описание, p.цена, p.размер, p.модель,
                   c.название as категория, s.имя as поставщик, pic.pic_id as изображение
            FROM товар p
            LEFT JOIN категории_товаров c ON p.id_категории = c.id_категории
            LEFT JOIN поставщик s ON p.id_поставщика = s.id_поставщика
            LEFT JOIN картинки pic ON p.id_товара = pic.product_id
        '''

        if category_id:
            query += ' WHERE p.id_категории = ?'
            return self.execute_query(query, (category_id,))
        else:
            return self.execute_query(query)

    def get_categories(self):
        """Получает список категорий"""
        query = 'SELECT id_категории, название, описание FROM категории_товаров'
        return self.execute_query(query)

    def get_user_cart(self, user_id):
        """Получает корзину пользователя"""
        query = '''
            SELECT c.id_связи, p.id_товара, p.название, p.цена, c.количество, 
                   (p.цена * c.количество) as total, pic.pic_id
            FROM корзина c
            JOIN товар p ON c.id_товара = p.id_товара
            LEFT JOIN картинки pic ON p.id_товара = pic.product_id
            WHERE c.id_user = ?
        '''
        return self.execute_query(query, (user_id,))

    def add_to_cart(self, user_id, product_id, quantity=1):
        """Добавляет товар в корзину"""
        # Проверяем, есть ли уже товар в корзине
        check_query = 'SELECT id_связи, количество FROM корзина WHERE id_user = ? AND id_товара = ?'
        existing = self.execute_query(check_query, (user_id, product_id))

        if existing:
            # Обновляем количество
            new_quantity = existing[0][1] + quantity
            update_query = 'UPDATE корзина SET количество = ? WHERE id_связи = ?'
            return self.execute_query(update_query, (new_quantity, existing[0][0]))
        else:
            # Добавляем новый товар
            insert_query = 'INSERT INTO корзина (id_user, id_товара, количество) VALUES (?, ?, ?)'
            return self.execute_query(insert_query, (user_id, product_id, quantity))

    def remove_from_cart(self, cart_item_id):
        """Удаляет товар из корзины"""
        query = 'DELETE FROM корзина WHERE id_связи = ?'
        return self.execute_query(query, (cart_item_id,))

    def create_order(self, user_id, total_amount):
        """Создает новый заказ"""
        from datetime import date
        query = 'INSERT INTO заказы (дата_заказа, сумма, id_user) VALUES (?, ?, ?)'
        return self.execute_query(query, (date.today(), total_amount, user_id))

    def get_user_orders(self, user_id):
        """Получает заказы пользователя"""
        query = '''
            SELECT o.id_заказа, o.дата_заказа, o.сумма, 
                   GROUP_CONCAT(p.название || ' (x' || oi.количество_в_заказе || ')') as товары
            FROM заказы o
            JOIN элементы_заказа oi ON o.id_заказа = oi.id_заказа
            JOIN товар p ON oi.id_товара = p.id_товара
            WHERE o.id_user = ?
            GROUP BY o.id_заказа
            ORDER BY o.дата_заказа DESC
        '''
        return self.execute_query(query, (user_id,))