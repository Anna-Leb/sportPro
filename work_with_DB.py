import sqlite3

def add_sample_data():
    """Добавление тестовых данных для демонстрации"""

    conn = sqlite3.connect('sports_shop.db')
    cursor = conn.cursor()

    try:
        suppliers = [
            ('Nike',),
            ('Adidas',),
            ('Puma',),
            ('Reebok',)
        ]
        cursor.executemany('INSERT INTO suppliers (name) VALUES (?)', suppliers)

        categories = [
            ('Кроссовки', 'Спортивная обувь для бега и тренировок'),
            ('Футболки', 'Спортивные футболки и майки'),
            ('Шорты', 'Спортивные шорты для тренировок'),
            ('Аксессуары', 'Спортивные аксессуары и инвентарь')
        ]
        cursor.executemany('INSERT INTO categories (name, description) VALUES (?, ?)', categories)

        users = [
            ('alex_ivanov', 'password123'),
            ('maria_petrova', 'securepass'),
            ('serg_sidorov', 'qwerty')
        ]
        cursor.executemany('INSERT INTO users (login, password) VALUES (?, ?)', users)

        products = [
            ('Nike Air Max', 'Беговые кроссовки', 129.99, 1, '42', 'Air Max 270', 1),
            ('Adidas Ultraboost', 'Кроссовки для бега', 149.99, 1, '41', 'Ultraboost 22', 2),
            ('Puma DryCell T-shirt', 'Влагоотводящая футболка', 34.99, 2, 'M', 'DryCell', 3),
            ('Nike Dri-FIT Shorts', 'Спортивные шорты', 45.99, 3, 'L', 'Dri-FIT', 1),
            ('Reebok Fitness Gloves', 'Тренировочные перчатки', 24.99, 4, 'Universal', 'Fitness', 4)
        ]
        cursor.executemany(
            'INSERT INTO products (name, description, price, category_id, size, model, supplier_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            products
        )

        from datetime import date
        orders = [
            (date(2024, 1, 15), 129.99, 1),
            (date(2024, 1, 16), 184.98, 2)
        ]
        cursor.executemany(
            'INSERT INTO orders (order_date, total_amount, user_id) VALUES (?, ?, ?)',
            orders
        )

        order_items = [
            (1, 1, 1),  # Заказ 1: 1 шт товара 1
            (2, 2, 1),  # Заказ 2: 1 шт товара 2
            (2, 3, 2)  # Заказ 2: 2 шт товара 3
        ]
        cursor.executemany(
            'INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
            order_items
        )

        cart_items = [
            (1, 4, 1),  # Пользователь 1: 1 шт товара 4 в корзине
            (2, 5, 2),  # Пользователь 2: 2 шт товара 5 в корзине
            (3, 1, 1)  # Пользователь 3: 1 шт товара 1 в корзине
        ]
        cursor.executemany(
            'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
            cart_items
        )

        shop_stock = [
            ('ул. Пушкина, 1', 1, 15),
            ('ул. Пушкина, 1', 2, 8),
            ('пр. Ленина, 25', 3, 20),
            ('пр. Ленина, 25', 4, 12),
            ('ул. Гагарина, 10', 5, 5)
        ]
        cursor.executemany(
            'INSERT INTO shops (address, product_id, quantity) VALUES (?, ?, ?)',
            shop_stock
        )

        conn.commit()
        print("Тестовые данные успешно добавлены!")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")
    finally:
        conn.close()

def get_user_cart(user_id):
    conn = sqlite3.connect('sports_shop.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.product_id, p.name, p.price, c.quantity, (p.price * c.quantity) as total
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = ?
    ''', (user_id,))

    cart_items = cursor.fetchall()
    conn.close()
    return cart_items


def add_to_cart(user_id, product_id, quantity=1):
    conn = sqlite3.connect('sports_shop.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (?, ?, ?)
        ''', (user_id, product_id, quantity))
        conn.commit()
        print("Товар добавлен в корзину!")
    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()


def create_order_from_cart(user_id):
    conn = sqlite3.connect('sports_shop.db')
    cursor = conn.cursor()

    try:
        cart_items = get_user_cart(user_id)
        if not cart_items:
            print("Корзина пуста!")
            return

        total_amount = sum(item[4] for item in cart_items)

        from datetime import date
        cursor.execute('''
            INSERT INTO orders (order_date, total_amount, user_id)
            VALUES (?, ?, ?)
        ''', (date.today(), total_amount, user_id))

        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (order_id, item[0], item[3]))

        cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))

        conn.commit()
        print(f"Заказ #{order_id} создан успешно! Сумма: ${total_amount}")

    except sqlite3.Error as e:
        print(f"Ошибка при создании заказа: {e}")
    finally:
        conn.close()
