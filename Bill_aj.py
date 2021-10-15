# from re import template
from tkinter import*
from tkinter import messagebox
from pages import page_rest,Page_aj
# -*- coding: utf-8 -*-

        
    
# coding
class Customer():
    def __init__(self):
        self.rate = IntVar()
        self.labour_charge = StringVar()
        self.gst = 0.03

        # variables
        self.cust_name = StringVar()
        self.cust_add = StringVar()
        self.cust_num = StringVar()
        self.curr_date = StringVar()
        self.inv_num = IntVar()
        self.particulars = []

class Billing(object):
    def __init__(self, root):
        self.root = root
        self.root.title("AJ")
        self.title = StringVar()
        # self.root.minsize(width=1, height=720)
        # variables
        self.bg_color = '#f8edeb'
        self.fg_color = '#C70039'
        lbl_color = 'red'
        
        self.title.set('Akash Jewellers')
        
        title = Label(self.root, textvariable=self.title,bd=12,fg=self.fg_color,bg=self.bg_color,font=("Calibri",32 , "bold"),pady=3).pack(fill=X)
        F0 = LabelFrame(text="Firm",font=("Calibri", 12, "bold"), fg="#264653", bg=self.bg_color,
        relief=RAISED)
        F0.pack(fill=X)

        #Navigation
        aj_btn = Button(F0, text="Akash", bg=self.bg_color, fg=self.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED,
        command=self.load_aj)
        abhj_btn = Button(F0, text="Abhushan", bg=self.bg_color, fg=self.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED,
        command=self.load_abj)
        shrj_btn = Button(F0, text="Shringar", bg=self.bg_color, fg=self.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED,
        command=self.load_sj)
        gurj_btn = Button(F0, text="Gurukrupa", bg=self.bg_color, fg=self.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED,
        command=self.load_gj)
        aj_btn.grid(row=0,column=0,padx=10, pady=5)
        abhj_btn.grid(row=0,column=1,padx=10, pady=5)
        shrj_btn.grid(row=0,column=2,padx=10, pady=5)
        gurj_btn.grid(row=0,column=3,padx=10, pady=5)
        F1 = Frame(self.root)
        F1.pack(fill='both',expand=True)
        #Akash Jewellers
        self.FAJ = Page_aj()
        self.FAJ.place(in_=F1,x=0,y=0,relwidth=1,relheight=1)
        self.FABH = page_rest(0)
        self.FABH.place(in_=F1,x=0,y=0,relwidth=1,relheight=1)
        self.FSHR = page_rest(1)
        self.FSHR.place(in_=F1,x=0,y=0,relwidth=1,relheight=1)
        self.FGUR = page_rest(2)
        self.FGUR.place(in_=F1,x=0,y=0,relwidth=1,relheight=1)
        self.FAJ.show()
        
        
    def load_aj(self):
        self.title.set("Akash Jewellers")
        self.FAJ.show()
        return
    
    def load_abj(self):
        self.title.set("Abhushan Jewellers")
        self.FABH.show()
        return
    
    def load_sj(self):
        self.title.set("Shringar Jewellers")
        self.FSHR.show()
        return
    
    def load_gj(self):
        self.title.set("Gurukrupa Jewellers")
        self.FGUR.show()
        return
    

root = Tk()
root.iconbitmap(default='Bill_aj_g.ico')
width = root.winfo_screenwidth()
height = int(root.winfo_screenheight()*0.9)
root.geometry("%dx%d+0+0" % (width, height))
root.resizable(True, True)
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to Exit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# root.attributes('-fullscreen',True)
object = Billing(root)
root.mainloop()