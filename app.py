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
        
        id = request.form.get('id')
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(id=id, title=title, detail=detail, due=due)

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

# ??????????????????
@app.route('/upload', methods=['GET'])
def home():
    return render_template("upload.html")

# ????????????????????????
@app.route('/upload', methods=['POST'])
def upload():
    try:
        print(request.files)
        print("2------")

        #file????????????FileStorage??????????????????
        # https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html
        fs = request.files['file']
        print("3------")
        
        # ???????????????????????????FileStorage??????????????????
        app.logger.info('file_name={}'.format(fs.filename))
        app.logger.info('content_type={} content_length={}, mimetype={}, mimetype_params={}'.format(
            fs.content_type, fs.content_length, fs.mimetype, fs.mimetype_params))
        print("4------")

        # ?????????????????????
        fs.save(fs.filename)
        print("5------")

        # ???????????????????????????????????????????????????
        data=reading_csv(fs.filename)
        insert_sql(data)
        print(data)
        
        return render_template("uploaded.html", data = data)
    except:
        print("except")
        return "??????????????????????????????"

# CSV?????????????????????????????????
def reading_csv(filename):
    data = []
    with open(filename, encoding='utf-8') as f:#windows???mac?????????????????????????????????OS???????????????????????????????????????
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

# CSV?????????????????????????????????
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
    print(date_fruit_list)
    return render_template('date_fruits.html', title='?????????????????????', date_fruit_list=date_fruit_list)
    #return render_template('date_fruits.html')


@app.route("/export")
def export_action():
    # ????????????????????????????????????
    paths = os.path.abspath(__file__)[:-7]
    print(paths)
    return send_from_directory(
        directory=paths + '/input',
        path='testdata.csv',
        as_attachment=True,
        attachment_filename='testdata.csv',
    )

if __name__ == "__main__":
    app.run(debug=True)#debug??????
    #app.run() # ????????????