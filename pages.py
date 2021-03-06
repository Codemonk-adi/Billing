
"""Pages for the GUI."""
from tkinter import Label,LabelFrame,Button,Frame
from tkinter import RAISED
from helpers import *
from math import floor, modf
from PyPDF2 import PdfFileReader,PdfFileWriter
from fpdf import FPDF
import details
import url_sender
from data import *
import os
import sys
from database import Database
class Page(Frame):
    def __init__(self):
        Frame.__init__(self)
    def show(self):
        self.lift()

class Page_aj(Page):
    #pylint: disable=line-too-long
    def __init__(self):
        Page.__init__(self) 
        self.data = data_aj()
        #264653
        self.db = Database()
        self.db.create_tables()
        F1 = LabelFrame(self,text="Customer Information",relief=RAISED,bg=self.data.bg_color, fg='#264653', font=("Calibri",12,"bold"))
        
        F1.place(x=0,y=0,relwidth=1,relheight=0.2)

        F2 = LabelFrame(self,text='Details',relief=RAISED,bg=self.data.bg_color, fg='#264653', font=("Calibri",18,"bold"))
        F2.place(x=0,rely=0.2, relwidth=0.72, relheight=0.6)
        
        Fpre = LabelFrame(self, text='Preview',relief=RAISED,bg=self.data.bg_color, fg='#264653', font=("Calibri",18,"bold"))
        Fpre.place(relx=0.72,rely=0.2, relwidth=0.28, relheight=0.6)
        
        F4 = LabelFrame(self,text="Result",relief=RAISED,bg=self.data.bg_color, fg='#264653', font=("Calibri",18,"bold"))
        F4.place(rely=0.8,relwidth=1,relheight=0.2)
        
        # This function for customer contact number
        customercontact_lbl = Label(F1, text="Phone No", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        customercontact_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.cust_num)
        customercontact_en.grid(row=0, column=1, ipady=4, ipadx=30, pady=2)
        AC = AutocompleteEntry(customercontact_en,self.set_retail_data)
        AC.set_completion_list(self.db.get_contact_id_list)
        #for name
        customername_lbl = Label(F1, text="Customer Name", bg=self.data.bg_color, fg=self.data.fg_color,
        font=("Calibri", 15, "bold")).grid(row=0, column=2, padx=10, pady=2)
        customername_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.cust_name)
        customername_en.grid(row=0, column=3, ipady=4, ipadx=30, pady=2)
        # This fucntion for Invoice Number
        customerinvoice_lbl = Label(F1, text="Invoice No.", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(row=0, column=4, padx=20)
        customerinvoice_en = Entry(F1,textvariable=self.data.inv_num,bd=8, relief=RAISED)
        customerinvoice_en.grid(row=0, column=5, ipadx=30, ipady=4, pady=2)
        # #button
        # invoice_btn = Button(F1, text="Enter", bd=7, relief=RAISED, font=("Calibri", 12, "bold"), bg=self.data.bg_color,
        # fg=self.data.fg_color)
        # invoice_btn.grid(row=0, column=6, ipady=5, padx=60, ipadx=19, pady=5)

        # This function for customer address
        customeraddress_lbl = Label(F1, text="Address", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=1, column=0, padx=20)
        customeraddress_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.cust_add, width=50)
        customeraddress_en.grid(row=1, column=1, columnspan=2, ipady=4, ipadx=30, pady=2)       
        #date
        date_lbl = Label(F1,text="Date", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=1, column=3, padx=20)
        date_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.curr_date, width=15)
        date_en.grid(row=1, column=4,ipady=4, ipadx=5, pady=2)

        # root.columnconfigure(0,1)
        
        desc_lbl = Label(F2,text="Particulars", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        descriptions = []
        for i in range(5):
            descriptions.append(Entry(F2,relief=RAISED,bg="pink" if i%2==0 else "white",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[i]))
            descriptions[i].grid(row=i+1,column=0,padx=5, pady=3, ipady=5, ipadx=5)
            AutocompleteCombobox(descriptions[i],self.setter_fn(descriptions[i])).set_completion_list(self.db.get_category_lists)

        weight_lbl = Label(F2, text="Weights",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        weights = []
        for i in range(5):    
            weights.append(Entry(F2,relief=RAISED,bg="pink" if i%2==0 else "white",font=('Calibri', 18, "bold"),textvariable=self.data.weight_list[i]))
            weights[i].grid(row=i+1,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        
        rate_lbl = Label(F2, text="Rate(per gram)",bg=self.data.bg_color, fg=self.data.fg_color,font=("Calibri", 15, "bold")).grid(row=0, column=2, padx=20)
        rates = []
        for i in range(5):    
            rates.append(Entry(F2,relief=RAISED,bg="pink" if i%2==0 else "white",font=('Calibri', 18, "bold"),textvariable=self.data.rate_list[i]))
            rates[i].grid(row=i+1,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        
        # Fr.columnconfigure(0,weight=1)
        
        
        labour_charge_lbl = Label(F2, text="Labour",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=3, padx=20)
        labours = []
        for i in range(5):    
            labours.append(Entry(F2,relief=RAISED,bg="pink" if i%2==0 else "white",font=('Calibri', 18, "bold"),textvariable=self.data.labour_list[i]))
            labours[i].grid(row=i+1,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        
        # Fl.columnconfigure(0,weight=1)

        total_lbl = Label(F4, text="Total",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        total_en = Entry(F4,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.total)
        total_en.grid(row=1,column=0,padx=5)
        
        #payment methods
        payment_lbl = Label(F4, text="Payment Method",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        payment_en = Entry(F4,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.payment_method).grid(row=1,column=1,padx=5)

        #buttons
        total_btn = Button(F4, text="Total", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED,
        command=self.total_section)
        total_btn.grid(row=1, column=4, ipadx=20, padx=30)
        
        # This function for Generate Bill
        generatebill_button = Button(F4, text="Generate Bill", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.billing_section)
        generatebill_button.grid(row=1, column=5, ipadx=20)
        
        # This function for Clear Button
        clear_button = Button(F4, text="Clear", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.clear)
        clear_button.grid(row=1, column=6, ipadx=20, padx=30)
        
        
        # This function for SMS Button
        SMS_buttonn = Button(F4, text="Send Thanks", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.thanks)
        SMS_buttonn.grid(row=1, column=7, ipadx=20)
        
        #This is for printing
        print_button = Button(F4, text="Print", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.print_bill)
        print_button.grid(row=1,column=8, ipadx= 20,padx=30)
        
        F4.rowconfigure(1,weight=1)
        F4.rowconfigure(0,weight=1)

        F2.columnconfigure(0,weight=1)
        F2.columnconfigure(1,weight=1)
        F2.columnconfigure(2,weight=1)
        F2.columnconfigure(3,weight=1)
        F2.columnconfigure(4,weight=1)
        
        customercontact_en.focus()
        widgets=[customercontact_en,customername_en, customerinvoice_en, customeraddress_en,date_en]
        # , description_0, gram_0, rate_0, labour_charge_0,description_1, gram_1, rate_1, labour_charge_1,description_2, gram_2, rate_2, labour_charge_2,description_3, gram_3, rate_3, labour_charge_3,description_4, gram_4, rate_4, labour_charge_4]
        for w in widgets:
            w.lift()
        for i in range(5):
            descriptions[i].lift()
            weights[i].lift()
            rates[i].lift()
            labours[i].lift()
    def close(self):
        self.db.close()
    def thanks(self):
        url_sender.send_thanks(self.data.cust_num.get())
    def setter_fn(self,entry:Entry):
        def fn(_id):
            entry.delete(0,END)
            entry.insert(0,self.db.get_category_name(_id))
        return fn
    def set_retail_data(self,id):
        list_data = self.db.get_custdetails(id)
        self.data.cust_name.set(list_data[0][0])
        self.data.cust_num.set(list_data[0][1])
        self.data.cust_add.set(list_data[0][2])
    def total_section(self):
        
        total = 0
        #formula total+=(gram+(milligram/1000))*((rate/10)+labour)*1.03
        for i in range(5):
            if(self.data.rate_list[i].get()!= ""):
                if(self.data.rate_list[i].get()[-1]=='/'):
                    self.data.total_list[i].set(round(float(self.data.rate_list[i].get()[:-1])*1.03,2))
                    total+=self.data.total_list[i].get()
                else:
                    labour = self.data.labour_list[i].get()
                    if(labour[-1]=='%'):
                        labour = float(labour[:-1])/100*float(self.data.rate_list[i].get())
                    else:
                        labour = float(labour)
                    if(floor(float(self.data.weight_list[i].get()))==0):
                        self.data.total_list[i].set(round((((float(self.data.weight_list[i].get()))*float(self.data.rate_list[i].get()))+labour)*1.03,2))
                        total+=self.data.total_list[i].get()
                    else:
                        self.data.total_list[i].set(round(float(self.data.weight_list[i].get())*(float(self.data.rate_list[i].get())+labour)*1.03,2))
                        total+=self.data.total_list[i].get()
        self.data.total.set(round(total))
        return
    
    def clear(self):
        self.data.cust_name.set('')
        self.data.cust_add.set('')
        self.data.cust_num.set('')
        self.data.inv_num.set(self.data.inv_num.get()+1)
        self.data.total.set('')
        self.data.payment_method.set('')
        for i in range(5):
            self.data.desc_list[i].set('')
            self.data.weight_list[i].set('')
            self.data.rate_list[i].set('')
            self.data.labour_list[i].set('')
            self.data.total_list[i].set(0.0)
        self.data.isgenerated = False
        return
    def billing_section(self):
        self.total_section()
        cust_id = self.db.insert_retail_user({
        'name':self.data.cust_name.get(),
        'contact': self.data.cust_num.get(),
        'address':self.data.cust_add.get()
        })
        
        pdf=FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_font('Times_uni',fname="Quivira.otf",uni=True)
        pdf.add_font('Times_uniB',fname="arialB.ttf",uni=True)
        pdf.add_page()
        pdf.set_font("Times_uni",size=11)
        #Invoice Number
        pdf.set_xy(45.7,54.8)
        pdf.cell(w=41.4,h=7.1,align='L',txt=str(self.data.inv_num.get()))
        #Date
        pdf.set_xy(149.4,54.8)
        pdf.cell(w=35.7,h=7.1,txt=self.data.curr_date.get())
        #Name
        pdf.set_xy(37.8,62.7)
        pdf.cell(w=56.4,h=7.1,txt=self.data.cust_name.get().title())
        #Address
        pdf.set_xy(41.1,69.6)
        pdf.multi_cell(w=58.9,h=8.1,txt=self.data.cust_add.get().title())
        #Contact Number
        pdf.set_xy(166.7,69.6)
        pdf.cell(w=39.1,h=8.1,txt=self.data.cust_num.get())
        # self.db.create_retail_bill({
        # 'name':self.data.cust_name.get(),
        # 'contact': self.data.cust_num.get(),
        # 'address':self.data.cust_add.get()
        # })
        bill_id = self.db.insert_retail_bill({
        'invoice': self.data.inv_num.get(),
        'date': self.data.curr_date.get(),
        'cust_id':cust_id,
        'total': self.data.total.get()
        })
        particulars = []
        #Details
        for i in range(5):
            if(self.data.rate_list[i].get() != ""):
                rate = self.data.rate_list[i].get()
                if rate[-1]=='/':
                    rate = rate + 'Pc'    
                    if(self.data.weight_list[i].get()!=''):
                        mgram,gram = modf(float(self.data.weight_list[i].get()))
                        gram=str(int(gram))
                        mgram = str(int(round(mgram,3)*1000)).zfill(3)
                    else:
                        gram,mgram = ("","")
                else:
                        mgram,gram = modf(float(self.data.weight_list[i].get()))
                        gram=str(int(gram))
                        mgram = str(int(round(mgram,3)*1000)).zfill(3)
                entry = [i,bill_id,self.data.desc_list[i].get().title(),gram,mgram,float(rate[:-3]),self.data.labour_list[i].get(),self.data.total_list[i].get()]
                pdf.set_xy(13,22.1*i+99.8)
                pdf.multi_cell(w=51.8,h=22.1,align="C",txt=(entry[2]))
                pdf.set_xy(65,22.1*i+99.8)
                pdf.cell(w=14,h=22.1  ,align="C",txt=str(entry[3]))
                pdf.cell(w=14,h=22.1  ,align="C",txt=str(entry[4]))
                pdf.cell(w=23.4,h=22.1,align="C",txt=rate)
                pdf.cell(w=27.7,h=22.1,align="C",txt=str(entry[6]))
                pdf.cell(w=24.6,h=22.1,align="C",txt="3%")
                pdf.cell(w=33.8,h=22.1,align="C",txt=str(entry[7]))
                particulars.append(entry)
        self.db.insert_retail_bill_particulars(bill_id,particulars)
        #Payment Method
        pdf.set_xy(15.7,239.5)
        pdf.set_font(family="Times_uni",size=12)
        pdf.cell(w=29.2,h=7.9,txt=self.data.payment_method.get().capitalize())
        
        #Total
        pdf.set_xy(169.2,233.4)
        pdf.cell(w=34,h=18.3,txt=formatter(self.data.total.get()))
        
        pdf.output("temp.pdf")
        pdf.close()
        
        pdf_template = PdfFileReader(open("bill_temp_v3.pdf","rb"))
        template_page = pdf_template.getPage(0)
        overlay_pdf=    PdfFileReader(open("temp.pdf",'rb'))
        template_page.mergePage(overlay_pdf.getPage(0))
        output_pdf = PdfFileWriter()
        output_pdf.addPage(template_page)
        os.makedirs("Bill_store/Akash",exist_ok=True)
        
        if getattr(sys, 'frozen', False):
        # The application is frozen
            dirname = os.path.dirname(sys.executable)
        else:
            dirname = os.path.dirname(__file__)
        
        pdfname = str(date.today())+str(self.data.cust_name.get())+str(self.data.inv_num.get())+".pdf"
        # pdfname = str(self.data.inv_num.get())+str(self.data.cust_name.get())+".pdf"
        self.data.filename = os.path.join(dirname, 'Bill_store/Akash/'+pdfname)
        output_pdf.write(open(self.data.filename,'wb'))
        
        os.startfile(self.data.filename, "open")
    def print_bill(self):
        self.billing_section()
        os.startfile(self.data.filename, "print")
    # def exit(self.data):
    #     return
class page_rest(Page):
    def __init__(self,firm):
        Page.__init__(self)
        self.db = Database()
        self.firm = firm
        self.data = data_rest()
        F1 = LabelFrame(self,text="Customer Information", font=("Calibri", 12, "bold"), fg="#264653", bg=self.data.bg_color,
        relief=RAISED)
        F1.place(x=0,y=0,relwidth=1,relheight=0.2)

        F2 = LabelFrame(self,text='Details',relief=RAISED,bg=self.data.bg_color, fg='#264653', font=("Calibri",18,"bold"))
        F2.place(x=0,rely=0.2, relwidth=0.72, relheight=0.6)
        
        Fpre = LabelFrame(self, text='Preview',relief=RAISED,bg=self.data.bg_color, fg='#264653', font=("Calibri",18,"bold"))
        Fpre.place(relx=0.72,rely=0.2, relwidth=0.28, relheight=0.6)
        
        F4 = LabelFrame(self,text="Result",relief=RAISED,bg=self.data.bg_color, fg='#264653', font=("Calibri",18,"bold"))
        F4.place(rely=0.8,relwidth=1,relheight=0.2)
        
        #for name
        customername_lbl = Label(F1, text="Customer Name", bg=self.data.bg_color, fg=self.data.fg_color,
        font=("Calibri", 15, "bold")).grid(row=0, column=0, padx=10, pady=2)
        customername_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.cust_name)
        customername_en.grid(row=0, column=1, ipady=4, ipadx=30, pady=2)
        AC = AutocompleteEntry(customername_en,self.set_whole_data)
        AC.set_completion_list(self.db.get_whole_name_id_list)

        # This function for GST number
        customergst_lbl = Label(F1, text="GST Number", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=2, padx=20)
        customergst_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.gst_num)
        customergst_en.grid(row=0, column=3,columnspan=2, ipady=4, ipadx=30, pady=2)
        # This fucntion for Invoice Number
        customerinvoice_lbl = Label(F1, text="Invoice No.", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(row=0, column=5, padx=20)
        customerinvoice_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.inv_num)
        customerinvoice_en.grid(row=0, column=6, ipadx=30, ipady=4, pady=2)

        # #button
        # invoice_btn = Button(F1, text="Enter", bd=7, relief=RAISED, font=("Calibri", 12, "bold"), bg=self.data.bg_color,
        # fg=self.data.fg_color)
        # invoice_btn.grid(row=0, column=6, ipady=2, padx=60, ipadx=19, pady=2)

        # This function for customer address
        customeraddress_lbl = Label(F1, text="Address", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=1, column=0, padx=20)
        customeraddress_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.cust_add, width=50)
        customeraddress_en.grid(row=1, column=1, columnspan=2, ipady=4, ipadx=30, pady=2)
        

        #date
        date_lbl = Label(F1,text="Date", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=1, column=3, padx=20)
        date_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.curr_date, width=15)
        date_en.grid(row=1, column=4,ipady=4, ipadx=5, pady=2)

        # root.columnconfigure(0,1)
        
        desc_lbl = Label(F2,text="Particulars", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        descriptions = []
        for i in range(5):
            descriptions.append(Entry(F2,relief=RAISED,bg="pink" if i%2==0 else "white",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[i]))
            descriptions[i].grid(row=i+1,column=0,padx=5, pady=3, ipady=5, ipadx=5)
            AutocompleteCombobox(descriptions[i],self.setter_fn(descriptions[i])).set_completion_list(self.db.get_category_lists)

        weight_lbl = Label(F2, text="Weights",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        weights = []
        for i in range(5):    
            weights.append(Entry(F2,relief=RAISED,bg="pink" if i%2==0 else "white",font=('Calibri', 18, "bold"),textvariable=self.data.weight_list[i]))
            weights[i].grid(row=i+1,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        
        rate_lbl = Label(F2, text="Rate(per gram)",bg=self.data.bg_color, fg=self.data.fg_color,font=("Calibri", 15, "bold")).grid(row=0, column=2, padx=20)
        rates = []
        for i in range(5):    
            rates.append(Entry(F2,relief=RAISED,bg="pink" if i%2==0 else "white",font=('Calibri', 18, "bold"),textvariable=self.data.rate_list[i]))
            rates[i].grid(row=i+1,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        
        amount_lbl = Label(F4, text="Amount",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        amount_en = Entry(F4,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.pretotal)
        amount_en.grid(row=1,column=0,padx=5)
        #payment methods
        ptotal_lbl = Label(F4, text="Total",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        ptotal_en = Entry(F4,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.posttotal).grid(row=1,column=1,padx=5)

        #buttons
        total_btn = Button(F4, text="Total", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED,
        command=self.total_section)
        total_btn.grid(row=1, column=4, ipadx=20, padx=30)
        
        # This function for Generate Bill
        generatebill_button = Button(F4, text="Generate Bill", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.billing_section)
        generatebill_button.grid(row=1, column=5, ipadx=20)
        
        # This function for Clear Button
        clear_button = Button(F4, text="Clear", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.clear)
        clear_button.grid(row=1, column=6, ipadx=20, padx=30)
        
        # # This function for Exit Button
        # exit_buttonn = Button(F4, text="Exit", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.exit)
        # exit_buttonn.grid(row=1, column=7, ipadx=20)
        print_button = Button(F4, text="Print", bg=self.data.bg_color, fg=self.data.fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.print_bill)
        print_button.grid(row=1,column=7, ipadx= 20)
        F4.rowconfigure(1,weight=1)
        F4.rowconfigure(0,weight=1)

        F2.columnconfigure(0,weight=1)
        F2.columnconfigure(1,weight=1)
        F2.columnconfigure(2,weight=1)
        F2.columnconfigure(3,weight=1)
        F2.columnconfigure(4,weight=1)
        
        customername_en.focus()
        widgets=[customername_en,customergst_en, customerinvoice_en, customeraddress_en,date_en]
        # , description_0, gram_0, rate_0, labour_charge_0,description_1, gram_1, rate_1, labour_charge_1,description_2, gram_2, rate_2, labour_charge_2,description_3, gram_3, rate_3, labour_charge_3,description_4, gram_4, rate_4, labour_charge_4]
        for w in widgets:
            w.lift()
        for i in range(5):
            descriptions[i].lift()
            weights[i].lift()
            rates[i].lift()
    def close(self):
        self.db.close()
    def setter_fn(self,entry:Entry):
        def fn(_id):
            entry.delete(0,END)
            entry.insert(0,self.db.get_category_name(_id))
        return fn
    def set_whole_data(self,id):
        list_data = self.db.get_whole_custdetails(id)
        self.data.cust_name.set(list_data[0][0])
        self.data.gst_num.set(list_data[0][1])
        self.data.cust_add.set(list_data[0][2])
    def total_section(self):
        total = 0
        total_mg = 0
        total_g =0
        #formula total+=(gram+(milligram/1000))*((rate/10)+labour)*1.03
        for i in range(5):
            if(self.data.rate_list[i].get() != ""):
                mgram,gram = modf(float(self.data.weight_list[i].get()))
                gram=int(gram)
                mgram = int(round(mgram,3)*1000)
                self.data.total_pretax_list[i].set(round((float(self.data.weight_list[i].get()))*(float(self.data.rate_list[i].get()))))
                self.data.total_posttax_list[i].set(round(self.data.total_pretax_list[i].get()*1.03,2))
                self.data.tax_list[i].set(round(self.data.total_pretax_list[i].get()*0.015,1))
                total+=self.data.total_pretax_list[i].get()
                total_mg += mgram
                total_g += gram
        self.data.pretotal.set(total)
        self.data.total_tax.set(total*0.015)
        self.data.total_mgram.set(total_mg%1000)
        self.data.total_gram.set(total_g + int(total_mg/1000))
        self.data.posttotal.set(round(total*1.03))
        return
        
    def billing_section(self):
        self.total_section()
        pdf=FPDF(orientation='P', unit='mm', format='A4')
        state = True
        if(self.data.gst_num.get()[:2] == '27'):
            state=True
        else:
            state=False
        cust_id = self.db.insert_whole_user({
        'name':self.data.cust_name.get(),
        'gst_no': self.data.gst_num.get(),
        'address':self.data.cust_add.get()
        })
        
        pdf.add_font('Times_uniB',fname="arialB.ttf",uni=True)
        pdf.add_font('Times_uni',fname="Quivira.otf",uni=True)
        pdf.add_page()
        pdf.set_font("Times_uni",size=11)
        #Invoice Number
        pdf.set_xy(31.3,53.6)
        pdf.cell(w=10.2,h=3.5,align='L',txt=str(self.data.inv_num.get()))
        #Date   
        pdf.set_xy(135.4,53.6)
        pdf.cell(w=15,h=3.5,align='L',txt=self.data.curr_date.get())
        #Name
        pdf.set_xy(23.9,61.7)
        pdf.cell(w=56.4,h=3.5,align='L',txt=self.data.cust_name.get().title())
        #Address
        pdf.set_xy(27.2,68.6)
        pdf.multi_cell(w=58.9,h=3.5,align='L',txt=self.data.cust_add.get().title())
        #Gst Number
        pdf.set_xy(141.2,68.6)
        pdf.cell(w=39.1,h=3.5,align='L',txt=self.data.gst_num.get().upper())
        
        bill_id = self.db.insert_whole_bill({
        'invoice': self.data.inv_num.get(),
        'firm':self.firm,
        'date': self.data.curr_date.get(),
        'cust_id':cust_id,
        'total': self.data.posttotal.get()
        })
        #Account info
        pdf.set_font("Times_uni",size=11)
        pdf.set_xy(25,235.9)
        pdf.cell(w=32,h=3,align='L',txt = details.ac[self.firm])
        pdf.set_xy(30.7,240.8)
        pdf.cell(w=32,h=3,align='L',txt = details.ifsc[self.firm])

        #sign
        pdf.set_xy(154.2,257.8)
        pdf.cell(w=30,h=3.5,align='L',txt=details.name[self.firm])
        particulars=[]
        if(state):
            #Details
            for i in range(5):
                if(self.data.rate_list[i].get() != ""):
                    mgram,gram = modf(float(self.data.weight_list[i].get()))
                    gram=int(gram)
                    mgram = int(round(mgram,3)*1000)
                    entry = [i,bill_id,self.data.desc_list[i].get().title(),gram,mgram,float(self.data.rate_list[i].get())]
                    pdf.set_xy(2.8,19.76*i+88.1)
                    pdf.multi_cell(w=40.9,h=19.76,align="C",txt=self.data.desc_list[i].get().title())
                    pdf.set_xy(43.7,19.76*i+88.1)
                    pdf.cell(w=19.3,h=19.76  ,align="C",txt=str(gram))
                    pdf.cell(w=19.6,h=19.76  ,align="C",txt=str(mgram).zfill(3))
                    pdf.cell(w=22.1,h=19.76,align="C",txt=str(self.data.rate_list[i].get()))
                    pdf.cell(w=25.1,h=19.76,align="C",txt=str(self.data.total_pretax_list[i].get()))
                    pdf.cell(w=19.1,h=19.76,align="C",txt=str(self.data.tax_list[i].get()))
                    pdf.cell(w=18.3,h=19.76,align="C",txt=str(self.data.tax_list[i].get()))
                    pdf.cell(w=40.1,h=19.76,align="C",txt=str(self.data.total_posttax_list[i].get()))
                    particulars.append(entry)
            #summary
            pdf.set_font("Times_uniB",size=11)
            pdf.set_xy(43.7,203)
            pdf.cell(w=19.3,h=9.7,align="C",txt=str(self.data.total_gram.get()))
            pdf.cell(w=19.6,h=9.7,align="C",txt=str(self.data.total_mgram.get()).zfill(3))
            pdf.set_xy(104.7,203)
            pdf.cell(w=25.1,h=9.7,align="C",txt=formatter(self.data.pretotal.get()))
            pdf.cell(w=19.1,h=9.7,align="C",txt=formatter(self.data.total_tax.get()))
            pdf.cell(w=18.3,h=9.7,align="C",txt=formatter(self.data.total_tax.get()))
            pdf.cell(w=40.1,h=9.7,align="C",txt=formatter(self.data.posttotal.get()))
            
            
        else:
            
            #Details
            for i in range(5):
                if(self.data.rate_list[i].get() != ""):
                    mgram,gram = modf(float(self.data.weight_list[i].get()))
                    gram=int(gram)
                    mgram = int(round(mgram,3)*1000)
                    entry = [i,bill_id,self.data.desc_list[i].get().title(),gram,mgram,float(self.data.rate_list[i].get())]
                    pdf.set_xy(2.8,19.76*i+88.1)
                    pdf.multi_cell(w=40.9,h=19.76,align="C",txt=self.data.desc_list[i].get().title())
                    pdf.set_xy(43.7,19.76*i+88.1)
                    pdf.cell(w=19.3,h=19.76  ,align="C",txt=str(gram))
                    pdf.cell(w=19.6,h=19.76  ,align="C",txt=str(mgram).zfill(3))
                    pdf.cell(w=22.1,h=19.76,align="C",txt=str(self.data.rate_list[i].get()))
                    pdf.cell(w=40,h=19.76,align="C",txt=str(self.data.total_pretax_list[i].get()))
                    pdf.cell(w=22.5,h=19.76,align="C",txt=str(self.data.tax_list[i].get()*2))
                    pdf.cell(w=40.1,h=19.76,align="C",txt=str(self.data.total_posttax_list[i].get()))
                    particulars.append(entry)
            #summary
            pdf.set_font("Times_uniB",size=11)
            pdf.set_xy(43.7,203)
            pdf.cell(w=19.3,h=9.7,align="C",txt=str(self.data.total_gram.get()))
            pdf.cell(w=19.6,h=9.7,align="C",txt=str(self.data.total_mgram.get()).zfill(3))
            pdf.set_xy(104.7,203)
            pdf.cell(w=40,h=9.7,align="C",txt=formatter(self.data.pretotal.get()))
            pdf.cell(w=22.5,h=9.7,align="C",txt=formatter(self.data.total_tax.get()*2))
            pdf.cell(w=40.1,h=9.7,align="C",txt=formatter(self.data.posttotal.get()))                    
        pdf.output("temp.pdf")
        pdf.close()
        self.db.insert_whole_bill_particulars(bill_id,particulars)
        
        if(state):
            pdf_template = PdfFileReader(open("Wholesale_template_v4.pdf","rb"))
        else:
            pdf_template = PdfFileReader(open("wholesale_template_igst_v2.pdf","rb"))
        template_page = pdf_template.getPage(0)
        overlay_pdf=    PdfFileReader(open("temp.pdf",'rb'))
        template_page.mergePage(overlay_pdf.getPage(0))
        output_pdf = PdfFileWriter()
        output_pdf.addPage(template_page)
        os.makedirs("Bill_store/"+details.nam[self.firm],exist_ok=True)
        if getattr(sys, 'frozen', False):
        # The application is frozen
            dirname = os.path.dirname(sys.executable)
        else:
            dirname = os.path.dirname(__file__)
        
        pdfname = str(date.today())+str(self.data.cust_name.get())+str(self.data.inv_num.get())+".pdf"
        # pdfname = str(self.data.inv_num.get())+str(self.data.cust_name.get())+".pdf"
        self.data.filename = os.path.join(dirname, 'Bill_store/'+details.nam[self.firm]+'/'+pdfname)
        output_pdf.write(open(self.data.filename,'wb'))
        
        # os.startfile(filename, "print")
        os.startfile(self.data.filename, "open")
    def clear(self):
        self.data.cust_name.set('')
        self.data.cust_add.set('')
        self.data.gst_num.set('')
        self.data.inv_num.set(self.data.inv_num.get()+1)
        for i in range(5):
            self.data.desc_list[i].set('')
            self.data.weight_list[i].set('')
            self.data.rate_list[i].set('')
            self.data.total_pretax_list[i].set(0)
            self.data.total_posttax_list[i].set(0)
            self.data.tax_list[i].set(0)
        self.data.pretotal.set('')
        self.data.posttotal.set('')
        return
    def print_bill(self):
        self.billing_section()
        os.startfile(self.data.filename, "print")
        return

#to be saved