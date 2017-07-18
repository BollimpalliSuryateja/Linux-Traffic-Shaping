#!/usr/bin/python

## main shaper script that will be used for changing the shaper traffic settings
import MySQLdb, os, subprocess
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/interfaces', methods=['GET'])
def ifaces():
	i = subprocess.check_output("ls /sys/class/net",shell=True)
	return "Availabale Interfaces in shaper ("+ip+") are :\n"+i

@app.route('/traffic', methods=['GET', 'POST'])
def check_traffic():
	if(request.args.get('iface')):
		interface = request.args.get('iface')
		cmd = "sudo tc qdisc show dev "+interface
		i = subprocess.check_output(cmd,shell=True)
		j = i.split(' ')
    		d,l,jtr = "delay","loss",10
    		if d in j:
        		a = j.index('delay')
        		a = a + 1
        		delay_value = j[a] 
        		if jtr < len(j):
            			if j[jtr] != "loss":
                			jtr = jtr + 1
                			jitter_value = j[jtr] 
				else:
					jitter_value = "0ms"
		else:
			delay_value = "0ms"
			jitter_value = "0ms"
    		if l in j:
        		b = j.index('loss')
       			b = b + 1
       			loss_value = j[b] 
		else:
			loss_value = "0%"	
		return "\nDelay: "+delay_value+"\nJitter: "+jitter_value+"\nLoss: "+loss_value 

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