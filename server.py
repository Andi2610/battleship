import socket
import threading
import ast


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
			
		
	
	#store ship positions
	def store_ship_positions(self):
		print (type(self.player1))
		try:
			player1_dict=self.player1.recv(BUFFER)
			print (player1_dict)
		except:
			print ("Player1 is unreachable")
			return
		try:
			player2_dict=self.player2.recv(BUFFER)
			print (player2_dict)
		except:
			print ("Player2 is unreachable")
			return

		
		self.player1_matrix=[[0,0,0,0,0,0,0,0,0,0]]*10
		self.player2_matrix=[[0,0,0,0,0,0,0,0,0,0]]*10

		player1_dict=ast.literal_eval(player1_dict)
		player2_dict=ast.literal_eval(player2_dict)

		for key,value in player1_dict.items():
			x=int(value[0])
			y=int(value[1])
			direction=int(value[2])
			if direction==1:
				for i in range(x,x-key):
					self.player1_matrix[i][y]=1
					
			if direction==0:
				for i in range(y,y-key):
					self.player1_matrix[x][i]=1
		
		for key,value in player2_dict.items():
			x=int(value[0])
			y=int(value[1])
			direction=int(value[2])
			if direction==1:
				for i in range(x,x-key):
					self.player2_matrix[i][y]=1
					
			if direction==0:
				for i in range(y,y-key):
					self.player2_matrix[x][i]=1
			
		print (self.player1_matrix)
		print (self.player2_matrix)
	
	def attacking_position(self):
		self.player1.send("Enter attacking positions: ")
		#self.player2.send("Enter attacking positions: ")
		
		self.player1_attack=str(serversocket.recv(BUFFER))
		#self.player1_attack=str(serversocket.recv(BUFFER))
	
	def waitingConnect(self,serversocket):
		n=0
		while True:
			conn,addr=serversocket.accept()
			n+=1
			if n==1:
				self.player1,addr1=conn,addr
				#self.player1.send("Welcome in Battleship game...Wait for player2...")
			if (n==2):
				self.player2,addr2=conn,addr
				self.player1.send("Be ready to fight")
				self.player2.send("Be ready to fight")
				thread1=threading.Thread(target=self.startGame(self.player1))
				thread1.start()
				thread2=threading.Thread(target=self.startGame(self.player2))
				thread2.start()
				n=0

	
		
	def startGame(self,serversocket):
		self.store_ship_positions()
		self.attacking_position()
		
		
	
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
	while True:
		server=Server(serversocket)
		
	