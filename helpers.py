from tkinter import Entry,END,INSERT, Event, Listbox
from tkinter.constants import OUTSIDE, S
from typing import Callable

def formatter(num:int):
    """
    Formats a given num into Indian format
    Returns a string
    """
    format_total=""
    total_copy = int(float(num))
    if total_copy<1000:
        format_total=str(total_copy)
    else:
        format_total="{:0>3d}".format(total_copy%1000)
        total_copy=int(total_copy/1000)
        format_total=","+format_total
        while total_copy>99:
            format_total=","+"{:0>2d}".format(total_copy%100) + format_total
            total_copy=int(total_copy/100)
        if total_copy!=0:
            format_total=str(total_copy)+format_total
        format_total="₹"+format_total
    return format_total

class AutocompleteEntry():
    """
    Takes an existing Entry and enables auto Complete Functionality.
    """
    def __init__(self,Entry_: Entry,set_data: Callable[[int],None]):
        self._entry = Entry_
        self.set_data=set_data
    def set_completion_list(self, completion_list):
        """
        Expects a function that returns key value pairs when called.
        keys are autocompleted and set_data is called with the value
        """
        #pylint: disable=attribute-defined-outside-init
        self._completion_list_fn = completion_list # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self._entry.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        """Autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits."""
        #pylint: disable=attribute-defined-outside-init
        if delta: # need to delete selection otherwise we would fix the current position
            self._entry.delete(self.position, END)
        else: # set position to end so selection starts where textentry ended
            self.position = len(self._entry.get())
        # collect hits
        _hits = []
        self._completion_list = dict(self._completion_list_fn())
        for element in self._completion_list.keys():
            if element.lower().startswith(self._entry.get().lower()):  # Match case-insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits=_hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self._entry.delete(0,END)
            self._entry.insert(0,self._hits[self._hit_index])
            self._entry.select_range(self.position,END)

    def handle_keyrelease(self, event):
        """Event handler for the keyrelease event on this widget."""
        #pylint: disable=attribute-defined-outside-init
        if event.keysym == "BackSpace":
            self._entry.delete(self._entry.index(INSERT), END)
            self.position = self._entry.index(END) 
        if event.keysym == "Left":
            if self.position < self._entry.index(END): # delete the selection
                self._entry.delete(self.position, END)
            else:
                self.position = self.position-1 # delete one character
                self._entry.delete(self.position, END)
        if event.keysym == "Right":
            self.position = self._entry.index(END) # go to end (no selection)
        if event.keysym == "Down":
            self.autocomplete(1) # cycle to next hit
        if event.keysym == "Up":
            self.autocomplete(-1) # cycle to previous hit
        if len(event.keysym) == 1 :
            self.autocomplete()
        if event.keysym == "Return":
            _id=self._completion_list.get(self._hits[self._hit_index])
            self.set_data(_id)

class AutocompleteCombobox():
    """
    Takes an existing Entry and enables auto Complete Functionality.
    """
    def __init__(self,Entry_: Entry,set_data: Callable[[int],None]):
        self._entry = Entry_
        self.set_data=set_data
        self.parent = Entry_.nametowidget(Entry_.winfo_parent())
        self.listbox = Listbox(self.parent)        
    def _place_listbox(self):
        self.listbox.configure(height=0)    
        self.listbox.place(in_=self._entry,bordermode=OUTSIDE,relx=0,rely=1,relwidth=1,y=5)
        self.listbox.lift()
    def _forget_listbox(self):
        self.listbox.place_forget()
    def set_completion_list(self, completion_list):
        """
        Expects a function that returns key value pairs when called.
        keys are autocompleted and set_data is called with the value
        """
        #pylint: disable=attribute-defined-outside-init
        self._completion_list_fn = completion_list # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self._entry.bind('<KeyRelease>', self.handle_keyrelease)
        self._entry.bind('<KeyPress>',self.handle_keypress)
        self.listbox.bind('<KeyRelease>',self.handle_return)
        self.listbox.bind('<FocusOut>',self._outta_focus)
        self._entry.bind('<FocusOut>',self._outta_focus)
    def _outta_focus(self,_):
        if self.parent.focus_get() not in (self._entry ,self.listbox):
            self._forget_listbox()
    def autocomplete(self):
        """Autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits."""
        #pylint: disable=attribute-defined-outside-init
        self.listbox.delete(0, END)
        # collect hits
        _hits = []
        self._completion_list = dict(self._completion_list_fn())
        for element in self._completion_list.keys():
            if element.lower().startswith(self._entry.get().lower()):  # Match case-insensitively
                _hits.append(element)
        self._hits=_hits
        if self._hits:
            self.listbox.delete(0,END)
            for hit in self._hits:
                self.listbox.insert(END,hit)
            self._place_listbox()
        else:
            self._forget_listbox()
    def handle_keypress(self,event:Event):
        if event.keysym == "Tab":
            self._forget_listbox()
    def handle_return(self,event:Event):
        if event.keysym == "Return":
            self._entry.delete(0,END)
            self._entry.insert(0,self._hits[self.listbox.curselection()[0]])
            _id=self._completion_list.get(self._hits[self.listbox.curselection()[0]])
            self._entry.focus()
            self._forget_listbox()
            self.set_data(_id)
            self._entry.event_generate('<Tab>')
        if event.keysym == "Up":
            if self.listbox.curselection() == (0,):
                self._entry.focus()
        # print(self.listbox.curselection())
    def handle_keyrelease(self, event):
        """Event handler for the keyrelease event on this widget."""
        #pylint: disable=attribute-defined-outside-init
        if event.keysym == "BackSpace":
            self.listbox.delete(0,END)
            self.autocomplete()
        # if event.keysym == "Left":
        #     if self.position < self._entry.index(END): # delete the selection
        #         self._entry.delete(self.position, END)
        #     else:
        #         self.position = self.position-1 # delete one character
        #         self._entry.delete(self.position, END)
        # if event.keysym == "Right":
        #     self.position = self._entry.index(END) # go to end (no selection)
        if event.keysym == "Down":
            self.autocomplete()
            self.listbox.select_set(0)
            self.listbox.focus()
        # if event.keysym == "Up":
        #     self.autocomplete(-1) # cycle to previous hit
        if len(event.keysym) == 1 :
            self.autocomplete()
        # if event.keysym == "Return":
        #     _id=self._completion_list.get(self._hits[self._hit_index])
        #     self.set_data(_id)
