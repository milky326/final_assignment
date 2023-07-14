from flask import Flask, render_template, request, redirect, url_for,session
import db,string,random
from datetime import timedelta
#登録ログイン
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))
   

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')


    # ログイン判定
    if db.login(name, password):
        session['user'] = True #sessionにキー:'user',バリュー:Trueを追加
        session.permanent = True #sessionの有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=1)#sessionの有効期限１分
        return redirect(url_for('mypage'))
    else :
        error = 'ユーザ名またはパスワードが違います。'

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {'name':name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
     return render_template('mypage.html')#sessionがあればmypage.htmlを表示
    else:
        return redirect(url_for('index')) #sessionがなければ画面にリダイレクト
@app.route('/userregister')
def register_form():
    return render_template('userregister.html')

@app.route('/user_register_exe', methods=['POST'])
def user_register_exe():
    name = request.form.get('name')
    password = request.form.get('password')

    if name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('userregister.html', error=error, name=name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('userregister.html', error=error)

    count = db.insert_user(name,password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('userregister.html', error=error)
@app.route('/loguout')
def logout():
    session.pop('user',None) 
    return redirect(url_for('index'))

# レイアウトサンプル
@app.route('/')
def sample_top():
    return render_template('mypage.html')

@app.route('/list')
def sample_list():
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)

@app.route('/bookregister')
def book_register():
    return render_template('bookregister.html')

@app.route('/sample_search')
def sample_search():
    return render_template('search.html')

@app.route('/book_select_search', methods=['POST'])
def book_select_search():
    title = request.form.get('keyword')
    book_list = db.select_book(title)
    return render_template('book_select.html',books=book_list)

@app.route('/book_register_exe', methods=['POST'])
def book_register_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    pages = request.form.get('pages')
           
    count = db.insert_book(title, author, publisher, pages)
           
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('mypage', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('bookregister.html', error=error)

@app.route('/book_delete')
def book_delete():
    return render_template('deleteform.html')

@app.route('/book_select_delete', methods=['POST'])
def book_select_delete():
    title = request.form.get('keyword')
    db.delete_book(title)
    return render_template('list.html')



if __name__ == '__main__':
    app.run(debug=True)

