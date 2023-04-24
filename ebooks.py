##-----------------import modules ----------------------##
import sqlite3
##-------------------------------------------------------##

db = sqlite3.connect('data/ebookstore_db')          #create connection to database
cursor = db.cursor()                                #create cursor object

#create initial list of books
book1 = [3001, 'A Tale of Two Cities', 'Charles Dickens', 30]
book2 = [3002, 'Harry Potter and the Phiosopher\'s Stone', 'JK Rowling', 30]
book3 = [3003, 'The lion the witch and the wardrobe','CS Lewis',25]
book4 = [3004, 'The Lord of the Rings','JRR Tolkien',37]
book5 = [3005,'Alice in wonderland','Lewis Caroll', 12]

book_list = [book1,book2,book3,book4,book5]



def create_table():
    #create empty table
    try:
        cursor.execute('''
        CREATE TABLE books(id int(4) primary key, title varchar(100), author varchar(100), qty int(3))
        ''')
        db.commit()
    except sqlite3.OperationalError:   #if table already created
       pass
   
    #add initial data into table
    try:
        cursor.executemany("INSERT INTO books VALUES (?,?,?,?)", book_list)

    except sqlite3.IntegrityError:   #If books already added     
        pass

def add_book():
    #get book parameters
    title = input("Enter title of book: ")
    author = input("Enter name of author: ")
    qty = int(input("Enter quantity of book: "))

    #get id parameter (1 + current highest id in table)
    res = (cursor.execute('''
    SELECT MAX(id)
    FROM books'''))
    high_id_tuple = res.fetchone()      #get highest value in id column
    high_id = high_id_tuple[0]          #select id integer from the tuple result

    new_id = high_id + 1                #iterate id

    newbook = [new_id,title,author,qty] #create 'newbook' list to store new book data

    cursor.execute('''
    INSERT INTO books
    VALUES(?,?,?,?)''', newbook)        #add the new book into table 'books'

    db.commit()

    return

def update_book():
    #Get values from user (base on id of book to change)
    book_id = input("What is the ID of the book you would like to update? ")
    field = input("What would value would you like to update (title, author or quantity? )")
    new_value = input(f"Enter the new value of {field}: ")

    #Update value base on what user entered as 'field' to update
    if field == 'author':
        cursor.execute('''
        UPDATE books SET author = ? WHERE id = ?
        ''', (new_value, book_id))

    elif field == 'title':
        cursor.execute('''
        UPDATE books SET title = ? WHERE id = ?
        ''', (new_value, book_id))

    elif field == 'quantity':
        cursor.execute('''
        UPDATE books SET qty = ? WHERE id = ?
        ''', (new_value, book_id))

    else:
        print("Sorry, that is not an option.")      #if wrong input

    db.commit()

def delete_book():
    book_id = int(input("What is the ID of the book you would like to delete? "))       #get id of book to delete
    cursor.execute(''' DELETE FROM books WHERE id = ? ''', (book_id,))          #delete book

    db.commit()     #commit changes

def search_books():
    search_type = (input("Would you like to search by title or author? ")) #how would the user like to search
    #search depending on input
    if search_type == 'title':
        title = input("Enter title to search: ")
        res = cursor.execute("SELECT * FROM books WHERE title = ?", (title,))
        
        for row in res.fetchall():  #print all rows with that title
            print(f"{row}\n")

    if search_type == 'author':
        author = input("Enter author to search: ")
        res = cursor.execute("SELECT * FROM books WHERE author = ?", (author,))
        
        for row in res.fetchall():  #print all rows with that author
            print(f"{row}\n")
            
    else:
        print("This is not an option. Sorry.")


#Call the function to create table first
create_table()


#user menu
while True:
    menu = input('''Select one of the following Options below:      
    e - Enter a book
    u - Update a book
    d - Delete a book
    s - Search books
    z - Exit
    : ''').lower()      

    if menu == 'e':
        add_book()
    elif menu == 'u':
        update_book()
    elif menu == 'd':
        delete_book()        
    elif menu == 's':
        search_books()
    elif menu == 'va':
        #view the database
        res = cursor.execute("SELECT * FROM books")
        for row in res.fetchall():
            print(row)

    elif menu == 'z':
        print('Goodbye!!!')
        db.close # close database
        exit()
    else:
        print("You have made a wrong choice, Please Try again")
