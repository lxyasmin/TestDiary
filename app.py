from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
app = Flask(__name__)


client= MongoClient("mongodb+srv://yasmin:yasmin@cluster0.yrjugsf.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'picture-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)
    
    profile = request.files['profile_give']
    print(profile)
    extension = profile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    profile_name = f'profile-{mytime}.{extension}'
    save_to = f'static/{profile_name}'
    profile.save(save_to)
    
    count = db.diary.count_documents({})
    num = count + 1

    doc = {
        'num': num,
        'file':filename,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive,
        'time': today.strftime('%Y.%m.%d')
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Upload complete!'})

@app.route("/diary/delete", methods=["POST"])
def delete():
    num_delete = request.form['delete_num']
    db.diary.delete_one({'num' : int(num_delete)})
    return jsonify({'msg': 'delete done!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
