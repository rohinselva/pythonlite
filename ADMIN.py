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
        self.title("Online Travels management")
        self.adminHome()
        self.mainloop()

    def adminHome(self):
        self.clear()
        B1=Button(self,text="VEHICLE",command= self.Movies)
        B1.pack()
        B2=Button(self,text="CITY",command=self.Screens)
        B2.pack()
        B3=Button(self,text="BOOKING",command=self.Shows)
        B3.pack()
        B4=Button(self,text='LOGOUT',command=self.logout)
        B4.pack()

    def Movies(self):
        self.clear()
        B=Button(self,text='Back',command=self.adminHome)
        B.grid()
        L=Label(self,text = '--VEHICLE--')
        L.grid()
        L1=Label(self,text = 'VehicleID : ')
        L1.grid(row=2,sticky="W")
        E1=Entry(self)
        E1.grid(row=2,sticky="E")
        B1=Button(self,text="Remove VEHICLE",command= lambda:self.removeMovie(E1.get()))
        B1.grid()
        L3=Label(self,text = "VehicleID : ")
        L3.grid(row=5,sticky="W")
        E3=Entry(self)
        E3.grid(row=5,sticky="E")
        L4=Label(self,text = "VehicleName : ")
        L4.grid(row=6,sticky="W")
        E4=Entry(self)
        E4.grid(row=6,sticky="E")
        L5=Label(self,text = "VehicleType : ")
        L5.grid(row=7,sticky="W")
        E5=Entry(self)
        E5.grid(row=7,sticky="E")
        L6=Label(self,text = "Arrival : ")
        L6.grid(row=8,sticky="W")
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        E6=Entry(self,validate='key',validatecommand=vcmd)
        E6.grid(row=8,sticky="E")
        B2=Button(self,text="Add Vehicle",command=lambda: self.addMovie(E3.get(),E4.get(),E5.get(),E6.get()))
        B2.grid(row=9,sticky="W")
        B3=Button(self,text="Edit Vehicle",command=lambda: self.editMovie(E3.get(),E4.get(),E5.get(),E6.get()))
        B3.grid(row=9,sticky="E")

        L2=Label(self,text ='--Vehicle List--')
        L2.grid()
        conn = sqlite3.connect('database.db')
        tickets=conn.execute('SELECT movieid,moviename,director,duration FROM movies ORDER BY moviename')
        msg='VehicleID'+'\tVehicleName'+'\tType'+'\tArrival'
        M=Label( self, text=msg,relief = RAISED )
        M.grid(sticky="W")
        for row in tickets:
            msg=str(row[0])+'\t'+str(row[1])+'\t\t'+str(row[2])+'\t'+str(row[3])
            M=Label( self, text=msg )
            M.grid(sticky="W")
        conn.close()

    def removeMovie(self,movieID):
        conn = sqlite3.connect('database.db')
        conn.execute("DELETE FROM movies WHERE movieid LIKE ?;",[movieID])
        conn.execute("DELETE FROM shows WHERE movieid LIKE ?;",[movieID])
        messagebox.showinfo('done',"Vehicles and Bookings Removed!")
        conn.commit()
        conn.close()
        self.Movies()

    def editMovie(self,movieID,movieName,director,duration):
        conn = sqlite3.connect('database.db')
        conn.execute("UPDATE movies SET moviename=?,director=?,duration=? WHERE movieID LIKE ?;",[movieName,director,duration,movieID])
        messagebox.showinfo('done',"Vehicles Details Updated!")
        conn.commit()
        conn.close()
        self.Movies()

    def addMovie(self,movieID,movieName,director,duration):
        conn = sqlite3.connect('database.db')
        try:
            conn.execute("INSERT INTO movies VALUES (?,?,?,?);",[movieID,movieName,director,duration])
        except :
            messagebox.showinfo('error','VehicleID Already Exists!')
        else:
            messagebox.showinfo('done',"Vehicle Added!")
            conn.commit()
            self.Movies()
        conn.close()

    def Screens(self):
        self.clear()
        B=Button(self,text='Back',command=self.adminHome)
        B.grid()
        L=Label(self,text = '--City--')
        L.grid()
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        L1=Label(self,text = 'CityNum : ')
        L1.grid(row=2,sticky="W")
        E1=Entry(self)
        E1.grid(row=2,sticky="E")
        B1=Button(self,text="Remove City",command= lambda:self.removeScreen(E1.get()))
        B1.grid()
        L3=Label(self,text = "CityNum : ")
        L3.grid(row=5,sticky="W")
        E3=Entry(self,validate='key',validatecommand=vcmd)
        E3.grid(row=5,sticky="E")
        L4=Label(self,text = "Branch : ")
        L4.grid(row=6,sticky="W")
        E4=Entry(self,validate='key',validatecommand=vcmd)
        E4.grid(row=6,sticky="E")
        L5=Label(self,text = "Availablity : ")
        L5.grid(row=7,sticky="W")
        E5=Entry(self,validate='key',validatecommand=vcmd)
        E5.grid(row=7,sticky="E")
        B2=Button(self,text="Add City",command=lambda: self.addScreen(E3.get(),E4.get(),E5.get()))
        B2.grid()
        L2=Label(self,text ='--City List--')
        L2.grid()
        conn = sqlite3.connect('database.db')
        tickets=conn.execute('SELECT screennum,floor,capacity FROM screen ORDER BY screennum')
        msg='CityNum'+'\tBranch'+'\tAvailability'
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
        messagebox.showinfo('done',"City Removed!")
        conn.commit()
        conn.close()
        self.Screens()

    def addScreen(self,screenNum,floor,capacity):
        conn = sqlite3.connect('database.db')
        try:
            conn.execute("INSERT INTO screen VALUES (?,?,?);",[screenNum,floor,capacity])
        except :
            messagebox.showinfo('error','CityNum Already Exists!')
        else:
            messagebox.showinfo('done',"City Added!")
            conn.commit()
            self.Screens()
        conn.close()
        

    def Shows(self):
        self.clear()
        B=Button(self,text='Back',command=self.adminHome)
        B.grid()
        L=Label(self,text = '--Bookings--')
        L.grid()
        L1=Label(self,text = 'BookingID : ')
        L1.grid(row=2,sticky="W")
        E1=Entry(self)
        E1.grid(row=2,sticky="E")
        B1=Button(self,text="Remove Booking",command= lambda:self.removeShow(E1.get()))
        B1.grid()
        L3=Label(self,text = "BookingID : ")
        L3.grid(row=5,sticky="W")
        E3=Entry(self)
        E3.grid(row=5,sticky="E")
        L4=Label(self,text = "VehicleID : ")
        L4.grid(row=6,sticky="W")
        E4=Entry(self)
        E4.grid(row=6,sticky="E")
        L5=Label(self,text = "Session : ")
        L5.grid(row=7,sticky="W")
        E5=Entry(self)
        E5.grid(row=7,sticky="E")
        L6=Label(self,text = "CityNum : ")
        L6.grid(row=8,sticky="W")
        vcmd = (self.register(self.onValidate),'%d','%i','%P','%s','%S','%v','%V','%W')
        E6=Entry(self,validate='key',validatecommand=vcmd)
        E6.grid(row=8,sticky="E")
        B2=Button(self,text="Add Booking",command=lambda: self.addShow(E3.get(),E4.get(),E5.get(),E6.get()))
        B2.grid(row=9)
        L2=Label(self,text ='--Bookings List--')
        L2.grid()
        conn = sqlite3.connect('database.db')
        tickets=conn.execute('''SELECT showid,moviename,showtime,screenno,ava_seats FROM shows
            INNER JOIN movies ON movies.movieid=shows.movieid
            ORDER BY moviename''')
        msg='BookingID'+'\tVehcileName'+'\tSession'+'\tCity'+'\tAvailableSeats'
        M=Label( self, text=msg,relief = RAISED )
        M.grid(sticky="W")
        for row in tickets:
            msg=str(row[0])+'\t\t'+str(row[1])+'\t\t'+str(row[2])+'\t'+str(row[3])+'\t'+str(row[4])
            M=Label( self, text=msg )
            M.grid(sticky="W")
        conn.close()

    def removeShow(self,showID):
        conn = sqlite3.connect('database.db')
        conn.execute("DELETE FROM shows WHERE showid LIKE ?;",[showID])
        messagebox.showinfo('done',"Booking Removed!")
        conn.commit()
        conn.close()
        self.Shows()

    def addShow(self,showID,movieID,showTime,screenNum):
        conn = sqlite3.connect('database.db')
        obj=conn.execute("SELECT capacity FROM screen WHERE screennum=?",[screenNum])
        capacity=obj.fetchone()
        if capacity is None:
            messagebox.showinfo('error','Invalid City!')
        else:
            capacity=capacity[0]
            try:
                conn.execute("INSERT INTO shows VALUES (?,?,?,?,?);",[showID,movieID,showTime,screenNum,capacity])
            except:
                messagebox.showinfo('error','BookingID Already Exists!')
            else:
                messagebox.showinfo('done',"Booking Added!")
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

