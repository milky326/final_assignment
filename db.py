import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return password

def insert_user(name, password):
    sql = 'INSERT INTO tosho_user VALUES(default, %s, %s, %s)'

    salt = get_salt()
    password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (name, password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

def login(name, password):
    sql = 'SELECT password, salt FROM tosho_user WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (name,))
        user = cursor.fetchone()

        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            password = get_hash(password, salt)

            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if password == user[0]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT title, author, publisher, pages FROM book"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows


def select_book(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT title, author, publisher, pages FROM book where title LIKE %s"
    
    key='%'+title+'%'
    
    cursor.execute(sql,(key,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def delete_book(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM book WHERE title =%s"
    
    cursor.execute(sql,(title,))
    connection.commit()
    
    cursor.close()
    connection.close()


def insert_book(title, author, publisher, pages):
    connection = get_connection()
    cursor = connection.cursor()
 
    try :
        sql = 'INSERT INTO book VALUES (default, %s, %s, %s, %s)'
    

        cursor.execute(sql, (title, author, publisher, pages))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count