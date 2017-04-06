import GPA
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
	return '''
<form name="input" action="/cha" method="POST">
ID: <input type="text" name="ID"><br>
PASSWORD: <input type="text" name="PWD">
<input type="submit" value="Submit">
</form>
	'''

@app.route('/cha',methods=['GET','POST'])
def chaxun():
	if request.method == 'POST':
		return GPA.chaxun(request.form['ID'],request.form['PWD'])


if __name__=='__main__':
	app.debug=True
	app.run(host='0.0.0.0')