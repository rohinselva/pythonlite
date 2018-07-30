import sqlite3
from tkinter import *
from tkinter import messagebox

class User(Tk):

    def start(self):
        self.title("Online Travel Booking")
        self.login()
        self.mainloop()

    def login(self):
        self.clear()
        LL=Label(self,text = "--Login--")
        LL.grid(columnspan=2)
        L1=Label(self,text = "User Name : ")
        L1.grid(row=1,column=0)
        E1=Entry(self)
        E1.grid(row=1,column=1)
        L2=Label(self,text = "Password : ")
        L2.grid(row=2,column=0)
        E2=Entry(self,show='*')
        E2.grid(row=2,column=1)
        B1=Button(self,text="Login",command = lambda: self.validateLogin(E1.get(),E2.get()))
        B1.grid(columnspan=2)
        LR=Label(self,text = "--Register--")
        LR.grid(columnspan=2)
        L3=Label(self,text = "Name : ")
        L3.grid(row=5,column=0)
        E3=Entry(self)
        E3.grid(row=5,column=1)
        L4=Label(self,text = "User Name : ")
        L4.grid(row=6,column=0)
        E4=Entry(self)
        E4.grid(row=6,column=1)
        L5=Label(self,text = "Password : ")
        L5.grid(row=7,column=0)
        E5=Entry(self,show='*')
        E5.grid(row=7,column=1)
        L6=Label(self,text = "Mobile Number : ")
        L6.grid(row=8,column=0)
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        E6=Entry(self,validate='key',validatecommand=vcmd)
        E6.grid(row=8,column=1)
        B2=Button(self,text="Register",command=lambda: self.registerUser(E3.get(),E4.get(),E5.get(),E6.get()))
        B2.grid(columnspan=2)

    def validateLogin(self,username,password):
        conn = sqlite3.connect('database.db')
        obs = conn.execute("SELECT password FROM users WHERE username LIKE ?",[username])
        dbpass = obs.fetchone()
        if dbpass is None :
            messagebox.showinfo('error',"Username Not Registered!")
        elif password == dbpass[0]:
            self.userHome(username)
        else:
            messagebox.showinfo('error',"Invalid Username or Password!")
        conn.close()

    def registerUser(self,name,username,password,mblenum):
        conn = sqlite3.connect('database.db')
        try:
            conn.execute("INSERT INTO users VALUES (?,?,?,?);",[name,username,password,mblenum])
        except :
            messagebox.showinfo('error','UserName Already Exists!')
        else:
            messagebox.showinfo('done',"Registration Successfull")
        conn.commit()
        conn.close()

    def userHome(self,user):
        self.clear()
        L=Label(self,text = "Hello "+user)
        L.pack()
        B1=Button(self,text="View Profile",command=lambda: self.viewProfile(user))
        B1.pack()
        B2=Button(self,text="Book Vehicle",command=lambda: self.viewMovies(user))
        B2.pack()
        B3=Button(self,text="Show Bookings",command=lambda: self.showTickets(user))
        B3.pack()
        B4=Button(self,text='Logout',command=lambda:self.login())
        B4.pack()

    def viewMovies(self,user):
        self.clear()
        B1=Button(self,text='Back',command=lambda:self.userHome(user))
        B1.pack()
        L=Label(self,text="--Vehicle--")
        L.pack()
        conn = sqlite3.connect('database.db')
        movies=conn.execute("SELECT movieid, moviename,director, duration FROM movies")
        lb = Listbox(self)
        movielist=[]
        for row in movies:
            movielist.append(row)
            lb.insert("end", row[1])
        lb.pack()
        conn.close()
        B2=Button(self,text='Next',command=lambda:self.viewShows(user,movielist,lb.curselection()[0]))
        B2.pack()
        
    def viewShows(self,user,movielist,opt):
        self.clear()
        B1=Button(self,text='Back',command=lambda:self.viewMovies(user))
        B1.pack()
        L1=Label(self,text='Vehicle name : '+movielist[opt][1])
        L1.pack()
        L2=Label(self,text='Type By '+movielist[opt][2])
        L2.pack()
        L3=Label(self,text='Arrival : '+str(movielist[opt][3]))
        L3.pack
        L=Label(self,text="--Booking--")
        L.pack()
        conn = sqlite3.connect('database.db')
        shows=conn.execute("SELECT showid, showtime,ava_seats FROM shows WHERE movieid LIKE ?",[movielist[opt][0]])
        lb = Listbox(self)
        showlist=[]
        for row in shows:
            showlist.append(row)
            lb.insert("end", row[1])
        lb.pack()
        conn.close()
        B2=Button(self,text='Next',command=lambda:self.bookShow(user,showlist,lb.curselection()[0],movielist[opt][1]))
        B2.pack() 

    def bookShow(self,user,showlist,opt,moviename):
        self.clear()
        L1=Label(self, text='Vehicle : '+moviename)
        L1.grid(columnspan=2)
        L2=Label(self,text='Booking : '+showlist[opt][1])
        L2.grid(columnspan=2)
        L3=Label(self,text='Seats Available :'+str(showlist[opt][2]))
        L3.grid(columnspan=2)
        var=StringVar(self)
        var.set(1)
        choices=[1,2,3,4,5,6,7,8]
        L4=Label(self,text='Select Vehicle : ')
        L4.grid(row=4,column=0)
        O=OptionMenu(self,var,*choices)
        O.grid(row=4,column=1)
        B1=Button(self,text='Confirm & Book',command=lambda:self.book(user,showlist[opt][0],var.get()))
        B1.grid(row=5,column=0)
        B2=Button(self,text='Cancel',command=lambda:self.userHome(user))
        B2.grid(row=5,column=1)

    def book(self,user,showid,seats):
        conn = sqlite3.connect('database.db')
        obj=conn.execute("SELECT max(ticketid) FROM tickets")
        ticketid=obj.fetchone()[0]
        if ticketid is None:
            ticketid=1001
        else:
            ticketid=ticketid+1
        try:
            conn.execute("UPDATE shows SET ava_seats=ava_seats-? WHERE showid LIKE ?;",[seats,showid])
            conn.execute("INSERT INTO tickets VALUES (?,?,?,?);",[ticketid,user,showid,seats])
        except Exception as ex:
            messagebox.showinfo('error','Seats Unavailable!')
        else:
            messagebox.showinfo('done',"Booking Successfull")
        conn.commit()
        conn.close()
        self.userHome(user)

    def showTickets(self,user):
        self.clear()
        L=Label(self,text = "Hello "+user)
        L.pack()
        conn = sqlite3.connect('database.db')
        tickets=conn.execute('''SELECT ticketid,moviename,showtime,screenno,seats FROM((tickets
                        LEFT OUTER JOIN shows ON shows.showid=tickets.showid)
                        LEFT OUTER JOIN movies ON movies.movieid=shows.movieid)
                        WHERE tickets.username=?;''',[user])
        L2=Label(self,text="--Bookings--")
        L2.pack()
        for row in tickets:
            msg='Booking ID : '+str(row[0])+'\n'+str(row[1])+'\n'+str(row[2])+'\nBranch '+str(row[3])+'\nSeats : '+str(row[4])
            M=Message( self, text=msg,relief = RAISED )
            M.pack()
        conn.close()
        B=Button(self,text='Back',command=lambda:self.userHome(user))
        B.pack()

    def viewProfile(self,user):
        self.clear()
        conn = sqlite3.connect('database.db')
        obj=conn.execute('SELECT name, password, mobilenum FROM users WHERE username like ? ;',[user])
        profile=obj.fetchone()
        L=Label(self,text = "--Profile--")
        L.grid(columnspan=2)
        L1=Label(self,text = "Name : ")
        L1.grid(row=1,column=0)
        E1=Entry(self)
        E1.insert(END,profile[0])
        E1.grid(row=1,column=1)
        L2=Label(self,text = "User Name : ")
        L2.grid(row=2,column=0)
        v=StringVar(self,value=user)
        E2=Entry(self,textvariable=v,state=DISABLED )
        E2.grid(row=2,column=1)
        L3=Label(self,text = "Password : ")
        L3.grid(row=3,column=0)
        E3=Entry(self,show='*')
        E3.insert(END,profile[1])
        E3.grid(row=3,column=1)
        L4=Label(self,text = "Mobile Number : ")
        L4.grid(row=4,column=0)
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        E4=Entry(self,validate='key',validatecommand=vcmd)
        E4.insert(END,profile[2])
        E4.grid(row=4,column=1)
        B2=Button(self,text="Update Profile",command=lambda: self.updateProfile(user,E1.get(),E3.get(),E4.get()))
        B2.grid(columnspan=2)
        B1=Button(self,text='Cancel',command=lambda:self.userHome(user))
        B1.grid(columnspan=2)

    def updateProfile(self,username,name,password,mblenum):
        conn = sqlite3.connect('database.db')
        conn.execute("UPDATE users SET name=?,password=?,mobilenum=? WHERE username LIKE ?;",[name,password,mblenum,username])
        messagebox.showinfo('done',"Profile Updated!")
        conn.commit()
        conn.close()

    def onValidate(self,  d, i, P, s, S, v, V, W):
        try:
            int(P)
        except ValueError:
            return False
        else:
            return True

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        
u=User()
u.start()
