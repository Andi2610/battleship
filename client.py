import Tkinter as tk
from Tkinter import *
import socket
import threading

class Client:
    
    global host
    global port
    global player_status
    global BUFFER
    global horizontal_flag
    global vertical_flag
    global ship_size
    global ship_positions
    global status_flag
    global attack_flag

    horizontal_flag=False
    vertical_flag=False
    status_flag=True
    attack_flag = False
    ship_positions=dict()
    
    def connectServer(self):
        global clientsocket
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect((host,port))
            print ("Connected to Server")
            status_label.configure(text='Waiting for other player...')
            player_status=clientsocket.recv(BUFFER)
            print (player_status)
            self.enable_player_grid()
            self.enable_ready()
            self.enable_horizontal()
            self.enable_vertical()
            status_label.configure(text='Enter your ship position of ship size 5')

        except:
            print ("error")

    def disable_player_grid(self):
        try:
            for x in range(10):
                for y in range(10):
                    buttons_player[x][y]['state']='disabled'

            print(type(buttons_player[0][0]))
        except:
            pass

    def disable_enemy_grid(self):
        try:
            for x in range(10):
                for y in range(10):
                    buttons_enemy[x][y]['state']='disabled'
        except:
            pass
    def disable_ready(self):
        ready['state']='disabled'

    def disable_horizontal(self):
        horizontal['state']='disabled'
        
    def disable_vertical(self):
        vertical['state']='disabled'

    def enable_player_grid(self):
        try:
            for x in range(10):
                for y in range(10):
                    buttons_player[x][y]['state']='normal'

            print(type(buttons_player[0][0]))
        except:
            pass

    def enable_enemy_grid(self):
        try:
            for x in range(10):
                for y in range(10):
                    buttons_enemy[x][y]['state']='normal'
        except:
            pass
    def enable_ready(self):
        ready['state']='normal'

    def enable_horizontal(self):
        horizontal['state']='normal'
        
    def enable_vertical(self):
        vertical['state']='normal'

    def set_horizontal(self):
        global horizontal_flag
        global vertical_flag
        horizontal_flag=True
        #print("in horizontal")
        vertical_flag=False

    def set_vertical(self):
        global horizontal_flag
        global vertical_flag
        vertical_flag =True
        horizontal_flag=False

    def send_ship_positions(self,ship_positions):
        global clientsocket
        print(ship_positions)
        clientsocket.sendall(str(ship_positions))
        print("After sending")
        while True:
            msg = clientsocket.recv(BUFFER)
            print(msg)
            self.do_operation(msg)
            if msg == 'win' or msg == 'lose':
                break

    def attack_postions(self,x,y):
        self.x_attack=x
        self.y_attack=y
        global attack_flag
        buttons_enemy[x][y]['background']='black'
        attack_flag = True

    def do_operation(self,msg):
        global clientsocket
        if msg == "attack":
            status_label.configure(text='Enter attacking position on enemy grid')
            self.enable_enemy_grid()
            if attack_flag == True:
                clientsocket.sendall(str(self.x_attack),str(self.y_attack))
                attack_flag=False
                self.disable_enemy_grid()
                status_label.configure(text='Wait..Checking if it is a hit or miss')
            else:
                pass
        elif msg == "wait":
            status_label.configure(text='Wait... it\'s your opponent\'s turn')
        elif msg.startswith('uhit'):
            status_label.configure(text='Wow! it is a hit')
            details = msg.split(",")
            x=int(details[1])
            y=int(details[2])
            your_score=int(details[3])
            enemy_score=int(details[4])
            ship_destroyed = int(details[5])
            if ship_destroyed != 0:
                status_label.configure(text='Enemy\'s ship of size '+ str(ship_destroyed)+ ' is destroyed' )
            buttons_enemy[x][y]['background']='red'
            score_label.configure(text='Your Score :'+" "+str(your_score))
            score_label.configure(text='Enemy\'s Score :'+" "+str(enemy_score))
        elif msg.startswith('umiss'):
            status_label.configure(text='Sad! it is a miss')
            details = msg.split(",")
            x=int(details[1])
            y=int(details[2])
            your_score=int(details[3])
            enemy_score=int(details[4])
            buttons_enemy[x][y]['background']='white'
            score_label.configure(text='Your Score :'+" "+str(your_score))
            score_label.configure(text='Enemy\'s Score :'+" "+str(enemy_score))
        elif msg.startswith('hit'):
            status_label.configure(text='Sad! Your ship is being hit')
            details = msg.split(",")
            x=int(details[1])
            y=int(details[2])
            your_score=int(details[3])
            enemy_score=int(details[4])
            ship_destroyed = int(details[5])
            if ship_destroyed != 0:
                status_label.configure(text='Your ship of size '+ str(ship_destroyed)+ ' is destroyed' )
            buttons_player[x][y]['background']='red'
            score_label.configure(text='Your Score :'+" "+str(your_score))
            score_label.configure(text='Enemy\'s Score :'+" "+str(enemy_score))
        elif msg.startswith('miss'):
            status_label.configure(text='Great! Your opponent missed')
            details = msg.split(",")
            x=int(details[1])
            y=int(details[2])
            your_score=int(details[3])
            enemy_score=int(details[4])
            buttons_player[x][y]['background']='white'
            score_label.configure(text='Your Score :'+" "+str(your_score))
            score_label.configure(text='Enemy\'s Score :'+" "+str(enemy_score))
        elif msg=='win':
            status_label.configure(text='Congratulations!!! You Win')
        else:
            status_label.configure(text='Sorry!! You lose')
            

    def ship_position(self,x,y):
        global ship_size
        global horizontal_flag
        global vertical_flag
        global status_flag
        global status_label
        #print(x)
        if ship_size>0:
            if horizontal_flag==True:
                if y+ship_size<=10:
                    for i in range(y,y+ship_size):
                        if(buttons_player[x][i]['background']=='turquoise'):
                            status_label.configure(text='please select another position as it is acquired')
                            status_flag = False
                            
                    if status_flag==True:
                        for i in range(y,y+ship_size):
                            buttons_player[x][i]['background']='turquoise'
                        ship_positions[ship_size] = [x,y,1]
                        horizontal_flag=False
                        ship_size -= 1
                        if(ship_size==0):
                            self.disable_player_grid()
                            self.disable_horizontal()
                            self.disable_vertical()
                            status_label.configure(text='Wait for a second')
                            self.send_ship_positions(ship_positions)

                        else:
                            status_label.configure(text='Enter your ship position of ship size ' + str(ship_size))
                    else:
                        status_flag=True
                else:
                    status_label.configure(text='please select another position as it won\'t fit')
            elif vertical_flag==True:
                if x+ship_size<=10:
                    for i in range(x,x+ship_size):
                        if(buttons_player[i][y]['background']=='turquoise'):
                            status_label.configure(text='please select another position as it is acquired')
                            status_flag = False

                    if status_flag==True:
                        for i in range(x,x+ship_size):
                            buttons_player[i][y]['background']='turquoise'
                        ship_positions[ship_size] = [x,y,0]
                        vertical_flag=False
                        ship_size-=1
                        if(ship_size==0):
                            self.disable_player_grid()
                            self.disable_horizontal()
                            self.disable_vertical()
                            status_label.configure(text='Wait for a second')
                            self.send_ship_positions(ship_positions)
                        else:
                            status_label.configure(text='Enter your ship position of ship size ' + str(ship_size))
                    else:
                        status_flag=True
                else:
                    status_label.configure(text='please select another position as it won\'t fit')

            else:
                status_label.configure(text='please select horizontal or vertical first')
        else:
            # self.disable_player_grid()
            # self.disable_horizontal()
            # self.disable_vertical()
            # self.send_ship_positions(ship_positions)
            pass


    
if __name__=='__main__':
    
    #connect to server
    host="127.0.0.1"
    port=12345
    BUFFER=4096
    root = tk.Tk()
    root.geometry("1350x750+0+0")
    root.title("Battleship")
    root.configure(background='#000000',padx=25)
    board1 = Frame(root, width=500, height=500, bd=8, relief="raise")
    board1.pack(side=LEFT)
    board1.configure(background='steel blue')
    board2 = Frame(root, width=500, height=500, bd=8, relief="raise")
    board2.pack(side=RIGHT)
    board2.configure(background='steel blue')
    global buttons_player
    global buttons_enemy
    buttons_player=[]
    buttons_enemy=[]
    client=Client()
    label = Label(root, text='Your Board',font=("Times", "24", "bold italic"),background='#000000',fg='#ffffff',bd=0)
    label.place(x=100, y=120)
    label1 = Label(root, text='Enemy\'s Board',font=("Times", "24", "bold italic"),background='#000000',fg='#ffffff',bd=0)
    label1.place(x=950, y=120)
    global ready
    ship_size = 5
    ready = tk.Button(root,text='Ready',font=("Helvetica", "16"),bd=0,padx=10,pady=10)
    ready.place(x =575,y=150)
    #print(type(ready))
    client.disable_ready()
    #ready['state']='disabled'
    global horizontal
    horizontal = Button(root,text='Horizontal',font=("Helvetica", "16"),padx=10,pady=10,command=lambda :client.set_horizontal())
    horizontal.place(x =575,y=300)
    client.disable_horizontal()
    #horizontal['state']='disabled'
    #global vertical
    vertical = Button(root,text='Vertical',font=("Helvetica", "16"),padx=10,pady=10,command=lambda :client.set_vertical())
    vertical.place(x =575,y=450)
    client.disable_vertical()
    #Vertical['state']='disabled'
    ship_color = Button(root,text=' ',width=5,height=2,background='turquoise',padx=10,pady=10).place(x =150,y=600)
    ship_color_label = Label(root,text='Ship\'s color',font=("Helvetica", "16"),background='#000000',fg='#ffffff',bd=0).place(x =230,y=620)
    hit_color = Button(root,text=' ',width=5,height=2,background='red',padx=10,pady=10).place(x =400,y=600)
    hit_color_label = Label(root,text='Hit\'s color',font=("Helvetica", "16"),background='#000000',fg='#ffffff',bd=0).place(x =480,y=620)
    miss_color = Button(root,text=' ',width=5,height=2,background='white',padx=10,pady=10).place(x =650,y=600)
    miss_color_label = Label(root,text='Miss\'s color',font=("Helvetica", "16"),background='#000000',fg='#ffffff',bd=0).place(x =720,y=620)
    global status_label
    status_label = Label(root, text=' ',font=("Helvetica", "18","bold"),background='#000000',fg='#ffffff',bd=0)
    status_label.place(x =480,y=100)
    #status_label.configure(text='qwerty')
    score_label = Label(root, text=' ',font=("Helvetica", "18","bold"),background='#000000',fg='#ffffff',bd=0)
    score_label.place(x=30,y=30)
    enemy_score_label = Label(root, text=' ',font=("Helvetica", "18","bold"),background='#000000',fg='#ffffff',bd=0)
    enemy_score_label.place(x=1100,y=30)
    for x in range(10):
        temp_buttons = []
        for y in range(10):
            b = tk.Button(board1, bd=1, text=" ", height=2, width=5,background='#00ace6',command=lambda x=x, y=y:client.ship_position(x,y))
            b.grid(row=x, column=y)
            temp_buttons.append(b)
        buttons_player.append(temp_buttons)
    
    client.disable_player_grid()

    for x in range(10):
        temp_buttons = []
        for y in range(10):
            b = tk.Button(board2, bd=1, text=" ", height=2, width=5,background='#00ace6',command=lambda x=x, y=y:client.attack_postions(x,y))
            b.grid(row=x, column=y)
            temp_buttons.append(b)
        buttons_enemy.append(temp_buttons)
    client.disable_enemy_grid()
    
    clientthread=threading.Thread(target=client.connectServer)
    clientthread.start()

    root.mainloop()
