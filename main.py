from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not isinstance(self.value, str) or len(self.value) != 10 or not self.value.isdigit():
            raise ValueError("Invalid phone number format")

    def set_value(self, value):
        self.value = value
        self.validate()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def __str__(self):
        if self.birthday:
            return (f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},"
                    f" birthday: {self.birthday.value}")
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == str(phone_number):
                return phone
        return None

    def edit_phone(self, old, new):
        old = Phone(old)
        new = Phone(new)
        flag = True
        for phone in self.phones:
            if phone.value == old.value:
                index = self.phones.index(phone)
                self.phones[index] = new
                flag = False
        if flag:
            raise ValueError

    def remove_phone(self, phone):
        new_phone = Phone(phone)
        for num in self.phones:
            if num.value == new_phone.value:
                self.phones.remove(num)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)
        days_left = (next_birthday - today).days
        return days_left


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, item_number):
        counter = 0
        result = ""
        for item, record in self.data.items():
            result += f"{item}: {record}\n"
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ""
        if result:
            yield result


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate_b()
        self.day = int(value.split("-")[2] if value else None)
        self.month = int(value.split("-")[1] if value else None)
        self.year = int(value.split("-")[0] if value else None)

    def validate_b(self):
        date_value = datetime.strptime(self.value, "%Y-%m-%d")
        if not isinstance(date_value, datetime):
            raise ValueError("Pls give Year-Month-Day")

    def set_value(self, value):
        self.value = value
        self.validate_b()


a = Birthday("2000-01-28")
w = Birthday("2001-11-19")
e = Birthday("2000-02-10")
n = Record("Vlad", birthday=e)
v = Record("Luda", birthday=w)
b = Record("Oleg", birthday=a)
v.add_phone("0963710683")
n.add_phone("1231234342")
b.add_phone("0963610573")
knige = AddressBook()
knige.add_record(n)
knige.add_record(v)
knige.add_record(b)
#print(knige.iterator(2))
#print(knige)
for items in knige.iterator(2):
    print(items)
