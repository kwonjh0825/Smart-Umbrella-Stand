import psutil
import os 
import subprocess as sp
import pymysql
from flask import Flask, request, redirect, url_for, render_template, request

app = Flask(__name__)

db = pymysql.connect(host = 'localhost', 
					 user = 'raspi_user', 
					 passwd = 'password',
					 db = 'smart_umbrella', 
					 charset = 'utf8')

cursor = db.cursor()
'''
sql = "SELECT * FROM state"
cursor.execute(sql)
data = cursor.fetchall()
print(data[0])
'''

		
@app.route('/')
def home():
	return render_template('state2.html')
	
@app.route('/home')
def homeBtn():
	return render_template('index.html')
	
@app.route('/water')
def water():
	return render_template('water.html')
	
@app.route('/state')
def state():
	#db access -> This router return page as state value in db
	sql = "SELECT * FROM state where id = 1"
	cursor.execute(sql)
	data = cursor.fetchall()
	htmlFile = "{}.html".format(data[0][2])
	print(htmlFile)
	return render_template(htmlFile)
	#return render_template('state2.html')

@app.route('/state_ajax', methods=['GET', 'POST'])
def state_ajax(): 
	sql = "SELECT * FROM state where id = 1"
	cursor.execute(sql)
	data = cursor.fetchall()
	originalStateDate = "{}.html".format(data[0][2])
	if request.args.get('state') == 'state0':
		print('/state_ajax >> state0')
		if originalStateDate == request.args.get('state'):
			return 'Same as before' 
		else:
			#db access
			renewalSql = "UPDATE state SET value = '{}' WHERE id = 1".format(request.args.get('state'))
			cursor.execute(renewalSql)
			db.commit()
			return render_template("{}.html".format(request.args.get('state')))
		
	elif request.args.get('state') == 'state1':
		print('/state_ajax >> state1')
		if originalStateDate == request.args.get('state'):
			return 'Same as before' 
		else:
			#db access
			renewalSql = "UPDATE state SET value = '{}' WHERE id = 1".format(request.args.get('state'))
			cursor.execute(renewalSql)
			db.commit()
			return render_template("{}.html".format(request.args.get('state')))
		
	elif request.args.get('state') == 'state2':
		print('/state_ajax >> state2')
		if originalStateDate == request.args.get('state'):
			return 'Same as before' 
		else:
			#db access
			renewalSql = "UPDATE state SET value = '{}' WHERE id = 1".format(request.args.get('state'))
			cursor.execute(renewalSql)
			db.commit()
			return render_template("{}.html".format(request.args.get('state')))
		
	elif request.args.get('state') == 'state3':
		print('/state_ajax >> state3')
		if originalStateDate == request.args.get('state'):
			return 'Same as before' 
		else:
			#db access
			renewalSql = "UPDATE state SET value = '{}' WHERE id = 1".format(request.args.get('state'))
			cursor.execute(renewalSql)
			db.commit()
			return render_template("{}.html".format(request.args.get('state')))
		
	
@app.route('/ON')
def ON():
	#process = sp.Popen('/home/pi/SmartUmb/main.py')
	
	os.system("python3 main.py")
	return redirect(url_for('home'))
@app.route('/OFF')
def OFF():
	#os.system('taskkill.exe /f /im main.py')
	# os.system('kill -9 python3 main.exe')
	
	# procname = "python3 main.py"
	# for proc in psutil.process_iter():
	# 	if proc.name() == procname:
	# 		proc.kill()

	print("exit")
	return redirect(url_for('home'))
	
	
if __name__ == '__main__':
	print("server  Start")
	app.run()
