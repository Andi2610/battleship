import socket
import threading


class Server:
	global host
	global port
	
	def __init__(self,serversocket):
		try:
			thread=threading.Thread(target=self.waitingConnect(serversocket))
			thread.start()
		except Exception as e:
			print (e.message)
	
	def waitingConnect(self,serversocket):
		self.player1,addr1=serversocket.accept()
		print ("Got connection from, "+str(addr1))
		self.player1.send("Welcome in Battleship game...Wait for player2...")
		self.player2,addr2=serversocket.accept()
		print ("Got connection from, "+str(addr2))
		self.player1.send("Be ready to fight")
		self.player2.send("Be ready to fight")
		#print (type(player1))
		
	def startGame(self):
		pass
		
	
if  __name__=='__main__':

	host="127.0.0.1"
	port=12345
	

	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		serversocket.bind((host,port))
		print ('Socket binded successfully')
		serversocket.listen(1)
		print ("Server is listening at port %s "%(port))

	except socket.error as err:
		print ("Socket creation failed with an error %s"%(err))
	server=Server(serversocket)
		
	