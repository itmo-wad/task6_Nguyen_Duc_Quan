from flask import Flask, send_from_directory, url_for, request, flash, redirect
from flask import render_template
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS ={'txt','pdf','png','jpg','jpeg','gif'}

app = Flask(__name__)
myclient = MongoClient('localhost',27017)
mydb = myclient["mydb"]
mydb = myclient["lab4"]
mycol = mydb["accounts"]
app.secret_key = 'this is secret key'
app.config['UPLOAD_FOLDER'] = 'upload'
# logins = {'admin': 'admin'}
session = False

def allowed_file(filename):
	return '.' in filename and filename.rsplit ('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET','POST'])
def login():
	error = None
	global session
	if request.method == 'POST':
		doc = mycol.find_one({"username": request.form['username']})
		try:
			if request.form['password'] == doc["password"]:
				session = True
				return redirect ('cabinet')
			error = "Invalid credentials"
		except:
			error = "Invalid credentials"
	return render_template('login.html', error = error)


@app.route('/upload/<path:filename>')
def upload(filename):
    return send_from_directory('upload', filename)		

@app.route('/cabinet', methods = ['GET','POST'])
def cabinet():
	if request.method == 'GET':
		global session
		if session == True:
			return render_template('gallery.html')
		else: 
			return redirect ('/')
	
	if 'file' not in request.files:
		flash ('No file part', 'danger')
		return redirect(request.url)
	
	file = request.files['file']
	if file.filename == '':
		flash('No selected file','danger')
		return redirect(request.url)

	if not allowed_file(file.filename):
		flash('Invalid file extension', 'danger')
		return redirect (request.url)

	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		flash('Successfully saved', 'success')
		return redirect (url_for('upload', filename=filename))
	
	


@app.route('/register', methods = ['GET','POST'])
def register():
	global session
	if request.method == "GET":
		return render_template('register.html')
	else:
		try:
			doc = mycol.find_one({"username": request.form['username']})
			if request.form['username'] in doc["username"]:
				flash("This username is already in use. Please try another one")
				return render_template('register.html')
		except:
			mycol.insert_one({"username": request.form['username'], "password": request.form['password']})
			session = True
			return redirect ('cabinet')
			
@app.route('/logout')
def logout():
	global session
	session = False
	return redirect ('/')

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('img', filename)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)