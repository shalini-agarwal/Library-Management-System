

"""
Should I be creating the memberlist dictionary with emailID as key or member ID as key?
What if a member forgets his ID, he should be able to find his member id by looking up his name/email ID. Name is not unique but the email ID is. Should I create two dictionaries - one with the member id as key and the other name or email_ID as key?
For now, I am assuming that all members will know their member ID at all times.
I am not having a logic for decativating members right now. I don't know what this means even.
I am also not checking all the overdue books currently.
I should also add try-except blocks to catch the exception raised in a user-firnedly way. Without Python showing a traceback.

Explore dataclass.
Explore getter and setter.

"""


import itertools
from datetime import date, timedelta

class Book:

    def __init__(self,isbn: int, title: str, author: str, year: int, copies: int) -> None:
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    # Should change it to str method
    def get_book_info(self) -> str:

        return f'''The book information:
        Title: {self.title}
        Author: {self.author}
        Year: {self.year}
        Copies Available Currently: {self.copies}
        '''

class Member:
    
    id_generator = itertools.count(start=1)

    def __init__(self, full_name: str, date_of_birth: str, email_id: str) -> None:
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.email_id = email_id
        self.member_id = next(Member.id_generator)
        self.loan_activity = {}
        self.join_date = date.today()
    
    # Should change it to str method
    def get_member_info(self) -> str:

        return f'''The member information:
        Name: {self.full_name}
        DOB: {self.date_of_birth}
        Email ID: {self.email_id}
        Member ID: {self.member_id}
        Loan Activity: {self.loan_activity}
        Member since: {self.join_date}
        '''
    
    def get_books_loaned(self):

        return f"The loan activity of the member {self.full_name} is:\n {self.loan_activity}."

class Library:
    def __init__(self):        
        self.book_inventory = {}
        self.member_list = {}

    def add_book(self,book: Book) -> str:
        if book.isbn in self.book_inventory:
            self.book_inventory[book.isbn]['copies']+=book.copies
        else:
            self.book_inventory[book.isbn] = {'title': book.title,
                                            'author': book.author,
                                            'year': book.year,
                                            'copies': book.copies}
        
        return f"Book {book.title} added to the inventory."

    def search_book(self,title: str):
        pass

    def register_member(self, member: Member) -> str:

        # How should I be checking if a person already is a member?

        self.member_list[member.member_id] = {
                                        'name': member.full_name,
                                        'DOB': member.date_of_birth,
                                        'email_id': member.email_id,
                                        'join_date': member.join_date,
                                        'loan_activity': member.loan_activity
        }

        return f"Member {member.full_name} registered successfully with member id: {member.member_id}."
    
    def checkout_book(self, book: Book, member: Member) -> str:
        if member.member_id not in self.member_list:
            raise ValueError("Member not found!")
        
        if len(self.member_list[member.member_id]['loan_activity']) == 5:
            raise ValueError("Member already has 5 books loaned. That is the limit!")
        
        if not book.isbn in self.book_inventory or self.book_inventory[book.isbn]['copies'] == 0:
            raise ValueError('Book is not available currently.')

        self.book_inventory[book.isbn]['copies']-=1

        # Need to change the structure of loan activity to allow multiple loans for same isbn; since we can have multiple copies of the same isbn
        if book.isbn in self.member_list[member.member_id]['loan_activity']:
            raise ValueError("Member already has a book loaned with the same ISBN")

        checkout_details = {book.isbn: {'date_loaned' : date.today(), 'due_date': date.today()+timedelta(days=14)}}
        self.member_list[member.member_id]['loan_activity'].update(checkout_details)

        return f"Successfully checked out the book {book.title} to {member.full_name}."
    
    def return_book(self,book: Book, member: Member) -> str:
        if member.member_id not in self.member_list or book.isbn not in self.book_inventory:
            raise ValueError("Invalid record! Either the member doesn't exists or the book ISBN doesn't exist!")
        
        if book.isbn not in self.member_list[member.member_id]['loan_activity']:
            raise ValueError(f"Record not found! Member {member.full_name} didn't loan the book {book.title}.")

        # I can add a check to see if the return date is past due date and impose a fine or late fee in future.
        self.book_inventory[book.isbn]['copies']+=1

        del self.member_list[member.member_id]['loan_activity'][book.isbn]

        return f"Member {member.full_name} returned the book {book.title} successfully."
    
    def get_book_inventory(self) -> str:
        return f"Here is the library collection\n: {self.book_inventory}."
    
    def get_member_list(self) -> str:
        return f"List of all library members\n: {self.member_list}."


book1 = Book('123-4', 'Are you afraid of the dark?', 'Sidney Sheldon', '2005', 1)
lib1 = Library()
print(lib1.add_book(book1))
# print(lib1.get_book_inventory())
print(lib1.add_book(book1))
# print(lib1.get_book_inventory())
member1 = Member('Shalini Agarwal','01-12-1997', 'shalini@example.com')
print(lib1.register_member(member1))
print(lib1.checkout_book(book1,member1))
# print(lib1.get_book_inventory())
# print(lib1.get_member_list())
# print(lib1.return_book(book1,member1))
# print(lib1.get_book_inventory())
print(member1.get_member_info())
print(member1.get_books_loaned())
# print(lib1.register_member('Shalini Agarwal'))
# print(lib1.checkout_book('123-4',1))
# print(lib1.get_book_inventory())
# print(lib1.get_member_info(1))
# print(lib1.add_book('123-5', "Harry Potter and the Sorcerer's Stone", 'JK Rowling', '1997', 2))
# print(lib1.add_book('123-4', 'Are you afraid of the dark? version2', 'SidneySheldon', '2005', 1))
# print(lib1.get_book_inventory())