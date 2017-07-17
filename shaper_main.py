#!/usr/bin/python

## main shaper script that will be used for changing the shaper traffic settings
import MySQLdb, os
from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/shaping', methods=['GET', 'POST'])
def traffic():
	if(request.args.get('iface')):
		interface = request.args.get('iface')
		if (request.args.get('action')):
			action = request.args.get('action')
			cmd1 = "sudo tc qdisc del dev " + interface + " root netem" 
			remove_traffic = os.system (cmd1)
			if (request.args.get('delay')):
				delay = request.args.get('delay')
			else: 
				delay = "0ms"
			if (request.args.get('loss')):
				loss = request.args.get('loss')
			else: 
				loss = "0%"
			if (request.args.get('jitter')):
				jitter = request.args.get('jitter')
			else: 
				jitter = "0ms"
			cmd = "sudo tc qdisc add dev " + interface + " root netem delay " + delay +" "+ jitter+" loss " + loss
			comm = os.system (cmd) 
			return "\n\nTraffic shaped successfully on "+interface+"\nTraffic on "+interface+" is as follows:\ndelay:"+delay+"\njitter:"+jitter+"\nloss:"+loss+"\n\n"  
		else:
			return 'Enter the action on the interface ' + interface
	else:
		return "Enter the interface and try again ..."
  
  if __name__ == '__main__':
   app.run('0.0.0.0')
