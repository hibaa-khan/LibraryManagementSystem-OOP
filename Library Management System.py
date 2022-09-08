from abc import ABC, abstractmethod
import sqlite3
import sys


class Functions:
    """Functions has all static methods.

    Contains all the methods to implement database functions.
    """
    
    @staticmethod  
    def add_rec(name_of_db, name_of_table="", *x):
        """Adds the records to the databases.

        Takes the arguments of the name of database and the table in
        which the values are to be added. The values to be added are
        passed as the args and then inserted into the table.
        """
        conn = sqlite3.connect(name_of_db)
        c = conn.cursor()
        ## in our code, the tables either have 6 columns, or 4 hence, the check
        if len(x) == 6:
            c.execute(f'INSERT INTO "{name_of_table}" VALUES (?,?,?,?,?,?)', x)  
        elif len(x) == 4:
            c.execute(f'INSERT INTO "{name_of_table}" VALUES (?,?,?,?)', x)
        conn.commit()
        conn.close()

    @staticmethod
    def showAll(name_of_db,name_of_table=""):
        """Returns all the records present in a table, as tuples, in a main list.

        Takes the arguments of the name of database and the name of
        the table, for the data to be fetched from.
        """
        conn = sqlite3.connect(name_of_db)
        c=conn.cursor()
        c.execute(f'SELECT * FROM {name_of_table} ')  ## builtin query statment of sqlite3
        x=(c.fetchall())
        conn.close()
        return (x)

    @staticmethod
    def show_rec(name_of_db="",name_of_table="",search_val=0):
        """Takes the arguments of the name of database and the name of
        the table, and the value to search, from any column.

        Returns the list of the record if the value is found in any,
        else returns an empty list. 
        """
        conn= sqlite3.connect(name_of_db)
        c = conn.cursor()
        all_data=Functions.showAll(name_of_db,name_of_table)
        flag=0
        for i in all_data:
            if search_val in i:            ## searches for target data in all data
                rec=(list(i))              ## converts the target data into list
            else:
                flag+=1                    ## increments flag
        if flag==len(all_data):
            return []                      ## if target data is not found, returns empty list
        else:
            conn.close()
            return rec

    @staticmethod
    def delete_rec(name_of_db="",name_of_table="",col="",x=""):
        """Just deletes the record from the table.

        Takes the argument of the name of database and the name of the
        table, along with the name of column and the value whose record
        is to be deleted. If the value is found, the record is deleted.
        """
        conn =sqlite3.connect(name_of_db)
        c= conn.cursor()
        c.execute(f'DELETE FROM "{name_of_table}" WHERE "{col}" = "{x}"')    ## built in query statement of sqlite3
        conn.commit()
        conn.close()

    @staticmethod
    def update_rec(name_of_db="",name_of_table="",record=[], with_val=0,what_val=0):
        """Updates a record of the table.

        Takes the argument of name of database, name of table, the
        record to be updated (of list data type), the value to be
        changed, and the new value.
        """
        conn= sqlite3.connect(name_of_db)
        c = conn.cursor()
        flag = 0
        count=0                     ## used to keep track of the indexes
        for i in record:
            if str(i) == str(what_val):               ## searches for the value to change in the target record
                record[count]=str(with_val)           ## changes the old value by new value, using its index
            else:
                count+=1
                flag += 1
        if flag == len(record):
            print("The value you want to change doesn't exist")
        else:
            ## in our code, the tables either have 6 columns, or 4 hence, the check
            if name_of_db=="Books.db":                
                Functions.delete_rec(name_of_db,name_of_table,"Book_ID",record[2])
                Functions.add_rec(name_of_db,name_of_table,record[0],record[1],record[2],record[3])
            elif name_of_db=="Student.db":
                Functions.delete_rec(name_of_db,name_of_table,"user",record[3])
                Functions.add_rec(name_of_db,name_of_table, record[0],record[1],record[2],record[3],record[4],record[5])
            conn.commit()
            conn.close()

    @staticmethod
    def search_rec(name_of_db,name_of_table="",col="",x=""):
        """Returns a tuple of the data that was to be searched.

        Takes the argument of name of database and table, where the
        required data is present. Also takes the argument of the column
        to be searched in, and the value to be searched.
        """
        conn= sqlite3.connect(name_of_db)
        c = conn.cursor()
        c.execute(f'SELECT * FROM "{name_of_table}" WHERE "{col}" = "{x}"')       ##  built in query statement of sqlite3
        x=(c.fetchall())
        conn.close()
        return x        # returns a tuple of a record


class User(ABC):
    """Serves as the abstract class for Admin and Student.

    Has three abstract methods. 
    """
    @abstractmethod
    def Sign_in(self):
        """An anstract method to sign in with already set user ID and
        password.
        """
        pass
    
    @abstractmethod
    def Sign_up(self):
        """An anstract method to sign up and create a new account, by
        providing basic self information. 
        """
        pass
    
    @abstractmethod
    def open_menu(self):
        """An abstract method to display the main menu and acts
        as the user interface for the whole application.
        """
        pass


class Admin (User,Functions):
    """Inherits from User and Functions.

    Overrides all the abstract methods provided in the base class.
    """
    def __init__(self):
        """Calls the Sign_in() method.
        """
        self.Sign_in()
        
    def Sign_in(self):
        """Provides the log in procedure for Admin.
        """
        flag=1
        while flag:              ## loop for ID and password
            self.name=input("""To log in as Admin:
Enter username: """)
            self.password=input("Enter password: ")
            if self.name== "LibraryAdmin" and self.password=="Admin_123":
                print ('You have Successfully Logged in!')
                self.open_menu()
                flag=0
            else:
                print("""Username or password is incorrect.
To try again, press 1,
to return to the main menu, press  2,
to exit the program, press 3.""") 
                while True:       ## loop for input choice
                    try:
                        c=int(input("Enter choice: "))                               
                    except ValueError:
                        print ("Please Enter an integer between 1 to 3 inclusive.")
                        continue                                 
                    if c==1:
                        self.Sign_in()
                        break
                    elif c==2:
                        Login.main_menu(self)
                        break
                    elif c==3:
                        print("Bye Bye!")
                        sys.exit()
                    else:
                        print("Please Enter an integer between 1 to 3 inclusive.")
                        continue
                    
    def Sign_up(self):## The admin can only sign in, and can not create a new admin account. 
        """The admin can not create a new account, hence no
        implementation of it is given. 
        """
        pass

    def open_menu(self):           ## Admin menu
        """Opens the main menu panel for the admin.
        """
        print("""Welcome Admin
Menu:
1. Add Books
2. Show all books available in the library
3. Show all borrowed books
4. Delete Books
5. Update Book Information
6. Search Book
7. Show all students
8. Search Student
9. Delete Student
10. Log out""")
        while True:          # main loop for admin menu
            try:
                option=int(input("Enter Option Number: "))
            except ValueError:
                print("Enter an integer from 1 to 10 inclusive.")
                continue
            
            if option == 1:   # adds new book record
                x=1
                while x :          # nested loop for currect data entry to add records
                    try:
                        n=input("Enter title of book: ")
                        a=input("Enter author's name: ")
                        ID=int(input("Enter Book_ID: "))
                        no=input("Enter the number of copies of this book available: ")
                    except ValueError:
                        print("Please enter valid values")
                        continue
                    info=Functions.show_rec("Books.db","All_Books_Rec",ID)      # searches for entered book ID
                    if len(info)==0:                                       # checks if book ID exists or not
                        Functions.add_rec("Books.db","All_Books_Rec",n,a,ID,no)
                        print("New Book information successfully added!")
                        x=0
                    else:
                        print("A book with the same ID already exists.")
                    
            elif option == 2:       # show records of all books
                all_data=Functions.showAll("Books.db","All_Books_Rec")
                print("Book Title                      Book Author                        Book ID                     No. of copies available")
                if len(all_data)!=0:                                       # checks if data is present in table or not
                    for i in all_data:
                        print(f'{i[0]:30}  {i[1]:20}  {i[2]:20}  {i[3]:20}')
                else:
                    print("There are no Books saved in the system right now.")   # should provide pre entered data????
                    
            elif option == 3:       # show all records of borrowed books
                borr_data= Functions.showAll("Books.db","Borrowed_Books_Rec")
                print("Book Title                      Book Author                        Book ID                     Name of borrower")
                space=""
                if len(borr_data)!=0:                                      # checks if data is present in table or not
                    for i in borr_data:
                        print(f'{i[0]:30}  {i[1]:20}  {i[2]:20}  {space:17}  {i[3]:20}')
                else:
                    print("No books are borrowed yet.")
                    
            elif option == 4:       # delete a book record by Book ID
                while True:
                    try:
                        ID=int(input("Enter the Book ID of the book that you want to delete: "))
                        break
                    except:
                        print("Pleasae enter an integer Book_ID")
                        continue
                rec=Functions.show_rec("Books.db","All_Books_Rec",ID)            # to check if book ID exists
                if len(rec)==0:
                    print("The Book ID doesn't exist")
                else:
                    Functions.delete_rec("Books.db","All_Books_Rec","Book_ID",ID)
                    print("Record successfully deleted!") 
                    
            elif option == 5:       # update a book record
                while True:
                    try:
                        ID=int(input("Enter the ID of the book that you want to update: ")) 
                        break
                    except:
                        print("Please enter an integer Book ID.")
                        continue                        
                rec=Functions.show_rec("Books.db","All_Books_Rec",ID)            # to check if Book ID exists
                if len(rec)==0:
                    print("The Book ID doesn't exist")
                else:
                    print("Book Title                      Book Author                        Book ID                     No. of copies available")
                    print(f'{rec[0]:30}  {rec[1]:20}  {rec[2]:20}  {rec[3]:20}')
                    what_val=input("Enter the value you want to update: ")
                    with_val=input("Enter the new value: ")
                    Functions.update_rec("Books.db","All_Books_Rec",rec,with_val,what_val)
                    print("Record successfully updated!")
                
            elif option == 6:       # search books by book ID
                while True:
                    try:
                        ID=int(input("Enter the Book ID of the book that you want to search: "))
                        break
                    except:
                        print("Pleasae enter an integer Book ID")
                        continue
                rec=Functions.show_rec("Books.db","All_Books_Rec",ID)
                if len(rec)==0:
                    print("The Book ID doesn't exist")
                else:
                    search=Functions.search_rec("Books.db","All_Books_Rec","Book_ID" ,ID)
                    print("Book Title                      Book Author                        Book ID                     No. of copies available")
                    for i in search:
                        print(f'{i[0]:30}  {i[1]:20}  {i[2]:20}  {i[3]:20}')

            elif option == 7:        # show all records of registered students
                all_data=Functions.showAll("Student.db","Student_Rec")
                print("Student Record: ")
                print("First Name            Last Name             Email address         Username              Password              History")
                if len(all_data)!=0:
                    for i in all_data:
                        print(f'{i[0]:20}  {i[1]:20}  {i[2]:20}  {i[3]:20}  {i[4]:20}  {i[5]:20}')
                else:
                    print("No Students are registered yet.")

            elif option == 8:        # search students by email
                email=input("Enter the email address of the student that you want to search: ")
                rec=Functions.show_rec("Student.db","Student_Rec",email)
                if len(rec)==0:
                    print("The email address doesn't exist")
                else:
                    print("First Name            Last Name             Email address         Username              Password              History")
                    search=Functions.search_rec("Student.db","Student_Rec","email" ,email)
                    for j in search:
                        print(f'{i[0]:20}  {i[1]:20}  {i[2]:20}  {i[3]:20}  {i[4]:20}  {i[5]:20}')

            elif option == 9:       # delete a record of student by their username
                while True:
                    uname=input("Enter the User name of the student that you want to delete: ")
                    rec=Functions.show_rec("Student.db","Student_Rec",uname)
                    if len(rec)==0:
                        print("This username doesn't exist")
                        continue
                    elif len(uname)==0:
                        print("Enter the username please")
                        continue
                    else:
                        Functions.delete_rec("Student.db","Student_Rec","user",uname)       
                        print("Record successfully deleted!")
                        break
            
            elif option == 10:      # log out
                print("""Logged out successfully!
Press 1 to log in to another account, press any other key to exit the application: """, end="")
                key=input()
                if key == "1":                 # return to main menu
                    Login.main_menu(self)
                else:                          # exit application
                    print("Bye Bye!")
                    sys.exit()      
            else:
                print("Enter an in integer from 1 to 10 inclusive")
                continue
            

class Student(User,Functions):
    """Inherits from User and Functions.

    Overrides all the abstract methods provided in the base class.
    """
    def __init__(self):
        """Allows the user to either log in, or create a new account.
        """
        self.info=[]
        print("""Hello Student. Please,
hit 1 to log in to your account,
hit 2 to create account.""",end = "")   
        while True:          # loop for correct input of choice to log in or create account
            try:
                c=int(input())
            except ValueError:
                print("Enter either 1 or 2")
                continue    
            if c==1:
                self.Sign_in()
            elif c==2:
                self.Sign_up()
            else:
                print("Enter either 1 or 2")
            
    def Sign_in(self):
        """Provides the Login procedure for Student.
        """
        flag=1
        while flag:              # loop for ID and password
            un=input("""To log in as Student:
Enter username: """)
            p=input("Enter password: ")
            self.name=un
            self.password=p
            conn = sqlite3.connect("Student.db")
            c = conn.cursor()
            c.execute(f'SELECT * FROM Student_Rec WHERE user == "{self.name}" AND pw== "{self.password}"')
            rec=c.fetchall()
            conn.commit()
            conn.close()
            if len(rec)==1:
                print("Login Successful!")
                self.info=[self.name,self.password]
                self.open_menu()
                flag=0
            else:
                print("""Incorrect username or password :(
To try again, press 1,
to return to the main menu, press  2,
to create a new account, press 3,
to exit the program, press 4.""") 
                while True:
                    try:
                        c=int(input("Enter choice: "))                               
                    except ValueError:
                        print ("Please Enter an integer between 1 to 4 inclusive.")
                        continue                                 
                    if c==1:
                        self.Sign_in()
                        break
                    elif c==2:
                        Login.main_menu(self)
                        break
                    elif c==3:
                        self.Sign_up()
                    elif c==4:
                        print("Bye Bye!")
                        sys.exit()
                    else:
                        print("Please Enter an integer between 1 to 4 inclusive.")
                        continue

    def Sign_up(self):
        """Provides the Signup procedure for Student.
        """
        print("Welcome new user. Please enter your informaion to create account.")
        nf=input("Enter first name: ")
        nl=input("Enter last name: ")
        e=input("Enter email address: ")
        uname=1
        while uname:           ## to ensure unique usernames
            self.name=input("Enter the username you want to set: ")
            rec=Functions.show_rec("Student.db","Student_Rec",self.name)
            if len(rec)==0:
                break
            else:
                print("The username already exists. Please try another username.")
                continue
        pw=1
        while pw:              ## to make sure passwords match
            p1=input("Enter password: ")
            p2=input("Re enter password: ")
            if p1!=p2:
                print("Passwords do not match.")
                continue
            else:
                self.password=p1
                Functions.add_rec("Student.db","Student_Rec",nf,nl,e,self.name,self.password,"")  
                print("Account Successfully created!")
                self.info=[self.name,self.password]
                self.open_menu()
                pw=0

    def open_menu(self):
        """Opens the main menue panel for the Student.
        """
        print("""Welcome Student
Menu:
1. Show all books available in the library
2. Borrow a Book
3. Return a Book
4. History of borrowed books
5. Update Self Information
6. Log out""")
        while True:          ## main loop for admin menu
            try:
                option=int(input("Enter Option Number: "))
            except ValueError:
                print("Enter an integer from 1 to 10 inclusive.")
                continue
            
            if option == 1:   ## shows records of all books      
                all_data=Functions.showAll("Books.db","All_Books_Rec")
                print("Book Title                      Book Author                        Book ID")
                for i in all_data:
                    if i[3]!=0:
                        print(f'{i[0]:30}  {i[1]:20}  {i[2]:20}')
                    
            elif option == 2:    ##allows to borrow a book
                borr_data=Functions.search_rec("Books.db","Borrowed_Books_Rec","borrower",self.info[0])
                if len(borr_data)==0:     ## to make sure a user borrows only one book at a time
                    while True:
                        ID=str(input("Enter the Book ID of the book, or press any letter to see all books: "))  
                        if  not ID.isdigit():
                            all_data=Functions.showAll("Books.db","All_Books_Rec")
                            print("Book Title                      Book Author                        Book ID")
                            for i in all_data:
                                if i[3]!=0:         ## displaying available books only
                                    print(f'{i[0]:30}  {i[1]:20}  {i[2]:20}')
                                    continue
                        else:
                            ID=int(ID)
                            rec=Functions.show_rec("Books.db","All_Books_Rec",ID)
                            if len(rec)==0:
                                print("The Book ID doesn't exist")
                                break
                            else:
                                search=Functions.search_rec("Books.db","All_Books_Rec","Book_ID" ,ID)  # if user enters Book_ID of the book thats currently all borrowed
                                if(search[0][3])==0:
                                    print("Currently, there are no copies of this book available."
                                          " Please come back later!")
                                    break
                                else:
                                    print("Book Title                      Book Author                        Book ID")
                                    for i in search:
                                        print(f'{i[0]:30}  {i[1]:20}  {i[2]:20}')
                                    lst_search=[i[0],i[1],i[2],i[3]]
                                    confirm=input("Press *1* to confirm. Else press *0* search another book: ")
                                    if confirm == "0":
                                        continue
                                    elif confirm=="1":
                                        Functions.add_rec("Books.db","Borrowed_Books_Rec",i[0],i[1],i[2],self.info[0])
                                        with_val_copies=int(i[3])-1
                                        Functions.update_rec("Books.db","All_Books_Rec",lst_search,with_val_copies,i[3])
                                        student_data=Functions.search_rec("Student.db","Student_Rec","user",self.info[0]) ## returns tuple form
                                        for j in student_data:
                                            lst_student_data=[j[0],j[1],j[2],j[3],j[4],j[5]]
                                            if lst_student_data[5]=="":     ## overwrites the default "" 
                                                hist=str(i[2])
                                            else:
                                                hist=str(lst_student_data[5])+","+str(i[2])
                                            Functions.update_rec("Student.db","Student_Rec",lst_student_data,hist,j[5])
                                        print("Book Borrowed!")
                                        break  
                                    else:
                                        print("Enter either 1 or 0 only")       
                                        continue
                else:
                    print("You can not borrow another book before returning the first one.")

            elif option == 3:   ## return a borrowed book
                borr_data=Functions.search_rec("Books.db","Borrowed_Books_Rec","borrower",self.info[0])
                if len(borr_data)==0:     ## to make sure a user has a borrowed book
                    print("There are no borrowed books. ")
                else:
                    print("Book Title                      Book Author                        Book ID")
                    for i in borr_data:
                        print(f'{i[0]:30}  {i[1]:20}  {i[2]:20}') ## [title, aname, Book_ID] i[3] is user
                        c=input("Enter Y to confirm the return: ")
                        if c=="y" or c=="Y":
                            Functions.delete_rec("Books.db","Borrowed_Books_Rec","borrower",self.info[0])
                            book_rec=Functions.search_rec("Books.db","All_Books_Rec","Book_ID" ,i[2])
                            for j in book_rec:
                                lst_book_rec=[j[0],j[1],j[2],j[3]]
                            with_val=int(j[3])+1
                            Functions.update_rec("Books.db","All_Books_Rec",lst_book_rec,with_val,j[3])
                            print("Book successfully returned!")
                        else:
                            print("Book not returned.")
                            continue
                        
            elif option == 4:      ## see Book IDs of previously borrowed books
                borr_data=Functions.search_rec("Student.db","Student_Rec","user",self.info[0])
                for i in borr_data:
                    lst=(i[5]).split(",")       ## convets the Book Ids stored in string format, into a list
                    if lst[0]!="":              ## "" is not overwritten before the books are borrowed
                        print("The Book IDs of your borrowed books are as follows: ")
                        for j in lst:
                            print(j)
                    else:
                        print("You have no borrowed books right now.")
                    
            elif option == 5:       ## update your information                  
                rec=Functions.show_rec("Student.db","Student_Rec",self.info[0])
                print(f'''for {rec[3]}, you can update the following info: ''')
                print("First Name            Last Name             Email address         Password")
                print(f'{rec[0]:20}  {rec[1]:20}  {rec[2]:20}  {rec[4]:20}')
                what_val=input("Enter the information you want to update (The information is case sensitive): ")
                with_val=input("Enter the new information (The infomation is case sensitive): ")
                Functions.update_rec("Student.db","Student_Rec",rec,with_val,what_val)
                new_rec=Functions.show_rec("Student.db","Student_Rec",self.info[0])
                print(f"""Self Information successfully updated. Your information is as follows:
username: {new_rec[3]}""")
                print("First Name            Last Name             Email address         Password")
                print(f'{new_rec[0]:20}  {new_rec[1]:20}  {new_rec[2]:20}  {new_rec[4]:20}')

            elif option == 6:                  ## log out
                print("""Logged out successfully!
Press 1 to log in to another account, press any other key to exit the application: """, end="")
                key=input()
                if key == "1":                 ## return to main menu
                    Login.main_menu(self)
                else:                          ## exit application
                    print("Bye Bye!")
                    sys.exit()
            else:
                print("Enter an in integer from 1 to 10 inclusive")
                continue

class Login:
    """Provides the main menu of the program.

    Is associated with the Admin and the Student class.
    """
    def __init__(self):
        """Creates the databases on the first run of the code.
        """
        try:
            conn1=sqlite3.connect("Books.db")
            c1=conn1.cursor()
            ##col1 stores title, col2 author's name, col3 3 Book_ID, col4 no. of copies of the book  
            c1.execute("CREATE TABLE All_Books_Rec "
                       "( title TEXT , aname TEXT, Book_ID INTEGER, copies INTEGER)")
            ##col1 stores title, col2 author's name, col3 3 Book_ID, col4 email of borrower
            c1.execute("CREATE TABLE Borrowed_Books_Rec "
                       "( title TEXT , aname TEXT, Book_ID INTEGER, borrower TEXT)")
            conn1.commit()
            conn1.close()
            # providing some pre entered data
            Functions.add_rec("Books.db","All_Books_Rec","It Ends with us","Colleen Hoover",1001,7)
            Functions.add_rec("Books.db","All_Books_Rec","Verity","Colleen Hoover",1002,5)
            Functions.add_rec("Books.db","All_Books_Rec","The Kite Runner","Khalid Hosseni",1003,7)
            Functions.add_rec("Books.db","All_Books_Rec","The Alchemist","Paulo Coelho",1004,5)
            Functions.add_rec("Books.db","All_Books_Rec","The Pilgrimage","Paulo Coelho",1005,10)
            Functions.add_rec("Books.db","All_Books_Rec","The Da Vinci Code","Dan Brown",1006,3)
            Functions.add_rec("Books.db","All_Books_Rec","Inferno","Dan Brown",1007,8)
            Functions.add_rec("Books.db","All_Books_Rec","Jane Eyre","Charlotte Bronte",1008,3)
            Functions.add_rec("Books.db","All_Books_Rec","Wuthering Heights","Emily Bronte",1009,2)
            Functions.add_rec("Books.db","All_Books_Rec","The Great Expectations","Charles Dickens",1010,6)
            conn2=sqlite3.connect("Student.db")
            c2=conn2.cursor()
            # col1 stores the first name, col2 last name, col3 email address, col4 username, col5 password, col6 history of books borrowed
            c2.execute("CREATE TABLE Student_Rec "
                       "( fname TEXT , lname TEXT, email TEXT, user TEXT, pw TEXT , history TEXT)")
            conn2.commit()
            conn2.close()
        except:
            pass
        self.main_menu()
        
    def main_menu(self):
        """Allows user to choose role. 
        """
        print("""Are you an Admin or a Student? Enter 1 for Admin, 2 for Student, 3 to Exit: """, end ="")
        flag=1
        while flag:
            try:
                self.who=int(input())
            except ValueError:
                print("Please enter 1 for Admin, 2 for Student, or 3 to exit.")    
                continue
            if self.who==1:
                Admin()
                flag=0
            elif self.who==2:
                Student()
                flag=0
            elif self.who==3:
                sys.exit()
            else:
                print("Please enter 1 for Admin, 2 for Student, or 3 to exit.")
                continue

# driver code
print("*******************************")
print ("This is only to let you know the ID and password for the first run.")
print("""For Admin: 
        Username: LibraryAdmin
        Password: Admin_123""")
print("*******************************")
x=Login()




