import os 
import subprocess as sp
from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)



@app.route('/')
def home():
	return render_template('index.html')

@app.route('/ON')
def ON():
	#process = sp.Popen('/home/pi/SmartUmb/main.py')
	os.system("python3 main.py")
	return redirect(url_for('home'))
	
@app.route('/OFF')
def OFF():
	#os.system('taskkill.exe /f /im main.py')
	#os.system('killall -9 main.exe')
	
	print("exit")
	return redirect(url_for('home'))
	
	
if __name__ == '__main__':
	print("server  Start")
	app.run()
