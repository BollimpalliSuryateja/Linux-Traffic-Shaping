from flask import Flask, redirect, url_for render_template, request, os, subprocess
app = Flask(__name__)

@app.route('/controller')
def index():
   return render_template('login_proj.html')
   
@app.route('/login', methods=['GET', 'POST']) 
def login():
	 user = request.form['uname']
	 code = request.form['pwd']
	 if user == "ltsadmin" and code == "ltslabb00":
	 	Session['login'] = 'True'
	 	Session['user'] = user
	 	Session['pass'] = code
	 	return render_template('main.html')
	 else:
	 	return redirect(url_for('index')) 

@app.route('/change_traffic', methods=['GET', 'POST'])
def change_traffic():
	if 'login' in session:
		ip = request.form['ip']
		iface = request.form['iface']
		if (request.form['dlay']):
			delay = request.form['dlay']
		else:
			delay = "0ms"
		if (request.form['loss']):
			loss = request.form['loss']
		else:
			loss = "0%"
		if (request.form['jitter']):
			jitter = request.form['jitter']
		else:
			jitter = "0ms"
		cmd = 'curl -X POST "http://'+ip+':5000/shaping?u='+session['user']+'&p='+session['pass']+'&iface='+iface+'&delay='+delay+'&jitter='+jitter+'&loss='+loss+'"'
		e = subprocess.check_output(cmd, shell=True)
		return e
	else:
		return redirect(url_for('index'))

@app.route('/view_traffic', methods=['GET', 'POST'])
def view_traffic():
	if 'login' in session:
		ip = request.form['ip']
		iface = request.form['iface']
		cmd = 'curl -X GET "http://'+ip+':5000/traffic?u='+session['user']+'&p='+session['pass']+'&iface='+iface+'"'
		e = subprocess.check_output(cmd, shell=True)
	else:
		return redirect(url_for('index'))


@app.route('/delete_traffic', methods=['GET', 'POST'])
def delete_traffic():
	if 'login' in session:
		ip = request.form['ip']
		iface = request.form['iface']
		cmd = 'curl -X DELETE "http://'+ip+':5000/traffic?u='+session['user']+'&p='+session['pass']+'&iface='+iface+'"'
		e = subprocess.check_output(cmd, shell=True)
	else:
		return redirect(url_for('index'))

@app.route('/view_int', methods=['GET', 'POST'])
def interfaces():
	if 'login' in session:
		ip = request.form['ip']
		cmd = 'curl -X GET "http://'+ip+':5000/interfaces"'
		e = subprocess.check_output(cmd, shell=True)
	else:
		return redirect(url_for('index'))

@app.route('/shaper_nodes')
def available_nodes():
	if 'login' in session:
	else:
		return redirect(url_for('index'))

@app.route('/home')
def home():
	if 'login' in session:
		return render_template('main.html')
	 else:
	 	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session.pop('user', None)
	session.pop('pass', None)
	session.pop('login', None)
	return redirect(url_for('index'))
				
if __name__ == '__main__':
   app.run('0.0.0.0')
