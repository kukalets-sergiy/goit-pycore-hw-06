"""Data models for a simple address book."""

import re
from collections import UserDict


class Field:
    """A base class for fields in a contact record."""
    def __init__(self, value):
        self.value = value

    # Define a string representation for the Field class
    def __str__(self):
        return str(self.value)


class Name(Field):
    """A required contact name."""
    def __init__(self, value):
        # Validate that the name is a non-empty string
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        # Call the parent class constructor to set the value
        super().__init__(value)


class Phone(Field):
    """A phone number containing exactly 10 digits."""
    def __init__(self, value):
        # Validate that the phone number is a string of exactly 10 digits
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        # Call the parent class constructor to set the value
        super().__init__(value)


class Record:
    """A contact record containing a name and a list of phone numbers."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone) -> Phone:
        """Add a phone number to the contact record."""
        # Validate and create a Phone object
        phone = Phone(phone)
        # Add the Phone object to the list of phones
        self.phones.append(phone)
        # Return the Phone object that was added
        return phone

    def find_phone(self, phone) -> Phone | None:
        """Find a phone number in the contact record."""
        # Use a generator expression to search for the phone number in the list of phones
        return next((item for item in self.phones if item.value == phone), None)

    def remove_phone(self, phone) -> None:
        """Remove a phone number from the contact record."""
        # Find the phone number in the list of phones
        found_phone = self.find_phone(phone)
        if found_phone is None:
            raise ValueError(f"Phone number {phone} not found.")
        # Remove the found phone number from the list of phones
        self.phones.remove(found_phone)

    def edit_phone(self, old_phone, new_phone) -> Phone:
        """Edit a phone number in the contact record."""
        # Find the phone number in the list of phones
        found_phone = self.find_phone(old_phone)
        if found_phone is None:
            raise ValueError(f"Phone number {old_phone} not found.")
        # Create a new Phone object with the new phone number
        replacement = Phone(new_phone)
        # Replace the old phone number with the new one in the list of phones
        self.phones[self.phones.index(found_phone)] = replacement
        # Return the new Phone object that was added
        return replacement

    def __str__(self):
        # Define a string representation for the Record class
        phones = "; ".join(str(phone) for phone in self.phones)
        # Return a formatted string with the contact name and phone numbers
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    """A collection of contact records."""
    def add_record(self, record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name) -> Record | None:
        """Find a record in the address book by name."""
        return self.data.get(name)

    def delete(self, name) -> None:
        """Delete a record from the address book by name."""
        del self.data[name]


# Creating a new address book
book = AddressBook()

# Creating a record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Adding John's record to the address book
book.add_record(john_record)

# Creating and adding a new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Printing all records in the address book
for name, record in book.data.items():
    print(record)

# Finding and editing a phone number for John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Output: Contact name: John, phones: 1112223333; 5555555555

# Finding a specific phone number in John's record
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Output: 5555555555

# Deleting Jane's record
book.delete("Jane")
