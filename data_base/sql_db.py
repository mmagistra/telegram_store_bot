import sqlite3


class DbWorker:
    def __init__(self):
        self.base = sqlite3.connect('closes_store.db')
        self.cur = self.base.cursor()
        if self.base:
            print('Data base connected')

        self.base.execute('''CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        photo TEXT, 
        gender TEXT, 
        type_of_clothing TEXT, 
        size TEXT, 
        description TEXT, 
        seasonality TEXT, 
        brand TEXT, 
        price TEXT, 
        url TEXT)''')

        self.base.execute('''CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id TEXT, 
        user_name TEXT, 
        role TEXT, 
        mailing TEXT)''')
        # roles: user, admin, super_admin
        # mailing: True/False (default - True)

    def products_add(self, name, photo_id, gender, type_of_clothing, size, style, seasonality, brand, price, url):
        self.cur.execute('''INSERT INTO Products VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
                         (name, photo_id, gender, type_of_clothing, size, style, seasonality, brand, price,
                          url))
        self.base.commit()

    def products_read(self, request_filter='', select_filter='*'):
        sql_request = f'SELECT {select_filter} FROM Products'
        if request_filter != '':
            sql_request += f' WHERE {request_filter}'
        print(sql_request)
        data = self.cur.execute(sql_request).fetchall()
        return data

    def products_update(self, id, **kwargs):
        change_string = ''
        for key, value in kwargs.items():
            change_string += f'{key}="{value}", '
        change_string = change_string[:-2]
        self.cur.execute(f'''UPDATE Products SET {change_string} WHERE id = {id} ''')
        self.base.commit()

    def products_del(self, id):
        self.cur.execute(f'''DELETE FROM Products WHERE id = {id}''')

    def users_add(self, user_id, user_name, role, mailing):
        self.cur.execute('''INSERT INTO Users VALUES(NULL, ?, ?, ?, ?)''',
                         (user_id, user_name, role, mailing))

    def users_update(self, id, **kwargs):
        change_string = ''
        for key, value in kwargs.items():
            change_string += f'{key}="{value}", '
        change_string = change_string[:-2]
        self.cur.execute(f'''UPDATE Users SET {change_string} WHERE id = {id}''')
        self.base.commit()

    def users_read(self, request_filter='', select_filter='*'):
        sql_request = f'SELECT {select_filter} FROM Users'
        if request_filter != '':
            sql_request += f' WHERE {request_filter}'
        data = self.cur.execute(sql_request).fetchall()
        return data

    def shutdown(self):
        self.base.commit()
