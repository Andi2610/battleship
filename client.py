import socket
import threading

class Client:
	
	global host
	global port
	global player_status
	global BUFFER
	
	def connectServer(self):
		try:
			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect((host,port))
			print ("Connected to Server")
			while True:
				player_status=clientsocket.recv(BUFFER)
				print (player_status)
		except:
			print ("error")
	
	
	
if __name__=='__main__':
	
	#connect to server
	host="127.0.0.1"
	port=12345
	BUFFER=4096
	
	client=Client()
	clientthread=threading.Thread(target=client.connectServer)
	clientthread.start()
		