from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date 
from io import StringIO
import csv,os
import pandas as pd

from flask_sqlalchemy.model import Model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
data=[]


class Post(db.Model):
    __tablename__ = 'Todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

class ergamechoice(db.Model):
    __tablename__ = 'ergamechoice'
    id = db.Column(db.Integer, primary_key=True)
    thema_id = db.Column(db.Integer)
    res = db.Column(db.String(100))
    vote_num = db.Column(db.Integer)

class ergamethema(db.Model):
    __tablename__ = 'ergamethema'
    id = db.Column(db.Integer, primary_key=True)
    thema = db.Column(db.String(200))

class er_room(db.Model):
    __tablename__ = 'er_room'
    id = db.Column(db.Integer, primary_key=True)
    room_name= db.Column(db.String(200))
    thema_id = db.Column(db.Integer)
    player_num=db.Column(db.Integer)
    room_status=db.Column(db.Integer)
    room_pass=db.Column(db.Integer)

###############メイン画面###############################
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        print(posts)
        return render_template('index.html', posts=posts, today=date.today())

    else:
        id = request.form.get('id')
        if id != None:
            title = request.form.get('title')
            detail = request.form.get('detail')
            due = request.form.get('due')
            print(id,title,detail,due)
            due = datetime.strptime(due, '%Y-%m-%d')
            new_post = Post(id=id, title=title, detail=detail, due=due)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')

        else:
            id2 = request.form.get('id2')
            title2 = request.form.get('title2')
            detail2 = request.form.get('detail2')
            due2 = request.form.get('due2')
            
            due2 = datetime.strptime(due2, '%Y-%m-%d')
            print(id2,title2,detail2,due2)
            
            new_ergame = ergame(id2=id2, title2=title2, detail2=detail2, due2=due2)

            db.session.add(new_ergame)
            db.session.commit()
            return redirect('/')

##############TODOアプリ###############################
@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    print(post)
    return render_template('detail.html', post=post)

@app.route('/detail_test/<int:id2>')
def read_test(id2):
    ergames = ergame.query.get(id2)
    print(ergames)
    return render_template('detail_test.html', ergames=ergames)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/add')
def add():
    example = Post()
    #example.id = 1
    example.title = 'auto title'
    example.detail = 'auto detail'
    example.due = datetime.strptime('2021-09-20', '%Y-%m-%d')
    print(example)

    db.session.add(example)
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
        print(post.due)

        db.session.commit()
        return redirect('/')

# フォーム表示
@app.route('/upload', methods=['GET'])
def home():
    return render_template("upload.html")

# アップロード機能
@app.route('/upload', methods=['POST'])
def upload():
    try:
        print(request.files)
        print("2------")

        #fileの取得（FileStorage型で取れる）
        # https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html
        fs = request.files['file']
        print("3------")
        
        # 下記のような情報がFileStorageからは取れる
        app.logger.info('file_name={}'.format(fs.filename))
        app.logger.info('content_type={} content_length={}, mimetype={}, mimetype_params={}'.format(
            fs.content_type, fs.content_length, fs.mimetype, fs.mimetype_params))
        print("4------")

        # ファイルを保存
        fs.save(fs.filename)
        print("5------")

        # アップしたファイルをインサートする
        data=reading_csv(fs.filename)
        insert_sql(data)
        print(data)
        
        return render_template("uploaded.html", data = data)
    except:
        print("except")
        return "ファイルがありません"

# CSVファイルを読み込む関数
def reading_csv(filename):
    data = []
    with open(filename, encoding='utf-8') as f:#windowsとmacで文字コードが異なる。OSに依存しない対応を要検討。
        print(f)
        reader = csv.reader(f)
        print(reader)

        header_ = next(csv.reader(f))
        for row in reader:
            tuples=(row[0], row[1], row[2])
            print(tuples)
            data.append(tuples,)
    print(data)
    return data

# CSVファイルを書き込む関数
def insert_sql(data):
    for temp in data:
        print(temp)
        example = Post()
        #example.id = 1
        example.title = temp[0]
        example.detail = temp[1]
        example.due = datetime.strptime(temp[2], '%Y-%m-%d')
        print(example)

        db.session.add(example)
        db.session.commit()
        #return redirect('/')

@app.route('/test')
def csv_display(): 
    date_fruit_list = pd.read_csv("./input/testdata.csv").values.tolist()
    #df= pd.DataFrame(date_fruit_list)
    df= pd.DataFrame(date_fruit_list)

    df.to_csv("./input/testdata2.csv")#ファイルがあったら、上書きしてる
    print(date_fruit_list)
    return render_template('date_fruits.html', title='食べた果物記録', date_fruit_list=date_fruit_list)
    #return render_template('date_fruits.html')


@app.route("/export")
def export_action():
    # 現在のディレクトリを取得
    paths = os.path.abspath(__file__)[:-7]
    print(paths)
    return send_from_directory(
        directory=paths + '/input',
        path='testdata.csv',
        as_attachment=True,
        attachment_filename='testdata.csv',
    )

#################ライン返信ゲーム##################################
@app.route('/vote/<int:id2>', methods=['GET', 'POST'])
def vote(id2):
    post = ergame.query.get(id2)
    if request.method == 'GET':
        return render_template('wait.html', post=post)
    else:
        post.title2 = request.form.get('title2')
        post.detail2 = request.form.get('detail2')
        post.due2 = datetime.strptime(request.form.get('due2'), '%Y-%m-%d')
        print(post.due2)

        db.session.commit()
        return redirect('/')

@app.route('/erhome', methods=['GET'])
def ehome():
    posts = er_room.query.all()
    print(posts)
    return render_template('erhome.html', posts=posts)

@app.route('/ercreate')
def ercreate():
    return render_template('ercreate.html')

@app.route('/er_thema_create')
def er_thema_create():
    return render_template('er_thema_create.html')

@app.route('/er_thema_create_process', methods=['GET', 'POST'])
def er_thema_create_prosecc():
    if request.method == 'GET':
        posts = ergamethema.query.all()
        print(posts)
        return render_template('erhome.html', posts=posts)

    else:
        id = request.form.get('id')
        thema= request.form.get('thema')
        print(id,thema)
        
        new_post = ergamethema(id=id, thema=thema)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/erhome')

@app.route('/er_create_room')
def er_create_room():
    return render_template('er_create_room.html')

@app.route('/er_delete_room/<int:id>')
def er_delete_room(id):
    post = er_room.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/erhome')

@app.route('/er_create_room_process', methods=['POST'])
def er_create_room_prosecc():
    
    id = request.form.get('id')
    room_name = request.form.get('room_name')
    room_pass = request.form.get('room_pass')
    thema_id = 0
    player_num = 0
    room_status = 0

    print(id,room_name,room_pass,thema_id,player_num,room_status)        
    new_post = er_room(id=id, room_name=room_name,room_pass=room_pass,thema_id=thema_id,player_num=player_num,room_status=room_status)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/erhome')


@app.route('/er_delete/<int:id>')
def er_delete(id):
    post = ergamethema.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/erhome')

#@app.route('/er_create_room', methods=['GET', 'POST'])
#def er_create_room():
#    if request.method == 'GET':
#        ergames = ergamethema.query.all()
#        print(ergames)
#        return render_template('er_create_room.html', ergames=ergames)
#    else:
#        return redirect('/erhome')

if __name__ == "__main__":
    app.run(debug=True)#debug環境
    #app.run() # 本番環境