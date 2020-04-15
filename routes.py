from flask import Flask
from flask import render_template, url_for, request,redirect
from forms import StudentForm
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["flask_mongo"]
students = mydb["students"]


@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
    form = StudentForm()
    if form.validate_on_submit():
            if  request.method == 'POST':
                fullName = form.fullName.data
                email = form.email.data
                phoneNumber = form.phoneNumber.data
                students.insert({'fullName':fullName,'email':email,'phoneNumber':phoneNumber})
                return redirect(url_for('index',message='Data Added'))
                
    return render_template('index.html',form=form)

@app.route('/view')
def view():    
    records = list(students.find({}))            
    return render_template('view.html',records=records)

@app.route('/delete/<string:_id>',methods=['GET','POST'])
def delete(_id):    
    students.remove({"_id": ObjectId(_id)}) 
    return redirect(url_for('view',message='Record Deleted'))


@app.route('/edit/<string:_id>',methods=['GET','POST'])
def edit(_id):
    student = students.find_one({"_id": ObjectId(_id)})
    form = StudentForm()
    if request.method == 'GET':
        form.fullName.data = student['fullName']
        form.email.data = student['email']
        form.phoneNumber.data = student['phoneNumber'] 
    elif  request.method == 'POST':
        if form.validate_on_submit():
                fullName = form.fullName.data
                email = form.email.data
                phoneNumber = form.phoneNumber.data
                students.update({"_id":ObjectId(_id)}, {'$set':{ "fullName":fullName ,"email":email,"phoneNumber":phoneNumber}})
                return redirect(url_for('view',message='Data Updated'))                    
    return render_template('edit.html',form=form)


if __name__ == "__main__":
    app.run(debug=True)
