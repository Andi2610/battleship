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
			
		
	#evaluate hit or miss
	def evaluate_hit_miss(self,player):
		if player=="1":
			if self.player2_matrix[self.player1_x][self.player1_y]>0:
				self.player1_score+=1
				key=self.player2_matrix[self.player1_x][self.player1_y]
				self.player2_matrix[self.player1_x][self.player1_y]=-key
				value=self.player2_dict[key]
				x=int(value[0])
				y=int(value[1])
				direction=int(value[2])
				count=0
				if (direction==1):
					for i in range(y,y+key):
						if self.player2_matrix[x][i]==-key:
							count+=1
					if count ==key:
						self.player1.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
						self.player2.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
					else:
						self.player1.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
						self.player2.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
				else:
					for i in range(x,x+key):
						if self.player2_matrix[i][y]==-key:
							count+=1
					if count ==key:
						self.player1.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
						self.player2.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
					else:
						self.player1.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
						self.player2.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
				
				return "hit"
			elif self.player2_matrix[self.player1_x][self.player1_y]==0:
				self.player1.sendall(str('umiss'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score))
				self.player2.sendall(str('miss'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score))
				return "miss"
		if player=="2":
			if self.player1_matrix[self.player2_x][self.player2_y]>0:
				self.player2_score+=1
				key=self.player1_matrix[self.player2_x][self.player2_y]
				self.player1_matrix[self.player2_x][self.player2_y]=-key
				value=self.player1_dict[key]
				x=int(value[0])
				y=int(value[1])
				direction=int(value[2])
				count=0
				if (direction==1):
					for i in range(y,y+key):
						if self.player1_matrix[x][i]==-key:
							count+=1
					if count ==key:
						self.player2.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
						self.player1.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
					else:
						self.player2.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
						self.player1.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
				else:
					for i in range(x,x+key):
						if self.player1_matrix[i][y]==-key:
							count+=1
					if count ==key:
						self.player2.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
						self.player2.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(key))
					else:
						self.player2.sendall(str('uhit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
						self.player1.sendall(str('hit'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score),str(0))
				return "hit"
			elif self.player1_matrix[self.player1_x][self.player1_y]==0:
				self.player2.sendall(str('umiss'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score))
				self.player1.sendall(str('miss'),str(self.player1_x),str(self.player1_y),str(self.player1_score),str(self.player2_score))
				return "miss"
			
		
		
	
	#store ship positions
	def store_ship_positions(self):
		print (type(self.player1))
		try:
			print ("heyy")
			self.player1_dict=self.player1.recv(BUFFER)
			print ("heyy1")
			print (self.player1_dict)
		except:
			print ("Player1 is unreachable")
			return
		try:
			self.player2_dict=self.player2.recv(BUFFER)
			print (self.player2_dict)
		except:
			print ("Player2 is unreachable")
			return
		
		self.player1_matrix=[[0,0,0,0,0,0,0,0,0,0] for i in range(10)]
		self.player2_matrix=[[0,0,0,0,0,0,0,0,0,0] for i in range(10)]

		self.player1_dict=ast.literal_eval(self.player1_dict)
		self.player2_dict=ast.literal_eval(self.player2_dict)

		for key,value in self.player1_dict.items():
			x=int(value[0])
			y=int(value[1])
			direction=int(value[2])
			if direction==1:
				for i in range(y,y+key):
					self.player1_matrix[x][i]=key
					
			if direction==0:
				for i in range(x,x+key):
					self.player1_matrix[i][y]=key
		
		for key,value in self.player2_dict.items():
			x=int(value[0])
			y=int(value[1])
			direction=int(value[2])
			if direction==1:					# 1: horizontal
				for i in range(y,y+key):
					self.player2_matrix[x][i]=key
					
			if direction==0:
				for i in range(x,x+key):
					self.player2_matrix[i][y]=key
		print ("heyy")
		print (self.player1_matrix)
		print (self.player2_matrix)
	
	def player1_chance(self):
		self.player1.send("attack")
		self.player2.send("wait")
		print ("me0.1")
		self.player1_attack=self.player1.recv(BUFFER)
		print ("me0.2")
		self.player1_coord=self.player1_attack.split(",")
		self.player1_x=self.player1_coord[0]
		self.player1_y=self.player1_coord[1]
		check=self.evaluate_hit_miss("1")
		return check
			
	def player2_chance(self):
		self.player2.send("attack")
		self.player1.send("wait")
		self.player2_attack=self.player2.recv(BUFFER)
		self.player2_coord=self.player2_attack.split(",")
		self.player2_x=self.player2_coord[0]
		self.player2_y=self.player2_coord[1]
		check=self.evaluate_hit_miss("2")
		return check
	
	def attacking_position(self):
		print ("me")
		self.player1_score=0
		self.player2_score=0
		self.flag=0
		
		while (self.flag==0):
			print ("me0")
			self.player1_check=self.player1_chance()
			print ("me1")
			while self.player1_check=='hit':
				print ("me2")
				if self.player1_score==15:
					print ("Player1 won..Player 2 loose")
					self.player1.send("win")
					self.player2.send("lose")
					return
				self.player1_check=self.player1_chance()
			while self.player1_check=='miss':
				self.player2_check=self.player2_chance()
			while self.player2_check=='hit':
				if self.player2_score==15:
					print ("Player2 won..Player 1 loose")
					self.player2.send("win")
					self.player1.send("lose")
					return
				self.player2_check=self.player2_chance()
			while self.player2_check=='miss':
				self.player1_check=self.player1_chance()
			
		
				
			
			
			
		
	
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
		
	