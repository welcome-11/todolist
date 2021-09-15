from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date 
from io import StringIO
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts, today=date.today())

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)

    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

# フォーム表示
@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

# アップロード機能
@app.route('/upload', methods=['POST'])
def upload():
    try:
        print(request.files)
        #fileの取得（FileStorage型で取れる）
        # https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html
        fs = request.files['file']
        # 下記のような情報がFileStorageからは取れる
        app.logger.info('file_name={}'.format(fs.filename))
        app.logger.info('content_type={} content_length={}, mimetype={}, mimetype_params={}'.format(
        fs.content_type, fs.content_length, fs.mimetype, fs.mimetype_params))
        # ファイルを保存
        fs.save(fs.filename)
        # アップしたファイルをインサートする
        reading_csv(fs.filename)
        return render_template("uploaded.html", data = data)
    except:
        return "ファイルがありません"

# CSVファイルを読み込む関数
def reading_csv(filename):
    data = []
    with open(filename, encoding='cp932') as f:
        reader = csv.reader(f)
        header_ = next(csv.reader(f))
        for row in reader:
            tuples=(row[0], row[1], row[2], row[3], row[4], row[5])
            print(tuples)
            data.append(tuples,)
        return data

if __name__ == "__main__":
    # app.run(debug=True)
    app.run() # こちらに変更