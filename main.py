

"""
Should I be creating the memberlist dictionary with emailID as key or member ID as key?
What if a member forgets his ID, he should be able to find his member id by looking up his name/email ID. Name is not unique but the email ID is. Should I create two dictionaries - one with the member id as key and the other name or email_ID as key?
For now, I am assuming that all members will know their member ID at all times.
I am not having a logic for decativating members right now. I don't know what this means even.
I am also not checking all the overdue books currently.
I should also add try-except blocks to catch the exception raised in a user-firnedly way. Without Python showing a traceback.

Explore dataclass.
Explore getter and setter/ property decoraters.
Make get functions to __str__ methods.

Explore on adding data validation checks.

"""


import itertools
from datetime import date, timedelta
from dataclasses import dataclass

@dataclass
class Book:
    isbn:  str
    title: str
    author: str
    year: str

    def __str__(self) -> str:

        return f'''The book information:
        Title: {self.title}
        Author: {self.author}
        Year: {self.year}
        '''

@dataclass
class Member:

    full_name: str
    date_of_birth: str
    email_id: str
    
    def __str__(self) -> str:

        return f'''The member information:
        Name: {self.full_name}
        DOB: {self.date_of_birth}
        Email ID: {self.email_id}
        '''

class Library:

    id_generator = itertools.count(start=1)

    def __init__(self):        
        self.book_inventory = {}
        self.member_list = {}

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

        # How should I be checking if a person is already a member?
        member_id = next(Library.id_generator)
        self.member_list[member_id] = { 'member_info': member, 'join_date': date.today(), 'loan_activity': [] }

        return f"Member {member.full_name} registered successfully with member id: {member_id}."
    
    def checkout_book(self, book: Book, member_id: int) -> str:
        if member_id not in self.member_list:
            raise ValueError("Member not found!")
        
        if len(self.member_list[member_id]['loan_activity']) == 5:
            raise ValueError("Member already has 5 books loaned. That is the limit!")
        
        if not book.isbn in self.book_inventory or self.book_inventory[book.isbn]['available_copies'] == 0:
            raise ValueError('Book is not available currently.')

        self.book_inventory[book.isbn]['available_copies']-=1

        checkout_details = { 'book_isbn': book.isbn, 'date_loaned' : date.today(), 'due_date': date.today()+timedelta(days=14) }
        self.member_list[member_id]['loan_activity'].append(checkout_details)

        return f"Successfully checked out the book {book.title} to {member_id}."
    
    def return_book(self,book: Book, member_id: int) -> str:
        is_book_loaned = False

        if member_id not in self.member_list or book.isbn not in self.book_inventory:
            raise ValueError("Invalid record! Either the member doesn't exists or the book ISBN doesn't exist!")

        books_loaned = self.member_list[member_id]['loan_activity']

        for book_info in books_loaned:
            if book.isbn == book_info['book_isbn']:
                is_book_loaned = True
        
        if not is_book_loaned:
            raise ValueError(f"Record not found! Member {member_id} didn't loan the book {book.title}.")

        # I can add a check to see if the return date is past due date and impose a fine or late fee in future.
        self.book_inventory[book.isbn]['available_copies']+=1

        for book_info in books_loaned:
            if book_info['book_isbn'] == book.isbn:
                self.member_list[member_id]['loan_activity'].remove(book_info)


        return f"Member {member_id} returned the book {book.title} successfully."
    
    def get_book_inventory(self) -> str:
        return f"Here is the library collection\n: {self.book_inventory}."
    
    def get_member_list(self) -> str:
        return f"List of all library members\n: {self.member_list}."
    
    def get_books_loaned(self, member_id: int) -> str:
        return f"List of books loaned by member with ID {member_id}\n: {self.member_list[member_id]['loan_activity']}"


book1 = Book('123-4', 'Are you afraid of the dark?', 'Sidney Sheldon', '2005')
book2 = Book('123-5', "Harry Potter and the Sorcerer's Stone", 'JK Rowling', '1997')
# book3 = Book('123-4', 'Are you afraid of the dark? version2', 'SidneySheldon', '2005', 1)
print(book2)
lib1 = Library()
print(lib1.add_book(book1,1))
print(lib1.add_book(book2,1))
print(lib1.add_book(book1,2))
member1 = Member('Shalini Agarwal','01-12-1997', 'shalini@example.com')
print(lib1.register_member(member1))
print(lib1.checkout_book(book1,1))
print(lib1.checkout_book(book1,1))
print(lib1.get_member_list())
print(lib1.get_book_inventory())
print(member1)
print(lib1.get_member_list())
print(lib1.get_books_loaned(1))
