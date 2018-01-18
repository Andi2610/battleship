import socket
import threading


class Server:
	global host
	global port
	global BUFFER
	
	def __init__(self,serversocket):
		try:
			thread=threading.Thread(target=self.waitingConnect(serversocket))
			thread.start()
		except Exception as e:
			print (e.message)
	
	def waitingConnect(self,serversocket):
		n=0
		while True:
		conn,addr=serversocket.accept()
			if n==1:
				self.player1,addr1=conn,addr
				thread1=threading.Thread(target=self.startGame(self.player1))
				thread1.start()
				self.player1.send("Welcome in Battleship game...Wait for player2...")
			n+=1
			if (n==2):
				self.player2,addr2=conn,addr
				thread2=threading.Thread(target=self.startGame(self.player2))
				thread2.start()
				self.player1.send("Be ready to fight")
				self.player2.send("Be ready to fight")
				n=0

		
	
	#enter ship positions
	def enterShipPositions(self,serversocket):
		self.player1.send("Enter ship positions")
		self.player2.send("Enter ship positions")
		self.player1_ship=dict()
		self.player2_ship=dict()
		try:
			for i in range(5):
				self.player1_ship[(i+1)]=str(serversocket.recv(BUFFER))
		except:
			print ("Player1 is unreachable")
			return
		try:
			for i in range(5):
				self.player2_ship[(i+1)]=str(serversocket.recv(BUFFER))
		except:
			print ("Player2 is unreachable")
			return
	
	def attackingposition(self,serversocket):
		self.player1.send("Enter attacking positions: ")
		self.player2.send("Enter attacking positions: ")
		
		self.player1_attack=str(serversocket.recv(BUFFER))
		self.player1_attack=str(serversocket.recv(BUFFER))
		
	def startGame(self,serversocket):
		enterShipPositions(self,serversocket)
		attackingposition(self,serversocket)
		
		
	
if  __name__=='__main__':

	host="127.0.0.1"
	port=12345
	BUFFER=4096
	

	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		serversocket.bind((host,port))
		print ('Socket binded successfully')
		serversocket.listen(2)
		print ("Server is listening at port %s "%(port))

	except socket.error as err:
		print ("Socket creation failed with an error %s"%(err))
	server=Server(serversocket)
		
	