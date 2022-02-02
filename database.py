import sqlite3 as sql
#to be saved
print(sql.sqlite_version)
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
        PRAGMA foreign_keys = ON;
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
        CREATE TABLE IF NOT EXISTS Categories (
            ID INTEGER PRIMARY KEY ,
            _Name varchar(255)
            );
            
		CREATE TABLE IF NOT EXISTS Alias(
			ID integer primary key,
            _Name varchar(255),
            category integer,
            foreign key (category) references Categories(ID)
            On delete cascade
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
                        ''').fetchone()[0]:
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
    def insert_categories(self,category:str):
        """Inserts a category and returns its ID."""
        temp = self.cur.execute(f'''
                        select exists (select * from categories where _Name="{category.title()}");
                        ''').fetchone()[0]
        if not temp:
            self.cur.execute(f'insert into categories(_Name) values ("{category.title()}") returning ID')
        var = self.cur.fetchone()
        self.conn.commit()
        if var:
            return var[0]
        else:
            return None
    def insert_alias(self,category_id:int,alias: str):
        """Inserts Alias for given Category ID"""
        if not self.cur.execute(f'''
                        select exists (select * from alias where _Name="{alias.title()}");
                        ''').fetchone()[0]:
            self.cur.execute(f'insert into alias(_Name,category) values ("{alias.title()}",{category_id})')
        self.conn.commit()
    def get_category_lists(self):
        """Returns Pairs of Category/Alias Name, Parent ID."""
        self.cur.execute('''
                        Select _Name,ID from categories
                        UNION
                        Select _Name,category from alias
                        ''')
        return self.cur.fetchall()
    def get_category_lists_s(self):
        self.cur.execute('''
                        Select _Name,ID from categories
                        ''')
        return self.cur.fetchall()
    def get_category_name(self,category:int):
        """Returns the name of the category given its id."""
        self.cur.execute(f'''
                        select _Name from categories where ID={category} 
                        ''')
        return self.cur.fetchone()[0]
    
    def get_category_id(self,category:str):
        """Returns the id of the category given its Name."""
        self.cur.execute(f'''
                        select ID from categories where _Name="{category}" 
                        ''')
        return self.cur.fetchone()
    def get_alias_id(self,alias:str):
        """Returns the id of the alias given its Name."""
        self.cur.execute(f'''
                        select ID from alias where _Name="{alias}" 
                        ''')
        return self.cur.fetchone()
    def get_aliases(self,category:int):
        """Returns all the aliases of the given id."""
        self.cur.execute(f'''
                        Select _Name from alias where category={category}
                        ''')
        return self.cur.fetchall()
    def del_categoty(self,category:int):
        """Deletes Category with the given ID."""
        self.cur.execute(f'''
                        Delete from categories where ID = {category}
                        ''')
        self.conn.commit()
    def del_alias(self,alias_id:int):
        """Deletes a particular alias given ID."""
        self.cur.execute(f'''
                        Delete from alias where ID = {alias_id}
                        ''')
        self.conn.commit()
        