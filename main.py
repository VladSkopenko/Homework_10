from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not isinstance(self._value, str) or len(self._value) != 10 or not self._value.isdigit():
            raise ValueError("Invalid phone number format")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.validate()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def __str__(self):
        if self.birthday:
            return (f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},"
                    f" birthday: {self.birthday}")
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: None"

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
        trans = datetime.strptime(str(self.birthday), "%Y-%m-%d")
        next_birthday = datetime(today.year, trans.month, trans.day)
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, trans.month, trans.day)
        days_left = (next_birthday - today).days
        return f"{days_left} days left until birthday {self.name.value}"


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

    def save_disk(self):
        with open("AddressBook.bin", "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open("AddressBook.bin", "rb") as file:
            return pickle.load(file)

    def search(self, value):
        result = []
        value = value.lower()
        for name, record in self.data.items():
            if name.lower().startswith(value):
                result.append(record)
            else:
                for phone in record.phones:
                    if phone.value.startswith(value):
                        result.append(record)

        return result

    def __str__(self):
        records_str = ',\n'.join(f"{name}: {record}" for name, record in self.data.items())
        return f"{{\n{records_str}\n}}"


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate_b()

    def validate_b(self):
        try:
            date_value = datetime.strptime(self._value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please provide Year-Month-Day.")

        if not (1 <= date_value.month <= 12 and 1 <= date_value.day <= 31):
            raise ValueError("Invalid date. Month should be between 1 and 12, day between 1 and 31.")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.validate_b()

    def __str__(self):
        return self._value


# мої тести
phone_1 = "0963610573"
phone_2 = "0963610574"
phone_3 = "0973716132"
record = Record("luda", birthday="1980-05-16")
record_1 = Record("Vlad", birthday="1994-03-28")
record_2 = Record("Oleg", birthday="1976-01-23")
record.add_phone(phone_1)
record_1.add_phone(phone_2)
record_2.add_phone(phone_3)
ad = AddressBook()
ad.add_record(record)
ad.add_record(record_1)
ad.add_record(record_2)
ad.save_disk()
print(ad.read_from_file())
while True:
    fin = ad.search(input("Enter phone or Name pls:"))
    for elem in fin:
        if elem:
            print(elem)
