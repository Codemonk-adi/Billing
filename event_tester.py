from tkinter import Entry, LabelFrame, Tk

root = Tk()
L = LabelFrame(root,width=500,height=500)
L.pack()
en = Entry(L)
e2 = Entry(L)
en.pack()
e2.pack()
str = """Activate
	
Destroy
	
Map

ButtonPress
	
Enter
	
MapRequest

ButtonRelease
	
Expose
	
Motion

Circulate
	
FocusIn
	
MouseWheel
	
FocusOut
	
Property

Colormap
	
Gravity
	
Reparent

Configure
	
KeyPress

KeyRelease
"""
str = str.replace('\n\t\n',',')
str = str.replace('\n\n',',')
print(str)
for event in str.split(','):
    print(f'<{event}>')
    en.bind(f'<{event}>',lambda e: print(e))
root.mainloop()
