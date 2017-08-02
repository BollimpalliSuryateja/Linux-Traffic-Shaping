# this file is to detect the traffic that has been changed through shaper console 

#!/usr/bin/python

import MySQLdb, os, subprocess, socket, time

#to get the ip address of the host
ip = socket.gethostbyname(socket.gethostname())

db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
cursor = db.cursor()

while ():
	interfaces = subprocess.check_output("ls /sys/class/net",shell=True)
	ifaces = []
	ifaces = interfaces.splitlines()

	for iface in ifaces:
# to retrieve the present traffic settings in order to compare them against the old values
		cmd = "sudo tc qdisc show dev "+iface
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
	
		sql = 'SELECT delay,jitter,loss FROM `'+ip+'` where interface = "'+iface+'"'
	
		try:	
   			cursor.execute(sql)
   			results = cursor.fetchall()
   			for row in results:
      			odelay = row[0]
      			ojitter = row[1]
      			oloss = row[2]
      			if (odelay != delay_value):	
      				sql_d = 'update `'+ip+'` set delay = "'+delay_value+'" where interface = "'+iface+'"'
      				cursor.execute(sql_d)
      			if (oloss != loss_value):	
      				sql_l = 'update `'+ip+'` set loss = "'+loss_value+'" where interface = "'+iface+'"'
      				cursor.execute(sql_l)
      			if (ojitter != jitter_value):	
      				sql_j = 'update `'+ip+'` set jitter = "'+jitter_value+'" where interface = "'+iface+'"'
      				cursor.execute(sql_j)
      			
## if the values does not match then we also need to update in the log file     
      	except:
   			print "Error: unable to fecth data"
	time.sleep(5)
# disconnect from server
db.close()
