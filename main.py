

"""
Things that can be aded in future:
    1. Deactivating members
    2. Imposing fine on overdue books
    3. Adding data validation if I am getting data from an external source in future.
    4. Adding a loan dataclass to keep the loan acitivty separate and adding a return date for record keeping.
    5. Creating custom exceptions for BookNotFound, MemberNotFound, NoCopiesAvailable etc. - Overkill?

"""


import itertools
from datetime import date, timedelta
from dataclasses import dataclass,field

@dataclass
class Book:
    isbn:  str
    title: str
    author: str
    year: int

    def __str__(self) -> str:

        return f'''The book information:
        Title: {self.title}
        Author: {self.author}
        Year: {self.year}
        '''

@dataclass
class Member:

    full_name: str
    date_of_birth: date
    email_id: str
    member_id: int = field(default=None, init=False) # If I would have created the ID while creating the Member object, I could have used default_factory parameter to pass a id generator function in field().

    def __str__(self) -> str:

        return f'''The member information:
        Name: {self.full_name}
        DOB: {self.date_of_birth}
        Email ID: {self.email_id}
        Member ID: {self.member_id}
        '''

class Library:

    id_generator = itertools.count(start=1)

    def __init__(self):        
        self.book_inventory = {}
        self.member_list = {}
        self.email_list = {}

    def add_book(self,book: Book, copies: int) -> str:
        if book.isbn in self.book_inventory:
            self.book_inventory[book.isbn]['available_copies']+=copies
            self.book_inventory[book.isbn]['total_copies']+=copies
        else:
            self.book_inventory[book.isbn] = {'book_info': book, 'available_copies': copies, 'total_copies': copies}
        
        return f"Book '{book.title}' added to the inventory."

    def search_book(self,title: str):
        pass

    def register_member(self, member: Member) -> str:

        try:

            if member.email_id.strip().lower() in self.email_list:
                raise ValueError(f"Member already registered with {member.email_id}. The member ID is: {self.email_list[member.email_id]}")

            new_member_id = next(Library.id_generator)

            member.member_id = new_member_id
            self.member_list[member.member_id] = { 'member_info': member, 'join_date': date.today(), 'loan_activity': [] }
            self.email_list[member.email_id.strip().lower()] = member.member_id

            return f"Member {member.full_name} registered successfully with member id: {member.member_id}."
        
        except ValueError as e:
            return f"Error:{e}"
    
    def checkout_book(self, isbn: str, member_id: int) -> str:

        try:

            if member_id not in self.member_list:
                raise ValueError("Member not found!")
            
            if len(self.member_list[member_id]['loan_activity']) >= 5:
                raise ValueError("Member already has 5 books loaned. That is the limit!")
            
            if not isbn in self.book_inventory or self.book_inventory[isbn]['available_copies'] == 0:
                raise ValueError('Book is not available currently.')


            self.book_inventory[isbn]['available_copies']-=1

            checkout_details = { 'book_isbn': isbn, 'date_loaned' : date.today(), 'due_date': date.today()+timedelta(days=14) }
            self.member_list[member_id]['loan_activity'].append(checkout_details)

            return f"Successfully checked out the book {isbn} to {member_id}."
        
        except ValueError as e:
            return f"Error:{e}"
    
    def return_book(self,isbn: str, member_id: int) -> str:

        try:
            is_book_loaned = False

            if member_id not in self.member_list or isbn not in self.book_inventory:
                raise ValueError("Invalid record! Either the member doesn't exists or the book ISBN doesn't exist!")

            books_loaned = self.member_list[member_id]['loan_activity']

            for book_info in books_loaned:
                if isbn == book_info['book_isbn']:
                    is_book_loaned = True
                    self.member_list[member_id]['loan_activity'].remove(book_info)
                    break
            
            if not is_book_loaned:
                raise ValueError(f"Record not found! Member {member_id} didn't loan the book {isbn}.")

            # I can add a check to see if the return date is past due date and impose a fine or late fee in future.
            self.book_inventory[isbn]['available_copies']+=1

            return f"Member {member_id} returned the book {isbn} successfully."
        
        except ValueError as e:
            return f"Error:{e}"
    
    def get_book_inventory(self) -> str:
        return f"Here is the library collection\n: {self.book_inventory}."
    
    def get_member_list(self) -> str:
        return f"List of all library members\n: {self.member_list}."
    
    def get_books_loaned(self, member_id: int) -> str:
        return f"List of books loaned by member with ID {member_id}\n: {self.member_list[member_id]['loan_activity']}"

    def get_available_copies(self,isbn: str) -> str:
        return f"Available copies for the book {self.book_inventory[isbn]['book_info'].title} with ISBN {isbn} are: {self.book_inventory[isbn]['available_copies']}."

    def get_total_copies(self,isbn: str) -> str:
        return f"Total copies for the book {self.book_inventory[isbn]['book_info'].title} with ISBN {isbn} are: {self.book_inventory[isbn]['total_copies']}."

book1 = Book('123-4', 'Are you afraid of the dark?', 'Sidney Sheldon', 2005)
book2 = Book('123-5', "Harry Potter and the Sorcerer's Stone", 'JK Rowling', 1997)
# book3 = Book('123-4', 'Are you afraid of the dark? version2', 'SidneySheldon', '2005', 1)
print(book2)
lib1 = Library()
print(lib1.add_book(book1,1))
print(lib1.add_book(book2,1))
print(lib1.add_book(book1,2))
member1 = Member('Shalini Agarwal',date(1997,1,12), 'Shalini@example.com')
print(member1)
print(lib1.register_member(member1))
print(lib1.checkout_book('123-4',1))
print(lib1.checkout_book('123-4',1))
print(lib1.get_member_list())
print(lib1.get_book_inventory())
print(member1)
print(lib1.get_member_list())
print(lib1.get_books_loaned(1))
print(lib1.get_available_copies('123-4'))
print(lib1.get_total_copies('123-4'))
print(lib1.return_book('123-4',1))