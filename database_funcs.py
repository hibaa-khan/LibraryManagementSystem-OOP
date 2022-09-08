import sqlite3

def add_rec(name_of_db,name_of_table="",*x):
    conn= sqlite3.connect(name_of_db)
    c= conn.cursor()
    if len(x)==6:
        c.execute(f'INSERT INTO "{name_of_table}" VALUES (?,?,?,?,?,?)',x)
    elif len(x)==4:
        c.execute(f'INSERT INTO "{name_of_table}" VALUES (?,?,?,?)',x)
    conn.commit()
    conn.close

def showAll(name_of_db,name_of_table=""):
    conn = sqlite3.connect(name_of_db)
    c=conn.cursor()
    c.execute(f'SELECT * FROM {name_of_table} ')
    x=(c.fetchall())
    return (x)
    conn.commit()
    conn.close()

def show_rec(name_of_db="",name_of_table="",ID=0):
    conn= sqlite3.connect(name_of_db)
    c = conn.cursor()
    all_data=showAll(name_of_db,name_of_table)
    flag=0
    for i in all_data:
        if ID in i:
            rec=(list(i))
        else:
            flag+=1
    if flag==len(all_data):
        return []
    else:
        return rec
    conn.commit()
    conn.close()
    

def delete_rec(name_of_db="",name_of_table="",col="",x=""):
    conn =sqlite3.connect(name_of_db)
    c= conn.cursor()
    c.execute(f'DELETE FROM "{name_of_table}" WHERE "{col}" = "{x}"')   
    conn.commit()
    conn.close()


def update_rec(name_of_db="",name_of_table="",record=[], with_val=0,what_val=0): 
    conn= sqlite3.connect(name_of_db)
    c = conn.cursor()
    flag = 0
    count=0
    for i in record:
        if str(i) == str(what_val):
            record[count]=str(with_val)
        else:
            count+=1
            flag += 1
    if flag == len(record):
        print("The value you want to change doesn't exist")            ##isko kesey replace kron???
    else:
        if name_of_db=="Books.db":                
            delete_rec(name_of_db,name_of_table,"Book_ID",record[2])
            add_rec(name_of_db,name_of_table,record[0],record[1],record[2],record[3])
        elif name_of_db=="Student.db":
            delete_rec(name_of_db,name_of_table,"user",record[3])
            add_rec(name_of_db,name_of_table, record[0],record[1],record[2],record[3],record[4],record[5])
        conn.commit()
        conn.close()


def search_rec(name_of_db,name_of_table="",col="",x=""):
    conn= sqlite3.connect(name_of_db)
    c = conn.cursor()
    c.execute(f'SELECT * FROM "{name_of_table}" WHERE "{col}" = "{x}"')
    x=(c.fetchall())
    return x        ## return a tuple of a record
    conn.commit()
    conn.close()

