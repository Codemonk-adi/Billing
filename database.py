import sqlite3 as sql
class Database():
    '''
    Class to store bills and user info.
    '''
    def __init__(self):        
        self.conn = sql.connect('AJ_DB.db')
        self.cur = self.conn.cursor()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
    def close(self):
        """Closes DB Connection."""
        self.cur.close()
        self.conn.close()
    def create_tables(self):
        """Creates Tables."""
        self.cur.executescript('''
        CREATE TABLE IF NOT EXISTS Retail_Cust(
            ID INTEGER ,
            NAME VARCHAR(255) NOT NULL,
            CONTACT_NO CHARACTER(10) NOT NULL,
            ADDRESS VARCHAR(511) NOT NULL,
            DOB DATE,
            PRIMARY KEY(ID)
            );

        CREATE TABLE IF NOT EXISTS Whole_Cust (
            ID INTEGER PRIMARY KEY ,
            NAME VARCHAR(255) NOT NULL,
            GST_NO CHAR(15) NOT NULL,
            ADDRESS VARCHAR(511) NOT NULL
            );

        CREATE TABLE IF NOT EXISTS Retail_Bill (
            ID INTEGER PRIMARY KEY ,
            INVOICE INTEGER,
            DATE DATE NOT NULL,
            CUST_ID INTEGER,
            TOTAL INTEGER,
            FOREIGN KEY (CUST_ID) REFERENCES Retail_Cust(ID)
            ON DELETE CASCADE
            );

        CREATE TABLE IF NOT EXISTS Retail_Particulars (
            ID INTEGER NOT NULL,
            BILL INTEGER NOT NULL,
            DESCR VARCHAR(255) NOT NULL,
            GRAM FLOAT NOT NULL,
            MILLIGRAM FLOAT NOT NULL,
            RATE INTEGER NOT NULL,
            LABOUR INTEGER NOT NULL,
            TOTAL FLOAT NOT NULL,
            FOREIGN KEY (BILL) REFERENCES Retail_Bill(ID)
            ON DELETE CASCADE,
            PRIMARY KEY (ID,BILL)
            );

        CREATE TABLE IF NOT EXISTS Whole_Bill (
            ID INTEGER PRIMARY KEY ,
            INVOICE INTEGER,
            FIRM VARCHAR(255) NOT NULL,
            DATE DATE NOT NULL,
            CUST_ID INTEGER,
            TOTAL INTEGER,
            FOREIGN KEY (CUST_ID) REFERENCES Whole_Cust(ID)
            ON DELETE CASCADE
            );

        CREATE TABLE IF NOT EXISTS Whole_Particulars (
            ID INTEGER ,
            BILL INTEGER,
            DESCR VARCHAR(255) NOT NULL,
            GRAM FLOAT NOT NULL,
            MILLIGRAM FLOAT NOT NULL,
            RATE INTEGER NOT NULL,
            FOREIGN KEY (BILL) REFERENCES Retail_Bill(ID)
            ON DELETE CASCADE,
            PRIMARY KEY (ID,BILL)
            );
        ''')
        self.conn.commit()
    def insert_retail_user(self,data_list):
        '''Inserts Retail User checks for duplicates via Contact no.'''
        u_id= self.cur.execute('''
                            select ID from retail_cust where CONTACT_NO=:contact
                            ''',data_list).fetchone()
        if u_id is None:
            u_id = self.cur.execute('''
                        INSERT INTO Retail_Cust(NAME,CONTACT_NO,ADDRESS) values(:name,:contact,:address) RETURNING ID;
                        ''',data_list).fetchone()
        self.conn.commit()
        return u_id[0]
    def insert_retail_bill(self,headers):
        '''Inserts Bill takes invoice, date,cust id, total amount.'''
        bill_id= self.cur.execute('''
                            select ID from Retail_Bill where INVOICE=:invoice AND DATE=:date
                            ''',headers).fetchone()
        if bill_id is None:
            bill_id = self.cur.execute("""
                        INSERT INTO Retail_BIll (INVOICE,DATE,CUST_ID,TOTAL) VALUES(:invoice,:date,:cust_id,:total) returning ID;
                        """,headers).fetchone()
        else:
            self.cur.execute("""
                        UPDATE Retail_BIll 
                        SET TOTAL=?,CUST_ID=?
                        WHERE ID =?
                        """,(headers['total'],headers['cust_id'],bill_id[0]))
        self.conn.commit()
        return bill_id[0]
    def insert_retail_bill_particulars(self,bill_id,particulars):
        '''Inserts particulars for a bill, deletes previous values if modified.'''
        if self.cur.execute('''
                        select exists (select * from retail_bill where id=:bill_id);
                        ''',{'bill_id':bill_id}).fetchone():
            self.cur.execute('''
                            delete from retail_particulars where BILL=:bill_id;
                            ''',{'bill_id':bill_id})
        self.cur.executemany('''
                        insert into retail_particulars (ID,BILL,DESCR,GRAM,MILLIGRAM,RATE,LABOUR,TOTAL) Values (?,?,?,?,?,?,?,?)
                        ''',particulars)
        self.conn.commit()
    def get_contact_id_list(self):
        '''Returns a list of (CONTACT_NO,ID).'''
        self.cur.execute('Select CONTACT_NO,ID from retail_cust')
        return self.cur.fetchall()
    def get_custdetails(self,cust_id):
        """Returns Name, Contact_no, Address given ID"""
        self.cur.execute(f'Select NAME,CONTACT_NO,ADDRESS from retail_cust WHERE ID = {cust_id} LIMIT 1')
        return self.cur.fetchall()
    def insert_whole_user(self,data_list):
        '''Inserts Wholesale User checks for duplicates via GST NO.'''
        u_id= self.cur.execute('''
                            select ID from whole_cust where GST_NO=:gst_no
                            ''',data_list).fetchone()
        if u_id is None:
            u_id = self.cur.execute('''
                        INSERT INTO whole_Cust(NAME,GST_NO,ADDRESS) values(:name,:gst_no,:address) RETURNING ID;
                        ''',data_list).fetchone()
        self.conn.commit()
        return u_id[0]
    def insert_whole_bill(self,headers):
        '''Inserts Bill takes invoice, firm,date,cust id, total amount.'''
        bill_id= self.cur.execute('''
                            select ID from Whole_Bill where INVOICE=:invoice AND DATE=:date AND FIRM=:firm
                            ''',headers).fetchone()
        if bill_id is None:
            bill_id = self.cur.execute("""
                        INSERT INTO Whole_Bill (INVOICE,FIRM,DATE,CUST_ID,TOTAL) VALUES(:invoice,:firm,:date,:cust_id,:total) returning ID;
                        """,headers).fetchone()
        else:
            self.cur.execute("""
                        UPDATE Whole_Bill 
                        SET TOTAL=?,CUST_ID=?
                        WHERE ID =?
                        """,(headers['total'],headers['cust_id'],bill_id[0]))
        self.conn.commit()
        return bill_id[0]
    def insert_whole_bill_particulars(self,bill_id,particulars):
        '''Inserts particulars for a bill, deletes previous values if modified.
            Takes ID,BILL_ID, Description, Grams, Milligrams, Rate for each particular
            in that order'''
        if self.cur.execute(f'''
                        select exists (select * from whole_bill where id={bill_id});
                        ''').fetchone():
            self.cur.execute(f'''
                            delete from whole_particulars where BILL={bill_id};
                            ''')
        self.cur.executemany('''
                        insert into whole_particulars (ID,BILL,DESCR,GRAM,MILLIGRAM,RATE) Values (?,?,?,?,?,?)
                        ''',particulars)
        self.conn.commit()
    def get_whole_name_id_list(self):
        '''Returns a list of (Name,ID).'''
        self.cur.execute('Select NAME,ID from whole_cust')
        return self.cur.fetchall()
    def get_whole_custdetails(self,cust_id):
        """Returns Name, GST_no, Address given ID"""
        self.cur.execute(f'Select NAME,GST_NO,ADDRESS from whole_cust WHERE ID = {cust_id} LIMIT 1')
        return self.cur.fetchall()
