import sqlite3


def create_table_users():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fill_name TEXT,
        telegram_id INTEGER UNIQUE,
        phone TEXT
        );''')


def create_table_carts():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id),
        total_price DECIMAL(12, 2) DEFAULT 0,
        total_products INTEGER DEFAULT 0 
        );''')


def create_cart_products_table():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name VARCHAR(50) NOT NULL,
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,
        cart_id INTEGER REFERENCES cart(cart_id),
        
        UNIQUE(product_name, cart_id)
    );''')


def create_categories_table():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(30) NOT NULL UNIQUE
    );''')


def insert_categories():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO categories(category_name) VALUES
    ('Лаваши'),
    ('Бургеры'),
    ('Гарниры'),
    ('Пицца'),
    ('Десерты'),
    ('Донар'),
    ('Хот-дог'),
    ('Сэндвичи'),
    ('Напитки'),
    ('Соусы')''')
    database.commit()
    database.close()


def create_products_table():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(30) NOT NULL UNIQUE,
    price DECIMAL(12, 2) NOT NULL,
    description VARCHAR(200),
    image TEXT,
    category_id INTEGER NOT NULL,
    
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
    );''')


def insert_product_table():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    try:
        cursor.execute('''
        INSERT INTO products(category_id, product_name, price, description, image) VALUES
        (1, 'Лаваш говяжий', '33000', 'Говяжье мясо, помидор, чипсы, майонез, соус', 
        'AgACAgIAAxkBAAMHZgvk7Ql7rDnmIlWo2ugjp4rZybwAAvTXMRskh2BIHgsa7-nkkN0BAAMCAANzAAM0BA'),
        (1, 'Лаваш говяжий с сыром', '36000', 'Говяжье мясо, помидор, чипсы, сыр, майонез, соус', 
        'AgACAgIAAxkBAAMHZgvk7Ql7rDnmIlWo2ugjp4rZybwAAvTXMRskh2BIHgsa7-nkkN0BAAMCAANzAAM0BA'),
        (1, 'Лаваш куриный с сыром', '32000', 'Куриная грудка, помидор, чипсы, сыр, соленые огурцы , майонез, соус', 
        'AgACAgIAAxkBAAMHZgvk7Ql7rDnmIlWo2ugjp4rZybwAAvTXMRskh2BIHgsa7-nkkN0BAAMCAANzAAM0BA'),
        (1, 'Лаваш куриный', '35000', 'Куриная грудка, помидор, чипсы, сыр, майонез, соус', 
        'AgACAgIAAxkBAAMHZgvk7Ql7rDnmIlWo2ugjp4rZybwAAvTXMRskh2BIHgsa7-nkkN0BAAMCAANzAAM0BA'),
        (10, 'Соус барбекю Heinz', '6000', 'Аппетитный соус с уникальным ароматом', 
        'AgACAgIAAxkBAAMHZgvk7Ql7rDnmIlWo2ugjp4rZybwAAvTXMRskh2BIHgsa7-nkkN0BAAMCAANzAAM0BA')
        ''')
        database.commit()
        database.close()
    except:
        pass


insert_product_table()


def first_select_user(chat_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user


def first_register_user(chat_id, full_name):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO users(telegram_id, fill_name) VALUES (?, ?)
    ''', (chat_id, full_name))
    database.commit()
    database.close()


def update_user_finish_register(phone, chat_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    UPDATE users
        SET phone = ?
        WHERE telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()


def insert_to_cart(chat_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO carts(user_id) VALUES 
    (
    (SELECT user_id FROM users WHERE telegram_id = ?)
    );
    ''', (chat_id,))
    database.commit()
    database.close()


def get_all_categories():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT * FROM categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories


def get_products_by_category_id(category_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT product_id, product_name FROM products
    WHERE category_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products


def get_product_detail(product_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT * FROM products
    WHERE product_id = ?
    ''', (product_id,))
    products = cursor.fetchone()
    database.close()
    return products


def get_user_cart_id(chat_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT cart_id FROM carts
    WHERE user_id = (
        SELECT user_id FROM users WHERE telegram_id = ?
    )
    ''', (chat_id,))
    cart_id = cursor.fetchone()[0]
    database.close()
    return cart_id


def get_quantity(cart_id, product):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT quantity FROM cart_products
    WHERE cart_id = ? AND product_name = ?
    ''', (cart_id, product))
    quantity = cursor.fetchone()[0]
    database.close()
    return quantity


def insert_or_update_cart_product(cart_id, product_name, quantity, final_price):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    try:
        cursor.execute('''
            INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
            VALUES(?, ?, ?, ?)
            ''', (cart_id, product_name, quantity, final_price))
        database.commit()
        return True
    except:
        cursor.execute('''
        UPDATE cart_products
        SET quantity = ?,
        final_price = ?
        WHERE product_name = ? AND cart_id = ?
        ''', (quantity, final_price, product_name, cart_id))
        database.commit()
        return False
    finally:
        database.close()


def update_total_product_total_price(cart_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    UPDATE carts
    SET total_products = (
    SELECT SUM(quantity) FROM cart_products
    WHERE cart_id = :cart_id
    ),
    total_price = (
    SELECT SUM(final_price) FROM cart_products
    WHERE cart_id = :cart_id
    )
    WHERE cart_id = :cart_id
    ''', {'cart_id': cart_id})
    database.commit()
    database.close()


def get_cart_products(cart_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products


def get_total_products_price(cart_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT total_products, total_price FROM carts 
    WHERE cart_id = ?
    ''', (cart_id,))
    total_products, total_price = cursor.fetchone()
    database.close()
    return total_products, total_price


def get_carts_products_for_delete(cart_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT cart_product_id, product_name FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products


def delete_cart_products_from(cart_product_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    DELETE FROM cart_products 
    WHERE cart_product_id = ?
    ''', (cart_product_id,))
    database.commit()
    database.close()


def drop_cart_products_default(cart_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    DELETE FROM cart_products 
    WHERE cart_id = ?
    ''', (cart_id,))
    database.commit()
    database.close()


def orders_total_price():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders_total_price(
    order_total_price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER REFERENCES carts(cart_id),
    total_price DECIMAL(12, 2) DEFAULT 0,
    total_products INTEGER DEFAULT 0,
    time_now TEXT,
    new_date TEXT
    );
    ''')


def order():
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_total_price_id INTEGER REFERENCES orders_total_price(orders_total_price_id),
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    final_price DECIMAL(12, 2) NOT NULL
    );
    ''')


def save_order_total(cart_id, total_products, total_price, time_now, new_date):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO orders_total_price(cart_id, total_products, total_price, time_now, new_date)
    VALUES(?, ?, ?, ?, ?)
    ''', (cart_id, total_products, total_price, time_now, new_date))
    database.commit()
    database.close()


def orders_total_price_id(cart_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT order_total_price_id FROM orders_total_price
    WHERE cart_id = ?
    ''', (cart_id,))
    order_total_id = cursor.fetchall()[-1][0]
    database.close()
    return order_total_id


def save_order(order_total_id, product_name, quantity, final_price):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    INSERT INTO orders(order_total_price_id, product_name, quantity, final_price)
    VALUES(?, ?, ?, ?)
    ''', (order_total_id, product_name, quantity, final_price))
    database.commit()
    cursor.close()


def get_order_total_price(cart_id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT * FROM orders_total_price
    WHERE cart_id = ?
    ''', (cart_id,))
    orders_total_price = cursor.fetchall()
    database.close()
    return orders_total_price


def get_detail_product(id):
    database = sqlite3.connect('database.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT product_name, quantity, final_price FROM orders
    WHERE order_total_price_id = ?
    ''', (id,))
    detail_product = cursor.fetchall()
    database.close()
    return detail_product
