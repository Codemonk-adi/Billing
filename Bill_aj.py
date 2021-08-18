# from re import template
import sys
from tkinter import*
from tkinter import messagebox
from datetime import date
from typing import Container
from fpdf import FPDF
from PyPDF2 import PdfFileReader,PdfFileWriter
import os
import details
# -*- coding: utf-8 -*-


def formatter(num):
    format_total=""
    total_copy = int(float(num))
    if(total_copy<1000):
        format_total=str(total_copy)
    else:
        format_total="{:0>3d}".format(total_copy%1000)
        total_copy=int(total_copy/1000)
        format_total=","+format_total
        while(total_copy>99):
            format_total=","+"{:0>2d}".format(total_copy%100) + format_total
            total_copy=int(total_copy/100)
        if(total_copy!=0):
            format_total=str(total_copy)+format_total
        format_total="₹"+format_total
    return format_total
        
    
# coding
class Customer():
    def __init__(self):
        self.rate = IntVar()
        self.labour_charge()
        self.gst = 0.03

        # variables
        self.cust_name = StringVar()
        self.cust_add = StringVar()
        self.cust_num = StringVar()
        self.curr_date = StringVar()
        self.inv_num = IntVar()
        self.particulars = []


class data_rest():
    def __init__(self):
        self.acc_no = StringVar()
        self.istotaled = False
        self.isgenerated = False
        self.filename = StringVar()
        self.cust_name = StringVar()
        self.cust_add = StringVar()
        self.gst_num = StringVar()
        self.curr_date = StringVar()
        self.inv_num = IntVar()
        self.item_details = []
        self.desc_list = [StringVar() for i in range(5)]
        self.gram_list = [IntVar() for i in range(5)]
        self.mgram_list = [IntVar() for i in range(5)]
        self.rate_list = [IntVar() for i in range(5)]
        self.total_gram = IntVar()
        self.total_mgram = IntVar()
        self.total_tax = DoubleVar()
        # self.labour_list = [IntVar() for i in range(5)]
        self.total_pretax_list = [DoubleVar() for i in range(5)]
        self.tax_list = [DoubleVar() for i in range(5)]
        self.total_posttax_list = [DoubleVar() for i in range(5)]
        self.pretotal = StringVar()
        self.posttotal = StringVar()
        self.curr_date.set(date.today().strftime('%d/%m/%y'))
        # self.payment_method = StringVar()
        # self.cust_name.set(str("Aadit"))
        self.bg_color = '#f8edeb'
        self.fg_color = '#C70039'
        return
    
class data_aj():
    def __init__(self):
        self.istotaled = False
        self.isgenerated = False
        self.filename = StringVar()
        self.cust_name = StringVar()
        self.cust_add = StringVar()
        self.cust_num = StringVar()
        self.curr_date = StringVar()
        self.inv_num = IntVar()
        self.item_details = []
        self.desc_list = [StringVar() for i in range(5)]
        self.gram_list = [IntVar() for i in range(5)]
        self.mgram_list = [IntVar() for i in range(5)]
        self.rate_list = [IntVar() for i in range(5)]
        self.labour_list = [IntVar() for i in range(5)]
        self.total_list = [DoubleVar() for i in range(5)]
        self.total = StringVar()
        self.curr_date.set(date.today().strftime('%d/%m/%y'))
        self.payment_method = StringVar()
        # self.cust_name.set(str("Aadit"))
        self.bg_color = '#f8edeb'
        self.fg_color = '#C70039'


class Page(Frame):
    def __init__(self):
        Frame.__init__(self)
    def show(self):
        self.lift()

class Page_aj(Page):
    def __init__(self):
        Page.__init__(self)
        self.data = data_aj()
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
        
        # This function for customer contact number
        customercontact_lbl = Label(F1, text="Phone No", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=2, padx=20)
        customercontact_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.cust_num)
        customercontact_en.grid(row=0, column=3, ipady=4, ipadx=30, pady=2)
        # This fucntion for Invoice Number
        customerinvoice_lbl = Label(F1, text="Invoice No.", bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(row=0, column=4, padx=20)
        customerinvoice_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.data.inv_num)
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
        description_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[0])
        description_0.grid(row=1,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_1 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[1])
        description_1.grid(row=2,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_2 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[2])
        description_2.grid(row=3,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_3 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[3])
        description_3.grid(row=4,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_4 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[4])
        description_4.grid(row=5,column=0,padx=5, pady=3, ipady=5, ipadx=5)

        W_gram_lbl = Label(F2, text="Gram",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        gram_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[0])
        gram_0.grid(row=1,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_1 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[1])
        gram_1.grid(row=2,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_2 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[2])
        gram_2.grid(row=3,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_3 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[3])
        gram_3.grid(row=4,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_4 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[4])
        gram_4.grid(row=5,column=1,padx=2, pady=3, ipady=5, ipadx=2)

        W_milli_gram_lbl = Label(F2, text="Milli Gram",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=2, padx=20)
        mgram_0 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[0],bg="pink",font=('Calibri', 18, "bold"))
        mgram_0.grid(row=1,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_1 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[1],font=('Calibri', 18, "bold"))
        mgram_1.grid(row=2,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_2 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[2],bg="pink",font=('Calibri', 18, "bold"))
        mgram_2.grid(row=3,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_3 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[3],font=('Calibri', 18, "bold"))
        mgram_3.grid(row=4,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_4 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[4],bg="pink",font=('Calibri', 18, "bold"))
        mgram_4.grid(row=5,column=2,padx=2, pady=3, ipady=5, ipadx=2)

        rate_lbl = Label(F2, text="Rate(per gram)",bg=self.data.bg_color, fg=self.data.fg_color,font=("Calibri", 15, "bold")).grid(row=0, column=3, padx=20)
        rate_0 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[0],bg="pink",font=('Calibri', 18, "bold"))
        rate_0.grid(row=1,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_1 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[1],font=('Calibri', 18, "bold"))
        rate_1.grid(row=2,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_2 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[2],bg="pink",font=('Calibri', 18, "bold"))
        rate_2.grid(row=3,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_3 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[3],font=('Calibri', 18, "bold"))
        rate_3.grid(row=4,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_4 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[4],bg="pink",font=('Calibri', 18, "bold"))
        rate_4.grid(row=5,column=3,padx=2, pady=3, ipady=5, ipadx=2)

        
        # Fr.columnconfigure(0,weight=1)
        
        
        labour_charge_lbl = Label(F2, text="Labour",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=4, padx=20)
        labour_charge_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.labour_list[0])
        labour_charge_0.grid(row=1,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        labour_charge_1 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[1],font=('Calibri', 18, "bold"))
        labour_charge_1.grid(row=2,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        labour_charge_2 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[2],bg="pink",font=('Calibri', 18, "bold"))
        labour_charge_2.grid(row=3,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        labour_charge_3 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[3],font=('Calibri', 18, "bold"))
        labour_charge_3.grid(row=4,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        labour_charge_4 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[4],bg="pink",font=('Calibri', 18, "bold"))
        labour_charge_4.grid(row=5,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        
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
        widgets=[customername_en,customercontact_en, customerinvoice_en, customeraddress_en,date_en, description_0, gram_0, mgram_0, rate_0, labour_charge_0,description_1, gram_1, mgram_1, rate_1, labour_charge_1,description_2, gram_2, mgram_2, rate_2, labour_charge_2,description_3, gram_3, mgram_3, rate_3, labour_charge_3,description_4, gram_4, mgram_4, rate_4, labour_charge_4]

        for w in widgets:
            w.lift()
    def total_section(self):
        total = 0
        #formula total+=(gram+(milligram/1000))*((rate/10)+labour)*1.03
        for i in range(5):
            if(self.data.labour_list[i].get() != 0):
                self.data.total_list[i].set((self.data.gram_list[i].get() +(self.data.mgram_list[i].get()/1000))*(self.data.rate_list[i].get()+self.data.labour_list[i].get())*1.03)
                total+=self.data.total_list[i].get()
        self.data.total.set(round(total))
        self.data.istotaled = True
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
            self.data.gram_list[i].set(0)
            self.data.mgram_list[i].set(0)
            self.data.rate_list[i].set(0)
            self.data.labour_list[i].set(0)
            self.data.total_list[i].set(0.0)
        self.data.istotaled= False
        self.data.isgenerated = False
        return
    def billing_section(self):
        if(self.data.istotaled == False):
            self.total_section()
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
        
        #Details
        for i in range(5):
            if(self.data.labour_list[i].get() != 0):
                pdf.set_xy(13,22.1*i+99.8)
                pdf.multi_cell(w=51.8,h=22.1,align="C",txt=self.data.desc_list[i].get().title())
                pdf.set_xy(65,22.1*i+99.8)
                pdf.cell(w=14,h=22.1  ,align="C",txt=str(self.data.gram_list[i].get()))
                pdf.cell(w=14,h=22.1  ,align="C",txt=str(self.data.mgram_list[i].get()))
                pdf.cell(w=23.4,h=22.1,align="C",txt=str(self.data.rate_list[i].get()))
                pdf.cell(w=27.7,h=22.1,align="C",txt=str(self.data.labour_list[i].get()))
                pdf.cell(w=24.6,h=22.1,align="C",txt="3%")
                pdf.cell(w=33.8,h=22.1,align="C",txt=str(self.data.total_list[i].get()))
        
        #Payment Method
        pdf.set_xy(15.7,239.5)
        pdf.set_font(family="Times_uni",size=12)
        pdf.cell(w=29.2,h=7.9,txt=self.data.payment_method.get())
        
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
        
        pdfname = str(date.today())+str(self.data.inv_num.get())+str(self.data.cust_name.get())+".pdf"
        # pdfname = str(self.data.inv_num.get())+str(self.data.cust_name.get())+".pdf"
        self.data.filename = os.path.join(dirname, 'Bill_store/Akash/'+pdfname)
        output_pdf.write(open(self.data.filename,'wb'))
        
        os.startfile(self.data.filename, "open")
        self.data.isgenerated = True
        
        return
    def print_bill(self):
        if(self.data.isgenerated == False):
            self.billing_section()
        
        os.startfile(self.data.filename, "print")
        return
    # def exit(self.data):
    #     return
class page_rest(Page):
    def __init__(self,firm):
        Page.__init__(self)
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
        description_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[0])
        description_0.grid(row=1,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_1 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[1])
        description_1.grid(row=2,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_2 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[2])
        description_2.grid(row=3,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_3 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[3])
        description_3.grid(row=4,column=0,padx=5, pady=3, ipady=5, ipadx=5)
        description_4 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.desc_list[4])
        description_4.grid(row=5,column=0,padx=5, pady=3, ipady=5, ipadx=5)

        W_gram_lbl = Label(F2, text="Gram",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        gram_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[0])
        gram_0.grid(row=1,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_1 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[1])
        gram_1.grid(row=2,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_2 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[2])
        gram_2.grid(row=3,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_3 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[3])
        gram_3.grid(row=4,column=1,padx=2, pady=3, ipady=5, ipadx=2)
        gram_4 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.gram_list[4])
        gram_4.grid(row=5,column=1,padx=2, pady=3, ipady=5, ipadx=2)

        W_milli_gram_lbl = Label(F2, text="Milli Gram",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=2, padx=20)
        mgram_0 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[0],bg="pink",font=('Calibri', 18, "bold"))
        mgram_0.grid(row=1,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_1 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[1],font=('Calibri', 18, "bold"))
        mgram_1.grid(row=2,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_2 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[2],bg="pink",font=('Calibri', 18, "bold"))
        mgram_2.grid(row=3,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_3 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[3],font=('Calibri', 18, "bold"))
        mgram_3.grid(row=4,column=2,padx=2, pady=3, ipady=5, ipadx=2)
        mgram_4 = Entry(F2,relief=RAISED,textvariable=self.data.mgram_list[4],bg="pink",font=('Calibri', 18, "bold"))
        mgram_4.grid(row=5,column=2,padx=2, pady=3, ipady=5, ipadx=2)

        rate_lbl = Label(F2, text="Rate(per gram)",bg=self.data.bg_color, fg=self.data.fg_color,font=("Calibri", 15, "bold")).grid(row=0, column=3, padx=20)
        rate_0 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[0],bg="pink",font=('Calibri', 18, "bold"))
        rate_0.grid(row=1,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_1 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[1],font=('Calibri', 18, "bold"))
        rate_1.grid(row=2,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_2 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[2],bg="pink",font=('Calibri', 18, "bold"))
        rate_2.grid(row=3,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_3 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[3],font=('Calibri', 18, "bold"))
        rate_3.grid(row=4,column=3,padx=2, pady=3, ipady=5, ipadx=2)
        rate_4 = Entry(F2,relief=RAISED,textvariable=self.data.rate_list[4],bg="pink",font=('Calibri', 18, "bold"))
        rate_4.grid(row=5,column=3,padx=2, pady=3, ipady=5, ipadx=2)

        
        # Fr.columnconfigure(0,weight=1)
        
        
        # labour_charge_lbl = Label(F2, text="Labour",bg=self.data.bg_color, fg=self.data.fg_color, font=("Calibri", 15, "bold")).grid(
        # row=0, column=4, padx=20)
        # labour_charge_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.data.labour_list[0])
        # labour_charge_0.grid(row=1,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        # labour_charge_1 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[1],font=('Calibri', 18, "bold"))
        # labour_charge_1.grid(row=2,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        # labour_charge_2 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[2],bg="pink",font=('Calibri', 18, "bold"))
        # labour_charge_2.grid(row=3,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        # labour_charge_3 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[3],font=('Calibri', 18, "bold"))
        # labour_charge_3.grid(row=4,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        # labour_charge_4 = Entry(F2,relief=RAISED,textvariable=self.data.labour_list[4],bg="pink",font=('Calibri', 18, "bold"))
        # labour_charge_4.grid(row=5,column=4,padx=2, pady=3, ipady=5, ipadx=2)
        
        # Fl.columnconfigure(0,weight=1)

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
        widgets=[customername_en,customergst_en, customerinvoice_en, customeraddress_en,date_en, description_0, gram_0, mgram_0, rate_0,description_1, gram_1, mgram_1, rate_1, description_2, gram_2, mgram_2, rate_2,description_3, gram_3, mgram_3, rate_3,description_4, gram_4, mgram_4, rate_4]

        for w in widgets:
            w.lift()

    def total_section(self):
        total = 0
        total_mg = 0
        total_g =0
        #formula total+=(gram+(milligram/1000))*((rate/10)+labour)*1.03
        for i in range(5):
            if(self.data.rate_list[i].get() != 0):
                self.data.total_pretax_list[i].set(round((self.data.gram_list[i].get() +(self.data.mgram_list[i].get()/1000))*(self.data.rate_list[i].get())))
                self.data.total_posttax_list[i].set(round(self.data.total_pretax_list[i].get()*1.03,2))
                self.data.tax_list[i].set(round(self.data.total_pretax_list[i].get()*0.015,1))
                total+=self.data.total_pretax_list[i].get()
                total_mg += self.data.mgram_list[i].get()
                total_g += self.data.gram_list[i].get()
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
        pdf.multi_cell(w=58.9,h=7,align='L',txt=self.data.cust_add.get().title())
        #Gst Number
        pdf.set_xy(141.2,68.6)
        pdf.cell(w=39.1,h=3.5,align='L',txt=self.data.gst_num.get().upper())
        # 
        #Account info
        pdf.set_font("Times_uni",size=11)
        pdf.set_xy(25,235.9)
        pdf.cell(w=32,h=3,align='L',txt = details.ac[self.firm])
        pdf.set_xy(30.7,240.8)
        pdf.cell(w=32,h=3,align='L',txt = details.ifsc[self.firm])

        #sign
        pdf.set_xy(154.2,257.8)
        pdf.cell(w=30,h=3.5,align='L',txt=details.name[self.firm])
        
        if(state):
            #Details
            for i in range(5):
                if(self.data.rate_list[i].get() != 0):
                    pdf.set_xy(2.8,22.1*i+88.1)
                    pdf.multi_cell(w=40.9,h=22.1,align="C",txt=self.data.desc_list[i].get().title())
                    pdf.set_xy(43.7,22.1*i+88.1)
                    pdf.cell(w=19.3,h=22.1  ,align="C",txt=str(self.data.gram_list[i].get()))
                    pdf.cell(w=19.6,h=22.1  ,align="C",txt=str(self.data.mgram_list[i].get()).zfill(3))
                    pdf.cell(w=22.1,h=22.1,align="C",txt=str(self.data.rate_list[i].get()))
                    pdf.cell(w=25.1,h=22.1,align="C",txt=str(self.data.total_pretax_list[i].get()))
                    pdf.cell(w=19.1,h=22.1,align="C",txt=str(self.data.tax_list[i].get()))
                    pdf.cell(w=18.3,h=22.1,align="C",txt=str(self.data.tax_list[i].get()))
                    pdf.cell(w=40.1,h=22.1,align="C",txt=str(self.data.total_posttax_list[i].get()))

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
                if(self.data.rate_list[i].get() != 0):
                    pdf.set_xy(2.8,22.1*i+88.1)
                    pdf.multi_cell(w=40.9,h=22.1,align="C",txt=self.data.desc_list[i].get().title())
                    pdf.set_xy(43.7,22.1*i+88.1)
                    pdf.cell(w=19.3,h=22.1  ,align="C",txt=str(self.data.gram_list[i].get()))
                    pdf.cell(w=19.6,h=22.1  ,align="C",txt=str(self.data.mgram_list[i].get()).zfill(3))
                    pdf.cell(w=22.1,h=22.1,align="C",txt=str(self.data.rate_list[i].get()))
                    pdf.cell(w=40,h=22.1,align="C",txt=str(self.data.total_pretax_list[i].get()))
                    pdf.cell(w=22.5,h=22.1,align="C",txt=str(self.data.tax_list[i].get()*2))
                    pdf.cell(w=40.1,h=22.1,align="C",txt=str(self.data.total_posttax_list[i].get()))

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
        if(state):
            pdf_template = PdfFileReader(open("Wholesale_template_v3.pdf","rb"))
        else:
            pdf_template = PdfFileReader(open("wholesale_template_igst.pdf","rb"))
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
        
        pdfname = str(date.today())+str(self.data.inv_num.get())+str(self.data.cust_name.get())+".pdf"
        # pdfname = str(self.data.inv_num.get())+str(self.data.cust_name.get())+".pdf"
        self.data.filename = os.path.join(dirname, 'Bill_store/'+details.nam[self.firm]+'/'+pdfname)
        output_pdf.write(open(self.data.filename,'wb'))
        
        # os.startfile(filename, "print")
        os.startfile(self.data.filename, "open")
        return
    def clear(self):
        self.data.cust_name.set('')
        self.data.cust_add.set('')
        self.data.gst_num.set('')
        self.data.inv_num.set(self.data.inv_num.get()+1)
        for i in range(5):
            self.data.desc_list[i].set('')
            self.data.gram_list[i].set(0)
            self.data.mgram_list[i].set(0)
            self.data.rate_list[i].set(0)
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