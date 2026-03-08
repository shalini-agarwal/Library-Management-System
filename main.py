
import itertools
from datetime import date, timedelta


"""
Should I be creating the memberlist dictionary with emailID as key or member ID as key?
What if a member forgets his ID, he should be able to find his member id by looking up his name/email ID. Name is not unique but the email ID is. Should I create two dictionaries - one with the member id as key and the other name or email_ID as key?
For now, I am assuming that all members will know their member ID at all times.
I am not having a logic for decativating members right now. I don't know what this means even.
I am also not checking all the overdue books currently.
"""
class Library:
    def __init__(self):        
        self.book_inventory = {}
        self.member_list = {}

        self.id_generator = itertools.count(start=1)

    def add_book(self,isbn: str, title: str, author: str, year: str, copies: int) -> str:
        if isbn in self.book_inventory:
            self.book_inventory[isbn]['copies']+=copies
        else:
            self.book_inventory[isbn] = {'title': title,
                                            'author': author,
                                            'year': year,
                                            'copies': copies}
        
        return "Book added to the inventory."

    def remove_book(self,isbn: str) -> str:
        if isbn not in self.book_inventory:
            raise ValueError("Can't find the book with this ISBN number")

        self.book_inventory[isbn]['copies']-=1

        # Should I delete a record if the copies are zero? Also what is the point of having a remove book function anyway?
        # if self.book_inventory[isbn]['copies'] == 0:
        #     del self.book_inventory[isbn]
    
        return "Book removed from the inventory."


    def register_member(self, name: str) -> str:

        # How should I be checking if a person already is a member if I am not creating the key with emailID?
        # if email_id in self.member_list:
        #     raise ValueError('Member already exists!')

        member_id = next(self.id_generator)
        self.member_list[member_id] = {
                                        'name': name,
                                        'join_date': date.today(),
                                        'loan_activity': []
        }

        return "Member registered successfully with member id:",member_id
    
    def checkout_book(self,isbn: str, member_id: int) -> str:
        if member_id not in self.member_list:
            raise ValueError("Member not found!")
        
        if len(self.member_list[member_id]['loan_activity']) == 5:
            raise ValueError("Member already has 5 books loaned. That is the limit!")
        
        if not isbn in self.book_inventory or self.book_inventory[isbn]['copies'] == 0:
            raise ValueError('Book is not available currently.')

        checkout_details = {isbn: {'date_loaned' : date.today(), 'due_date': date.today()+timedelta(days=14)}}
        self.member_list[member_id]['loan_activity'].append(checkout_details)

        return "Successfully checked out the book."
    
    def return_book(self,isbn: str, member_id: int) -> str:
        if member_id not in self.member_list or isbn not in self.book_inventory:
            raise ValueError("Invalid record! Either the member doesn't exists or the book ISBN doesn't exist!")
        
        if isbn not in self.member_list[member_id]['loan_activity']:
            raise ValueError("This member didn't loan this book!")

        # I can add a check to see if the return date is past due date and impose a fine or late fee in future.
        del self.member_list[member_id]['loan_activity'][isbn]

        return "Return successfull!"
    
    def get_book_inventory(self) -> dict:
        return self.book_inventory
    
    def get_member_list(self) -> dict:
        return self.member_list
    
    def get_member_info(self,member_id: str) -> dict:
        return self.member_list[member_id]

class Book:

    def __init__(self,isbn: int, title: str, author: str, year: int, copies: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    # function for getting the current book inventory state

    pass

    


class Member:
    pass

lib1 = Library()
print(lib1.add_book('123-4', 'Are you afraid of the dark?', 'Sidney Sheldon', '2005', 1))
print(lib1.register_member('Shalini Agarwal'))
print(lib1.checkout_book('123-4',1))
print(lib1.get_book_inventory())
print(lib1.get_member_info(1))
print(lib1.add_book('123-5', "Harry Potter and the Sorcerer's Stone", 'JK Rowling', '1997', 2))
print(lib1.add_book('123-4', 'Are you afraid of the dark? version2', 'SidneySheldon', '2005', 1))
print(lib1.get_book_inventory())