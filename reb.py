import sqlite3
import os
DRPASS = '1234'
print('-----Database Reboot------')
pas=input('Password : ')
if pas==DRPASS:
    print('Rebooting Database Will Delete existing Database...')
    ch=input('Do you wish to continue ? (Y) :')
    if ch=='Y':
        try:
             print('Deleting Existing Database...')
             os.remove("database.db")
             print('Database Deletion Successful!')
        except:
            pass
        print('Creating new Database...')
        conn = sqlite3.connect('database.db')
        print('Database Creation Successful!')
        print('Creating Tables...')
        conn.execute('''CREATE TABLE users
                 (name TEXT NOT NULL,
                 username TEXT PRIMARY KEY NOT NULL,
                 password TEXT NOT NULL,
                 mobilenum NUMBER NOT NULL);''')
        print('Created Users Table...') 
        conn.execute('''CREATE TABLE movies
                (movieid TEXT PRIMARY KEY NOT NULL,
                moviename TEXT NOT NULL,
                director TEXT NOT NULL,
                duration NUMBER NOT NULL);''')
        print('Created Vehicles Table...')
        conn.execute('''CREATE TABLE screen
                (screennum NUMBER PRIMARY KEY NOT NULL,
                floor NUMBER NOT NULL,
                capacity NUMBER NOT NULL,
                CHECK (capacity>0));''')
        print('Created City Table...')
        conn.execute('''CREATE TABLE shows
                (showid TEXT PRIMARY KEY NOT NULL,
                movieid TEXT NOT NULL,
                showtime DATETIME NOT NULL,
                screenno NUMBER NOT NULL,
                ava_seats NUMBER NOT NULL,
                CHECK (ava_seats>=0));''')
        print('Created Booking Table...') 
        conn.execute('''CREATE TABLE tickets
                (ticketid NUMBER PRIMARY KEY NOT NULL,
                username TEXT NOT NULL,
                showid TEXT NOT NULL,
                seats NUMBER NOT NULL);''')
        print('Created Tables Table...')
        print('Table Creation Successful!') 
        conn.commit()
        conn.close()
    else:
        print('Exiting!')
else:
    print('Access Denied!')
os.system("pause")

# Admin.py

import sqlite3
from tkinter import *
from tkinter import messagebox

def login():
    username=input('Enter Admin Username : ')
    password=input('Enter Password : ')
    if username=='Admin' and password=='password':
        print('Access Granted')
        a=Admin()
        a.start()
    else :
        print('Access Denied')

class Admin(Tk):

    def start(self):
        self.title("Online Movie Ticket Booking")
        self.adminHome()
        self.mainloop()

    def adminHome(self):
        self.clear()
        B1=Button(self,text="Movies",command= self.Movies)
        B1.pack()
        B2=Button(self,text="Screens",command=self.Screens)
        B2.pack()
        B3=Button(self,text="Shows",command=self.Shows)
        B3.pack()
        B4=Button(self,text='Logout',command=self.logout)
        B4.pack()

    def Movies(self):
        self.clear()
        B=Button(self,text='Back',command=self.adminHome)
        B.grid()
        L=Label(self,text = '--Movies--')
        L.grid()
        L1=Label(self,text = 'MovieID : ')
        L1.grid(row=2,sticky="W")
        E1=Entry(self)
        E1.grid(row=2,sticky="E")
        B1=Button(self,text="Remove Movie",command= lambda:self.removeMovie(E1.get()))
        B1.grid()
        L3=Label(self,text = "MovieID : ")
        L3.grid(row=5,sticky="W")
        E3=Entry(self)
        E3.grid(row=5,sticky="E")
        L4=Label(self,text = "MovieName : ")
        L4.grid(row=6,sticky="W")
        E4=Entry(self)
        E4.grid(row=6,sticky="E")
        L5=Label(self,text = "Director : ")
        L5.grid(row=7,sticky="W")
        E5=Entry(self)
        E5.grid(row=7,sticky="E")
        L6=Label(self,text = "Duration : ")
        L6.grid(row=8,sticky="W")
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        E6=Entry(self,validate='key',validatecommand=vcmd)
        E6.grid(row=8,sticky="E")
        B2=Button(self,text="Add Movie",command=lambda: self.addMovie ( E3.get(), E4.get(),  E5.get(),  E6.get() ))
        B2.grid(row=9,sticky="W")
        B3=Button(self,text="Edit Movie",command=lambda: self.editMovie(E3.get(),E4.get(), E5.get(), E6.get()))
        B3.grid(row=9,sticky="E")
        L2=Label(self,text ='--Movie List--')
        L2.grid()
        conn = sqlite3.connect('database.db')
        tickets=conn.execute('SELECT movieid,moviename,director,duration FROM movies ORDER BY moviename')
        msg='MovieID'+'\tMovieName'+'\tDirector'+'\t\tDuration'
        M=Label( self, text=msg,relief = RAISED )
        M.grid(sticky="W")
        for row in tickets:
            msg=str(row[0])+'\t'+str(row[1])+'\t'+str(row[2])+'\t'+str(row[3])
            M=Label( self, text=msg )
            M.grid(sticky="W")
        conn.close()

    def removeMovie(self,movieID):
        conn = sqlite3.connect('database.db')
        conn.execute("DELETE FROM movies WHERE movieid LIKE ?;",[movieID])
        conn.execute("DELETE FROM shows WHERE movieid LIKE ?;",[movieID])
        messagebox.showinfo('done',"Movie and Shows Removed!")
        conn.commit()
        conn.close()
        self.Movies()

    def editMovie(self,movieID,movieName,director,duration):
        conn = sqlite3.connect('database.db')
        conn.execute("UPDATE movies SET moviename=?,director=?,duration=? WHERE movieID LIKE ?;", [ movieName, director, duration, movieID])
        messagebox.showinfo('done',"Movie Details Updated!")
        conn.commit()
        conn.close()
        self.Movies()

    def addMovie(self,movieID,movieName,director,duration):
        conn = sqlite3.connect('database.db')
        try:
            conn.execute("INSERT INTO movies VALUES (?,?,?,?);",[movieID,movieName,director,duration])
        except :
            messagebox.showinfo('error','MovieID Already Exists!')
        else:
            messagebox.showinfo('done',"Movie Added!")
            conn.commit()
            self.Movies()
        conn.close()

    def Screens(self):
        self.clear()
        B=Button(self,text='Back',command=self.adminHome)
        B.grid()
        L=Label(self,text = '--Screen--')
        L.grid()
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        L1=Label(self,text = 'ScreenNum : ')
        L1.grid(row=2,sticky="W")
        E1=Entry(self)
        E1.grid(row=2,sticky="E")
        B1=Button(self,text="Remove Screen",command= lambda:self.removeScreen(E1.get()))
        B1.grid()
        L3=Label(self,text = "ScreenNum : ")
        L3.grid(row=5,sticky="W")
        E3=Entry(self,validate='key',validatecommand=vcmd)
        E3.grid(row=5,sticky="E")
        L4=Label(self,text = "Floor : ")
        L4.grid(row=6,sticky="W")
        E4=Entry(self,validate='key',validatecommand=vcmd)
        E4.grid(row=6,sticky="E")
        L5=Label(self,text = "Capacity : ")
        L5.grid(row=7,sticky="W")
        E5=Entry(self,validate='key',validatecommand=vcmd)
        E5.grid(row=7,sticky="E")
        B2=Button(self,text="Add Screen",command=lambda: self.addScreen(E3.get(),E4.get(),E5.get()))
        B2.grid()
        L2=Label(self,text ='--Screen List--')
        L2.grid()
        conn = sqlite3.connect('database.db')
        tickets=conn.execute('SELECT screennum,floor,capacity FROM screen ORDER BY screennum')
        msg='ScreenNum'+'\tFloor'+'\tCapacity'
        M=Label( self, text=msg,relief = RAISED )
        M.grid(sticky="W")
        for row in tickets:
            msg=str(row[0])+'\t\t'+str(row[1])+'\t'+str(row[2])
            M=Label( self, text=msg )
            M.grid(sticky="W")
        conn.close()

    def removeScreen(self,screenNum):
        conn = sqlite3.connect('database.db')
        conn.execute("DELETE FROM screen WHERE screennum LIKE ?;",[screenNum])
        messagebox.showinfo('done',"Screen Removed!")
        conn.commit()
        conn.close()
        self.Screens()

    def addScreen(self,screenNum,floor,capacity):
        conn = sqlite3.connect('database.db')
        try:
            conn.execute("INSERT INTO screen VALUES (?,?,?);",[screenNum,floor,capacity])
        except :
            messagebox.showinfo('error','ScreenNum Already Exists!')
        else:
            messagebox.showinfo('done',"Screen Added!")
            conn.commit()
            self.Screens()
        conn.close()

    def Shows(self):
        self.clear()
        B=Button(self,text='Back',command=self.adminHome)
        B.grid()
        L=Label(self,text = '--Shows--')
        L.grid()
        L1=Label(self,text = 'ShowID : ')
        L1.grid(row=2,sticky="W")
        E1=Entry(self)
        E1.grid(row=2,sticky="E")
        B1=Button(self,text="Remove Show",command= lambda:self.removeShow(E1.get()))
        B1.grid()
        L3=Label(self,text = "ShowID : ")
        L3.grid(row=5,sticky="W")
        E3=Entry(self)
        E3.grid(row=5,sticky="E")
        L4=Label(self,text = "MovieID : ")
        L4.grid(row=6,sticky="W")
        E4=Entry(self)
        E4.grid(row=6,sticky="E")
        L5=Label(self,text = "Date & Time : ")
        L5.grid(row=7,sticky="W")
        E5=Entry(self)
        E5.grid(row=7,sticky="E")
        L6=Label(self,text = "ScreenNum : ")
        L6.grid(row=8,sticky="W")
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        E6=Entry(self,validate='key',validatecommand=vcmd)
        E6.grid(row=8,sticky="E")
        B2=Button(self,text="Add Show",command=lambda: self.addShow(E3.get(),E4.get(),E5.get(),E6.get()))
        B2.grid(row=9)
        L2=Label(self,text ='--Show List--')
        L2.grid()
        conn = sqlite3.connect('database.db')
        tickets=conn.execute('''SELECT showid,moviename,showtime,screenno,ava_seats FROM shows
            INNER JOIN movies ON movies.movieid=shows.movieid
            ORDER BY moviename''')
        msg='ShowID'+'\tMovieName'+'\tShowTime'+'\tScreen'+'\tAvailableSeats'
        M=Label( self, text=msg,relief = RAISED )
        M.grid(sticky="W")
        for row in tickets:
            msg=str(row[0])+'\t'+str(row[1])+'\t'+str(row[2])+'\t'+str(row[3])+'\t'+str(row[4])
            M=Label( self, text=msg )
            M.grid(sticky="W")
        conn.close()

    def removeShow(self,showID):
        conn = sqlite3.connect('database.db')
        conn.execute("DELETE FROM shows WHERE showid LIKE ?;",[showID])
        messagebox.showinfo('done',"Show Removed!")
        conn.commit()
        conn.close()
        self.Shows()

    def addShow(self,showID,movieID,showTime,screenNum):
        conn = sqlite3.connect('database.db')
        obj=conn.execute("SELECT capacity FROM screen WHERE screennum=?",[screenNum])
        capacity=obj.fetchone()
        if capacity is None:
            messagebox.showinfo('error','Invalid Screen!')
        else:
            capacity=capacity[0]
            try:
                conn.execute("INSERT INTO shows VALUES (?,?,?,?,?);",[showID, movieID, showTime, screenNum, capacity])
            except:
                messagebox.showinfo('error','ShowID Already Exists!')
            else:
                messagebox.showinfo('done',"Show Added!")
                conn.commit()
                self.Shows()
        conn.close()

    def logout(self):
        self.destroy()
        login()
        
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
                
login()
