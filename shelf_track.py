import sqlite3

def connect_database():

    #Connect to the ebookstore database, return db 
    db = sqlite3.connect("ebookstore_db.db")
    return db
    
def create_book_table():

    #Function to create 'book' table   
    with connect_database() as db:
        try:
            cursor = db.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS book(
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               authorID INTEGER NOT NULL,
               qty INTEGER NOT NULL
            )''')
            db.commit()
        
        except Exception as e:
            db.rollback()
            raise e
    

def populate_book_table():

    #Populate the 'book' table with data
    with connect_database() as db:
        try:
            cursor = db.cursor()
            book_info = [
                (3001, "A Tale of Two Cities", 1290, 30),
                (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
                (3003, "The Lion, the Witch and the Wardobe", 2356, 25),
                (3004, "The Lord of the Rings", 6380, 37),
                (3005, "Alice's Adventures in Wonderland", 5620, 12),
                ]
            cursor.executemany(
            '''INSERT INTO book(id, title, authorID, qty) VALUES(?, ?, ?, ?)'''
            ,book_info
            )
            db.commit()
    
        except Exception as e:
            db.rollback()
            raise e
    

def create_author_table():
    
    #Create 'author' table
    with connect_database() as db:
        try:
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS author(
                idAUTH INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
                )''')
            db.commit()

        except Exception as e:
            db.rollback()
            raise e
    

def populate_author_table():

    #Populate the 'author' table with data
    with connect_database() as db:
        try:
            cursor = db.cursor()
            author_info = [
                (1290, "Charles Dickens", "England"),
                (8937, "J.K. Rowling", "England"),
                (2356, "C.S. Lewis", "Ireland"),
                (6380, "J.R.R Tolkien", "South Africa"),
                (5620, "Lewis Carroll", "England"),
                ]
            cursor.executemany(
            '''INSERT INTO author(idAUTH, name, country) VALUES(?, ?, ?)'''
            , author_info
            )
            db.commit()

        except Exception as e:
            db.rollback()
            raise e
    

def enter_book():
    
    # Function to allow the user to enter a book. 
    # Prompt user to enter book id and insert data into table
    # USe condition statement to ensure the id entered is no more than 4 digits 
    # use insert or ignore to allow for duplicates 
    with connect_database() as db:
        try:
            cursor = db.cursor()
            new_id = int(input("Please enter the book id: ")) 
            if new_id >= 1000 or new_id <= 9999:
                new_title = input("Please enter the book title: ")
                new_author = int(input("Please enter the author id: "))
                if new_author <= 1000 or new_author >= 9999:
                    print("You have entered an invalid ID")
                    return menu
                else:
                    new_qty = input("Please enter the quantity of the book: ")
                    cursor.execute('''
                        INSERT OR IGNORE INTO book(id, title, authorID, qty)
                        VALUES (?, ?, ?, ?)
                        ''', (new_id, new_title, new_author, new_qty))
                    print("Book added.")
                    db.commit()
            else:
                print("You have entered an invalid ID")
                return
    

        except ValueError:
            print("Please enter a valid entry.")
    

def update_book():

    # Function to allow user to update book details
    # Use elif statements to edit details of the books/authors depending on the user's choice
    # Ensure id input is no more than 4 digits 
    with connect_database() as db:
        try:
            cursor = db.cursor()
            update_choice = int(input("Please enter the book id you would like to update: "))       
            if update_choice >= 1000 or update_choice <= 9999:
                choice = input(
                '''Would you like to edit book details or update quantity? '''
                '''Enter E for edit or U for update: ''').upper()
                if choice == "U": 
                    update_qty = int(input("Please enter the new quantity: "))
                    cursor.execute(
                        '''UPDATE book SET qty = ? WHERE id = ?''', 
                        (update_qty, update_choice)
                        )
                    print("Quantity changed.")
                elif choice == "E":
                    edit_choice = input(
                    '''Please enter 'T' to edit a title, 'A' to edit the author, '''
                    '''or 'C' to edit the author country: ''').upper()
                    if edit_choice == "T":
                        edit_title = input("Please enter the updated title: ")
                        cursor.execute(
                            '''UPDATE book SET title = ? WHERE id = ?''', 
                            (edit_title, update_choice)
                            )
                        print("Title updated.")
                    elif edit_choice == "A":
                        author_id = input("Please enter the author ID: ")
                        cursor.execute('''
                            SELECT book.title, book.qty, author.name, 
                            author.country FROM book INNER JOIN author ON 
                            book.authorID = author.idAUTH'''
                                       )
                        cursor.fetchall()
                        author_choice = input(
                        '''Please enter 'AN' to update author name, '''
                        ''''AC' to update author country, or 'B' to update both: ''').upper()
                        if author_choice == "AN":
                            update_an = input("Please enter the new author name: ")
                            cursor.execute('''UPDATE author SET name = ? WHERE id = ?''', 
                                (update_an, author_id)
                                )
                            print("Author name updated.")
                        elif author_choice == "AC":
                            update_ac = input("Please enter the new author country: ")
                            cursor.execute('''UPDATE author SET country = ? WHERE id = ? ''', 
                                           (update_ac, author_id))
                            print("Author country updated.")
                        elif author_choice == "B":
                            update_an = input("Please enter the new author name: ")
                            update_ac = input("Please enter the new author country: ")
                            cursor.execute('''UPDATE author SET name = ? 
                                           WHERE id = ?''', (update_an, author_id))
                            cursor.execute('''UPDATE author SET country = ? 
                                           WHERE id = ? ''', (update_ac, author_id))
                            print("Author name and country updated.")
                        db.commit()
            else:
                print("You have entered an invalid ID")
                return menu
        
        except ValueError:
            print("Invalid input. Please re-enter.")

    
    
def delete_book():

    #Function to allow user to delete book
    with connect_database() as db:
        try:
            cursor = db.cursor()
            delete_choice = int(input("Please enter the id of the book you want to delete: "))
            cursor.execute('''DELETE FROM book WHERE id = ?''', (delete_choice,))
            print(f"Book {delete_choice} has been deleted.")
            db.commit()
    
        except ValueError:
            print("Invalid id entered. Please try again.")
    
        

def search_books():

    #Function to allow user to search for a book
    with connect_database() as db:
        try:
            cursor = db.cursor()
            book_search = int(input("Please enter the id of the book you are searching for: "))
            cursor.execute('''SELECT book.title, author.name, author.country 
                           FROM book INNER JOIN author ON book.authorID = author.idAUTH 
                           WHERE id = ?''', ([book_search,]))
            result = cursor.fetchall()
            for title, name, country in result:
                print(title, name, country)
    
        except ValueError:
            print("Invalid id entered. Please try again.")


def view_all():

    # Function to allow user to view all books, using inner join
    # Loop through to print details  
    with connect_database() as db:
        cursor = db.cursor()
        cursor.execute('''SELECT book.title, author.name, author.country 
                       FROM book INNER JOIN author ON 
                       book.authorID = author.idAUTH''')
        result = cursor.fetchall()
        for title, name, country in result:
            print(title, name, country)
        


def exit_program():

    with connect_database() as db:
        db.close()
        print("Exiting the program")

    
create_author_table()
populate_author_table()
create_book_table()
populate_book_table()

while True:

    try:
        menu = int(input(
            '''Select one of the following options:
            1. Enter book
            2. Update book
            3. Delete book
            4. Search books
            5. View details of all books
            0. Exit
            '''
        ))

        if menu == 1:
            enter_book()

        elif menu == 2:
            update_book()

        elif menu == 3:
            delete_book()

        elif menu == 4:
            search_books()

        elif menu == 5:
            view_all()

        elif menu == 0:
            exit_program()
            
    
    except ValueError:
        with connect_database() as db:
            print("Choice not valid.")
            db.close()


