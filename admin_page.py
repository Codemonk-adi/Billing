
from tkinter import Button, Entry, Label, LabelFrame, Listbox, messagebox
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
        del_cat_btn = Button(F1,text='Delete Category',bg='#f8edeb' , fg='#264653', font=("lucida", 12, "bold"), bd=7, relief=RAISED,command=self.delete_category)
        del_cat_btn.grid(row=3,column=3,ipady=4, ipadx=30, pady=2)
        del_alias_btn = Button(F1,text='Delete Alias',bg='#f8edeb' , fg='#264653', font=("lucida", 12, "bold"), bd=7, relief=RAISED,command=self.delete_alias)
        del_alias_btn.grid(row=2,column=3,ipady=4, ipadx=30, pady=2)
        
    def delete_category(self):
        _id_tuple = self.db.get_category_id(self.category_en.get())
        if _id_tuple is None:
            messagebox.showinfo('Invalid Category',f'{self.category_en.get()} Not Found')
        else:
            self.db.del_categoty(_id_tuple[0])
            self.aliases_en_l.delete(0,END)
            self.category_en.focus()
    def delete_alias(self):
        try:    
            _id_tuple = self.db.get_alias_id(self.aliases_en_l.selection_get())
            if _id_tuple is None:
                messagebox.showinfo('Invalid Category',f'{self.category_en.get()} Not Found')
            else:
                self.db.del_alias(_id_tuple[0])
                self.fill_alias(self.db.get_category_id(self.category_en.get())[0])
        except:
            pass
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
        _id = self.db.insert_categories(self.category_en.get())
        self.fill_alias(_id)