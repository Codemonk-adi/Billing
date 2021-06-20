# from re import template
import sys
# import docx
from tkinter import*
from datetime import date
from fpdf import FPDF
from PyPDF2 import PdfFileReader,PdfFileWriter
import os
# -*- coding: utf-8 -*-


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
        
class Aj_billing(object):
    def __init__(self, root):
        self.root = root
        self.root.title("AJ")
        self.root.minsize(width=1370, height=720)
        # variables
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
        self.total_list = [IntVar() for i in range(5)]
        self.total = StringVar()
        self.curr_date.set(date.today().strftime('%d/%m/%y'))
        self.payment_method = StringVar()
        # self.cust_name.set(str("Aadit"))
        bg_color = "#000000"
        fg_color = "red"
        lbl_color = 'red'

        title = Label(self.root, text="Akash Jewellers",bd=12,fg=fg_color,bg=bg_color,font=("Calibri",36 , "bold"),pady=3).pack(fill=X)

        F1 = LabelFrame(text="Customer Information", font=("Calibri", 12, "bold"), fg="gold", bg=bg_color,
        relief=RAISED, bd=10)
        F1.place(x=0, y=80, relwidth=1)

        #for name
        customername_lbl = Label(F1, text="Customer Name", bg=bg_color, fg=fg_color,
        font=("Calibri", 15, "bold")).grid(row=0, column=0, padx=10, pady=5)
        customername_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.cust_name)
        customername_en.grid(row=0, column=1, ipady=4, ipadx=30, pady=5)
        
        # This function for customer contact number
        customercontact_lbl = Label(F1, text="Phone No", bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=2, padx=20)
        customercontact_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.cust_num)
        customercontact_en.grid(row=0, column=3, ipady=4, ipadx=30, pady=5)
        # This fucntion for Invoice Number
        customerinvoice_lbl = Label(F1, text="Invoice No.", bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(row=0, column=4, padx=20)
        customerinvoice_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.inv_num)
        customerinvoice_en.grid(row=0, column=5, ipadx=30, ipady=4, pady=5)

        # #button
        # invoice_btn = Button(F1, text="Enter", bd=7, relief=RAISED, font=("Calibri", 12, "bold"), bg=bg_color,
        # fg=fg_color)
        # invoice_btn.grid(row=0, column=6, ipady=5, padx=60, ipadx=19, pady=5)

        # This function for customer address
        customeraddress_lbl = Label(F1, text="Address", bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=1, column=0, padx=20)
        customeraddress_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.cust_add, width=50)
        customeraddress_en.grid(row=1, column=1, columnspan=2, ipady=4, ipadx=30, pady=5)
        

        #date
        date_lbl = Label(F1,text="Date", bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=1, column=3, padx=20)
        date_en = Entry(F1, bd=8, relief=RAISED, textvariable=self.curr_date, width=15)
        date_en.grid(row=1, column=4,ipady=4, ipadx=5, pady=5)

        F2 = LabelFrame(self.root, text='Details',bd=10,relief=RAISED,bg=bg_color, fg='gold', font=("Calibri",18,"bold"))
        F2.place(x=0,y=210, relwidth=0.72, height=380)
        
        Fpre = LabelFrame(self.root, text='Preview',bd=10,relief=RAISED,bg=bg_color, fg='gold', font=("Calibri",18,"bold"))
        Fpre.place(relx=0.72,y=210, relwidth=0.28, height=380)
        # root.columnconfigure(0,1)
        
        F4 = LabelFrame(self.root,text="Result",bd=10,relief=RAISED,bg=bg_color, fg='gold', font=("Calibri",18,"bold"))
        F4.place(y=590,relwidth=1)

        desc_lbl = Label(F2,text="Particulars", bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        description_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.desc_list[0])
        description_0.grid(row=1,column=0,padx=5, pady=10, ipady=5, ipadx=5)
        description_1 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.desc_list[1])
        description_1.grid(row=2,column=0,padx=5, pady=10, ipady=5, ipadx=5)
        description_2 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.desc_list[2])
        description_2.grid(row=3,column=0,padx=5, pady=10, ipady=5, ipadx=5)
        description_3 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.desc_list[3])
        description_3.grid(row=4,column=0,padx=5, pady=10, ipady=5, ipadx=5)
        description_4 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.desc_list[4])
        description_4.grid(row=5,column=0,padx=5, pady=10, ipady=5, ipadx=5)

        W_gram_lbl = Label(F2, text="Gram",bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        gram_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.gram_list[0])
        gram_0.grid(row=1,column=1,padx=2, pady=10, ipady=5, ipadx=2)
        gram_1 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.gram_list[1])
        gram_1.grid(row=2,column=1,padx=2, pady=10, ipady=5, ipadx=2)
        gram_2 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.gram_list[2])
        gram_2.grid(row=3,column=1,padx=2, pady=10, ipady=5, ipadx=2)
        gram_3 = Entry(F2,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.gram_list[3])
        gram_3.grid(row=4,column=1,padx=2, pady=10, ipady=5, ipadx=2)
        gram_4 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.gram_list[4])
        gram_4.grid(row=5,column=1,padx=2, pady=10, ipady=5, ipadx=2)

        W_milli_gram_lbl = Label(F2, text="Milli Gram",bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=2, padx=20)
        mgram_0 = Entry(F2,relief=RAISED,textvariable=self.mgram_list[0],bg="pink",font=('Calibri', 18, "bold"))
        mgram_0.grid(row=1,column=2,padx=2, pady=10, ipady=5, ipadx=2)
        mgram_1 = Entry(F2,relief=RAISED,textvariable=self.mgram_list[1],font=('Calibri', 18, "bold"))
        mgram_1.grid(row=2,column=2,padx=2, pady=10, ipady=5, ipadx=2)
        mgram_2 = Entry(F2,relief=RAISED,textvariable=self.mgram_list[2],bg="pink",font=('Calibri', 18, "bold"))
        mgram_2.grid(row=3,column=2,padx=2, pady=10, ipady=5, ipadx=2)
        mgram_3 = Entry(F2,relief=RAISED,textvariable=self.mgram_list[3],font=('Calibri', 18, "bold"))
        mgram_3.grid(row=4,column=2,padx=2, pady=10, ipady=5, ipadx=2)
        mgram_4 = Entry(F2,relief=RAISED,textvariable=self.mgram_list[4],bg="pink",font=('Calibri', 18, "bold"))
        mgram_4.grid(row=5,column=2,padx=2, pady=10, ipady=5, ipadx=2)

        rate_lbl = Label(F2, text="Rate(per gram)",bg=bg_color, fg=fg_color,font=("Calibri", 15, "bold")).grid(row=0, column=3, padx=20)
        rate_0 = Entry(F2,relief=RAISED,textvariable=self.rate_list[0],bg="pink",font=('Calibri', 18, "bold"))
        rate_0.grid(row=1,column=3,padx=2, pady=10, ipady=5, ipadx=2)
        rate_1 = Entry(F2,relief=RAISED,textvariable=self.rate_list[1],font=('Calibri', 18, "bold"))
        rate_1.grid(row=2,column=3,padx=2, pady=10, ipady=5, ipadx=2)
        rate_2 = Entry(F2,relief=RAISED,textvariable=self.rate_list[2],bg="pink",font=('Calibri', 18, "bold"))
        rate_2.grid(row=3,column=3,padx=2, pady=10, ipady=5, ipadx=2)
        rate_3 = Entry(F2,relief=RAISED,textvariable=self.rate_list[3],font=('Calibri', 18, "bold"))
        rate_3.grid(row=4,column=3,padx=2, pady=10, ipady=5, ipadx=2)
        rate_4 = Entry(F2,relief=RAISED,textvariable=self.rate_list[4],bg="pink",font=('Calibri', 18, "bold"))
        rate_4.grid(row=5,column=3,padx=2, pady=10, ipady=5, ipadx=2)

        
        # Fr.columnconfigure(0,weight=1)
        
        
        labour_charge_lbl = Label(F2, text="Labour",bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=4, padx=20)
        labour_charge_0 = Entry(F2,relief=RAISED,bg="pink",font=('Calibri', 18, "bold"),textvariable=self.labour_list[0])
        labour_charge_0.grid(row=1,column=4,padx=2, pady=10, ipady=5, ipadx=2)
        labour_charge_1 = Entry(F2,relief=RAISED,textvariable=self.labour_list[1],font=('Calibri', 18, "bold"))
        labour_charge_1.grid(row=2,column=4,padx=2, pady=10, ipady=5, ipadx=2)
        labour_charge_2 = Entry(F2,relief=RAISED,textvariable=self.labour_list[2],bg="pink",font=('Calibri', 18, "bold"))
        labour_charge_2.grid(row=3,column=4,padx=2, pady=10, ipady=5, ipadx=2)
        labour_charge_3 = Entry(F2,relief=RAISED,textvariable=self.labour_list[3],font=('Calibri', 18, "bold"))
        labour_charge_3.grid(row=4,column=4,padx=2, pady=10, ipady=5, ipadx=2)
        labour_charge_4 = Entry(F2,relief=RAISED,textvariable=self.labour_list[4],bg="pink",font=('Calibri', 18, "bold"))
        labour_charge_4.grid(row=5,column=4,padx=2, pady=10, ipady=5, ipadx=2)
        
        # Fl.columnconfigure(0,weight=1)

        total_lbl = Label(F4, text="Total",bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=0, padx=20)
        total_en = Entry(F4,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.total)
        total_en.grid(row=1,column=0,padx=5)
        #payment methods
        payment_lbl = Label(F4, text="Payment Method",bg=bg_color, fg=fg_color, font=("Calibri", 15, "bold")).grid(
        row=0, column=1, padx=20)
        payment_en = Entry(F4,relief=RAISED,font=('Calibri', 18, "bold"),textvariable=self.payment_method).grid(row=1,column=1,padx=5)

        #buttons
        total_btn = Button(F4, text="Total", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED,
        command=self.total_section)
        total_btn.grid(row=1, column=4, ipadx=20, padx=30)
        
        # This function for Generate Bill
        generatebill_button = Button(F4, text="Generate Bill", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.billing_section)
        generatebill_button.grid(row=1, column=5, ipadx=20)
        
        # This function for Clear Button
        clear_button = Button(F4, text="Clear", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.clear)
        clear_button.grid(row=1, column=6, ipadx=20, padx=30)
        
        # This function for Exit Button
        exit_buttonn = Button(F4, text="Exit", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7, relief=RAISED, command=self.exit)
        exit_buttonn.grid(row=1, column=7, ipadx=20)
        
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
            if(self.labour_list[i].get() != 0):
                self.total_list[i].set((self.gram_list[i].get() +(self.mgram_list[i].get()/1000))*(self.rate_list[i].get()+self.labour_list[i].get())*1.03)
                total+=self.total_list[i].get()
        self.total.set(int(total))
        return
    def welcome_customer(self):
        return
    def clear(self):
        self.cust_name.set('')
        self.cust_add.set('')
        self.cust_num.set('')
        self.inv_num.set(self.inv_num.get()+1)
        self.total.set('')
        for i in range(5):
            self.desc_list[i].set('')
            self.gram_list[i].set(0)
            self.mgram_list[i].set(0)
            self.rate_list[i].set(0)
            self.labour_list[i].set(0)
            self.total_list[i]=0
        return
        # This function for Add Product name , qty and price to bill section
        
    def billing_section(self):
        self.total_section()
        pdf=FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_font('Times_uni',fname="Quivira.otf",uni=True)
        pdf.add_page()
        pdf.set_font("Times_uni",size=11)
        #Invoice Number
        pdf.set_xy(45.7,54.8)
        pdf.cell(w=41.4,h=7.1,align='L',txt=str(self.inv_num.get()))
        #Date
        pdf.set_xy(149.4,54.8)
        pdf.cell(w=35.7,h=7.1,txt=self.curr_date.get())
        #Name
        pdf.set_xy(37.8,62.7)
        pdf.cell(w=56.4,h=7.1,txt=self.cust_name.get())
        #Address
        pdf.set_xy(41.1,69.6)
        pdf.multi_cell(w=58.9,h=8.1,txt=self.cust_add.get())
        #Contact Number
        pdf.set_xy(166.7,69.6)
        pdf.cell(w=39.1,h=8.1,txt=self.cust_num.get())
        
        #Details
        for i in range(5):
            if(self.labour_list[i].get() != 0):
                pdf.set_xy(13,22.1*i+99.8)
                pdf.multi_cell(w=51.8,h=22.1,align="C",txt=self.desc_list[i].get())
                pdf.set_xy(65,22.1*i+99.8)
                pdf.cell(w=14,h=22.1  ,align="C",txt=str(self.gram_list[i].get()))
                pdf.cell(w=14,h=22.1  ,align="C",txt=str(self.mgram_list[i].get()))
                pdf.cell(w=23.4,h=22.1,align="C",txt=str(self.rate_list[i].get()))
                pdf.cell(w=27.7,h=22.1,align="C",txt=str(self.labour_list[i].get()))
                pdf.cell(w=24.6,h=22.1,align="C",txt="3%")
                pdf.cell(w=33.8,h=22.1,align="C",txt=str(self.total_list[i].get()))
        
        #Payment Method
        pdf.set_xy(15.7,239.5)
        pdf.set_font(family="Times_uni",size=12)
        pdf.cell(w=29.2,h=7.9,txt=self.payment_method.get())
        
        #Total
        pdf.set_xy(169.2,233.4)
        format_total=""
        total_copy = int(self.total.get())
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
        # print(format_total.encode().decode(encoding='utf-8'))
        pdf.cell(w=34,h=18.3,txt=format_total)
        
        pdf.output("temp.pdf")
        pdf.close()
        
        pdf_template = PdfFileReader(open("bill_temp_v3.pdf","rb"))
        template_page = pdf_template.getPage(0)
        overlay_pdf=    PdfFileReader(open("temp.pdf",'rb'))
        template_page.mergePage(overlay_pdf.getPage(0))
        output_pdf = PdfFileWriter()
        output_pdf.addPage(template_page)
        os.makedirs("Bill_store",exist_ok=True)
        dirname = os.path.dirname(__file__)
        pdfname = str(self.inv_num.get())+str(self.cust_name.get())+".pdf"
        filename = os.path.join(dirname, 'Bill_store/'+pdfname)
        output_pdf.write(open(filename,'wb'))
        os.startfile(filename, "print")
        os.startfile(filename, "open")
        
        return
    
    def exit(self):
        self.root.destroy()
        return
    
root = Tk()
object = Aj_billing(root)
root.mainloop()