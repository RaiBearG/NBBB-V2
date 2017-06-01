from Tkinter import *

root = Tk()

root.title('Boat Tracker v1.1')

#added NBBB logo 
logo = PhotoImage(file="NBBB_Logo.gif")
Label(root, image=logo).grid(row=0, sticky=W)


#Left frame for all input parameters except communication 

params = Frame(root, bd=2, relief=SUNKEN)
params.grid(row=1,sticky=W)


Label(params, text='Input Parameters').pack()

#fetch height of unit on boat in feet
Label(params, text='Height of GPS in ft').pack()
Height = Entry(params)
Height.pack()
Height.focus_set()
def getheight():
	print Height.get()
save_height = Button(params, text="SAVE", width=12, command=getheight)
save_height.pack()

# fetch horizontal position on boat
Label(params, text='Distance from middle in ft (left = -ve)').pack()
Dist = Entry(params)
Dist.pack()
Dist.focus_set()
def getdist():
	print Dist.get()
save_dist = Button(params, text="SAVE", width=12, command=getdist)
save_dist.pack()


# calibrate initial offset
Label(params, text='Initial offset in ft').pack()
Offset = Entry(params)
Offset.pack()
Offset.focus_set()
def getoffset():
	print Offset.get()
save_offset = Button(params, text="SAVE", width=12, command=getoffset)
save_offset.pack()






root.mainloop()
