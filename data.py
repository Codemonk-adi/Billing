from tkinter import StringVar,IntVar,DoubleVar
from datetime import date

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
        self.weight_list = [StringVar() for i in range(5)]
        self.rate_list = [StringVar() for i in range(5)]
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
        self.weight_list = [StringVar() for i in range(5)]
        self.rate_list = [StringVar() for i in range(5)]
        self.labour_list = [StringVar() for i in range(5)]
        self.total_list = [DoubleVar() for i in range(5)]
        self.total = StringVar()
        self.curr_date.set(date.today().strftime('%d/%m/%y'))
        self.payment_method = StringVar()
        # self.cust_name.set(str("Aadit"))
        self.bg_color = '#f8edeb'
        self.fg_color = '#C70039'
