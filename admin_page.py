
from tkinter import Button, Entry, Label, LabelFrame, Listbox
from tkinter.constants import END, OUTSIDE, RAISED
import pages
from database import Database
from helpers import *
class page_admin(pages.Page):
    """Page to add aliases and do other admin stuff."""
    def __init__(self):
        super().__init__()
        self.db = Database()
        F1 = LabelFrame(self,text="Aliases",relief='raised',bg='#f8edeb' , fg='#264653', font=("Calibri",12,"bold"))
        F1.place(x=0,y=0,relwidth=1,relheight=0.4)
        Label(F1, text="Category",bg='#f8edeb' , fg='#264653' , font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        self.category_en = Entry(F1)
        self.category_en.grid(row=1, column=0, ipady=4, ipadx=30, pady=2)
        AC=AutocompleteCombobox(self.category_en,self.fill_alias)
        AC.set_completion_list(self.db.get_category_lists_s)
        Label(F1, text="Alias",bg='#f8edeb' , fg='#264653' , font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        self.aliases_en = Entry(F1)
        self.aliases_en.grid(row=1, column=1, ipady=4, ipadx=30, pady=2)
        self.aliases_en_l = Listbox(F1)
        self.aliases_en_l.place(in_=self.aliases_en,relx=0,rely=1,relwidth=1,y=5)
        add_alias_btn = Button(F1,text='Add Alias',bg='#f8edeb' , fg='#264653', font=("lucida", 12, "bold"), bd=7, relief=RAISED,command=self.add_alias)
        add_alias_btn.grid(row=2,column=2,ipady=4, ipadx=30, pady=2)
        add_cat_btn = Button(F1,text='Add Category',bg='#f8edeb' , fg='#264653', font=("lucida", 12, "bold"), bd=7, relief=RAISED,command=self.add_category)
        add_cat_btn.grid(row=3,column=2,ipady=4, ipadx=30, pady=2)
    def add_alias(self):
        self.db.insert_alias(self._id,self.aliases_en.get())
        self.fill_alias(self._id)
    def fill_alias(self,_id):
        self._id = _id
        aliases = self.db.get_aliases(_id)
        self.aliases_en_l.delete(0,END)
        for alias in aliases:
            self.aliases_en_l.insert(END,alias)
    def add_category(self):
        self.db.insert_categories(self.category_en.get())