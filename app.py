from operator import and_
from flask import Flask, request, render_template, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import os
from os import write
import cv2 
import numpy as np
import psycopg2

global state

UPLOAD_FOLDER = '/Line_bot_project/static/upload'
SCREEN_SHOT = '/Line_bot_project/static/screen_state'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]  = "postgresql+psycopg2://postgres:banana@172.17.0.2:5432/database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SCREEN_SHOT'] = SCREEN_SHOT
db = SQLAlchemy(app)

class image_schedule(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    created_date = db.Column(db.DateTime,default=datetime.now)
    schedule_date = db.Column(db.DateTime,nullable=False)
    name = db.Column(db.String(300))
    uuid = db.Column(db.String(100))
    
    def __repr__(self):
        return '<Task %r>'%self.id

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now)

    def __repr__(self):
        return '<Task %r>'%self.id

@app.route('/delete_cus/<int:id>')
def delete_cus(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/customer_list/')
    except:
        return 'There was an issue'


@app.route('/update_cus/<int:id>',methods=['GET','POST'])
def update_cus(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/customer_list/')
        except:
            return 'There was an issue'
    else:
        return render_template('update.html', task = task)


@app.route('/uploadImage/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        #try:
            uploaded_image = request.files.getlist('files[]')
            scheduledate = request.form['schedule_dt']
            python_dt = datetime(*[int(v) for v in scheduledate.replace('T', '-').replace(':', '-').split('-')])
            for f in uploaded_image:
                new_uuid = str(uuid.uuid4())
                new_content = image_schedule(schedule_date=python_dt,name=f.filename,uuid=new_uuid)
                #try:
                db.session.add(new_content)
                db.session.commit()
                file_name = new_uuid
                f.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name+".png"))
                #except:
                    #return 'There was an issue submiting the request'
            return redirect('/uploadImage/')
        #except:
            r#eturn 'Please enter the time and upload the picutre'
    else:
        tasks = image_schedule.query.order_by(image_schedule.id).all()
        return render_template('index.html',tasks = tasks)

@app.route('/customer_list/',methods=['POST','GET'])
def cus_list():
    if (request.method == 'POST'):
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/customer_list/')
        except:
            return 'There was an issue'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('customer.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    to_delete = image_schedule.query.get_or_404(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/uploadImage/')
    except:
        return 'There was a problem deleting the image'

@app.route('/check_img/',methods=['GET'])
def checkImg():
    curr_time = datetime.now()
    from_time = curr_time - timedelta(minutes= 60)
    from_time = from_time.strftime("%Y-%m-%d %H:%M:%S")
    curr_time = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    res = db.session.query(image_schedule).filter(and_(image_schedule.schedule_date<=curr_time,image_schedule.schedule_date>=from_time)).all()
    images = [r.uuid for r in res]
    val = {
        "images": images
    }
    return val

@app.route('/get_cus_list/',methods=['GET'])
def get_cus():
    res = db.session.query(Todo).all()
    cus_list = [r.content for r in res]
    cus_dict = {
        "customer":cus_list
    }
    return cus_dict


@app.route('/static/screen_state',methods=['POST'])
def getScreen():
    try:
        global state
        f = request.get_data()
        open(os.path.join(app.config['SCREEN_SHOT'],"screen.png"),"wb")
        fd = os.open('/home/sorawitchok/Line_bot_project/static/screen_state/'+"screen.png",os.O_RDWR)
        write(fd,f)
        os.close(fd)
        screen = cv2.imread('/home/sorawitchok/Line_bot_project/static/screen_state/screen.png')
        login_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/login.png')
        chat_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/chat.png')
        friend_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/friend.png')
        add_friend_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/add_friend.png')

        state = 'None'

        result = cv2.matchTemplate(login_check,screen,cv2.TM_SQDIFF)

        H,W = np.unravel_index(result.argmax(),result.shape)
        h,w,c = login_check.shape
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        h1 , w1 = min_loc

        if min_val < 0.000000000000001:
            state = 'login'
        else:
            pass

        result = cv2.matchTemplate(chat_check,screen,cv2.TM_SQDIFF)

        H,W = np.unravel_index(result.argmax(),result.shape)
        h,w,c = login_check.shape
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        h1 , w1 = min_loc

        if min_val < 0.000000000000001:
            state = 'chat'
        else:
            pass

        result = cv2.matchTemplate(friend_check,screen,cv2.TM_SQDIFF)

        H,W = np.unravel_index(result.argmax(),result.shape)
        h,w,c = login_check.shape
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        h1 , w1 = min_loc

        if min_val < 0.000000000000001:
            state = 'friend'
        else:
            pass

        result = cv2.matchTemplate(add_friend_check,screen,cv2.TM_SQDIFF)

        H,W = np.unravel_index(result.argmax(),result.shape)
        h,w,c = login_check.shape
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        h1 , w1 = min_loc

        if min_val < 0.000000000000001:
            state = 'add friend'
        else:
            pass
        return state
    except:
        return 'Some error occur'

@app.route('/get_state/', methods=['GET'])
def getState():
    global state
    return state
 

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="0.0.0.0")
