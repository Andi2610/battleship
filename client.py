import Tkinter as tk
from Tkinter import *

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
buttons_player=[]
buttons_enemy=[]
label = Label(root, text='Your Board',font=("Times", "24", "bold italic"),background='#000000',fg='#ffffff',bd=0)
label.place(x=100, y=120)
label1 = Label(root, text='Enemy\'s Board',font=("Times", "24", "bold italic"),background='#000000',fg='#ffffff',bd=0)
label1.place(x=950, y=120)

ready = Button(root,text='Ready',font=("Helvetica", "16"),bd=0,padx=10,pady=10).place(x =575,y=150)
horizontal = Button(root,text='Horizontal',font=("Helvetica", "16"),padx=10,pady=10).place(x =575,y=300)
vertical = Button(root,text='Vertical',font=("Helvetica", "16"),padx=10,pady=10).place(x =575,y=450)
ship_color = Button(root,text=' ',width=5,height=2,background='turquoise',padx=10,pady=10).place(x =150,y=600)
ship_color_label = Label(root,text='Ship\'s color',font=("Helvetica", "16"),background='#000000',fg='#ffffff',bd=0).place(x =230,y=620)
hit_color = Button(root,text=' ',width=5,height=2,background='red',padx=10,pady=10).place(x =400,y=600)
hit_color_label = Label(root,text='Hit\'s color',font=("Helvetica", "16"),background='#000000',fg='#ffffff',bd=0).place(x =480,y=620)
miss_color = Button(root,text=' ',width=5,height=2,background='white',padx=10,pady=10).place(x =650,y=600)
miss_color_label = Label(root,text='Miss\'s color',font=("Helvetica", "16"),background='#000000',fg='#ffffff',bd=0).place(x =720,y=620)

for x in range(10):
    temp_buttons = []
    for y in range(10):
        b = tk.Button(board1, bd=1, text=" ", height=2, width=5,background='#00ace6')
        b.grid(row=x, column=y)
        temp_buttons.append(b)
    buttons_player.append(temp_buttons)

for x in range(10):
    temp_buttons = []
    for y in range(10):
        b = tk.Button(board2, bd=1, text=" ", height=2, width=5,background='#00ace6')
        b.grid(row=x, column=y)
        temp_buttons.append(b)
    buttons_enemy.append(temp_buttons)

root.mainloop()
