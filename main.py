import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory,render_template
import sqlite3
from myutil import allowed_file
UPLOAD_FOLDER = 'UPLOAD_FOLDER'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
con = sqlite3.connect('example.db',check_same_thread = False)
cur = con.cursor()

def init_db():
    try:
        cur.execute('''CREATE TABLE pics (pname text,price real,desc text)''')
        cur.execute('''CREATE TABLE cart (desc text,price real,image text)''')
        con.commit()
    except:pass

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/products')
def displayAllIMages():
    images=[]
    for row in cur.execute('SELECT * FROM pics'):
        images.append([row[0],row[1],row[2]])
    # print(images)
    return render_template("gallery.html",images=images)

@app.route('/buy/<desc>/<price>/<image>')
def buy(desc,price,image):
    # CREATE TABLE cart (desc text,price real)
    sql =f"INSERT INTO cart VALUES ('{desc}',{price},'{image}')"
    # print(sql)
    cur.execute(sql)
    con.commit()
    return render_template('loans.html')

@app.route('/remove/<id>')
def remove(id):
    # CREATE TABLE cart (desc text,price real)
    sql =f"delete from cart where rowid = {id}"
    # print(sql)
    cur.execute(sql)
    con.commit()
    return loans()

@app.route('/loans')
def loans():
    products=[]
    for row in cur.execute('SELECT *,rowid FROM cart'):
        products.append([row[0],row[1],row[2],row[3]])
        # print(row)
    return render_template('loans.html',products=products)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # post block 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # save file name to DB
            sql =f"INSERT INTO pics VALUES ('{filename}',{request.form.get('price')},'{request.form.get('desc')}')"
            # print(sql)
            cur.execute(sql)
            con.commit()
            
            return displayAllIMages()
            # return redirect(url_for('download_file', name=filename))

    return render_template('up.html')

if __name__ == '__main__':
    app.run(debug=True)
