import math
import sqlite3

class Bank:
    CARD_NO = 400000000000000
    PIN_NO = 1000
    ID = 0

    def __init__(self):
        self.banking_status = True
        self.customer_login_status = False
        self.database_connector = None
        self.database_driver = None
        self.card_no = None

    def __str__(self):
        if self.customer_login_status:
            return "1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit"
        else:
            return "1. Create an account\n2. Log into account\n0. Exit"
    def operation(self):
        self.initialize_database()

        while self.banking_status:
            print(self)
            choice = int(input())

            if choice == 0:
                self.banking_status = False
                break
            elif self.customer_login_status:
                if choice == 1:
                    balance = self.check_balance()
                    print(f'Balance: {balance}')
                elif choice == 2:
                    self.add_income()
                elif choice == 3:
                    self.transfer_balance()
                elif choice == 4:
                    self.close_account()
                else:
                    self.customer_login_status = False
                    print('You have successfully logged out!')
            else:
                if choice == 1:
                    self.create_account()
                else:
                    card_no = input('Enter your card number: ')
                    pin_no = input('Enter your PIN: ')

                    if self.check_account_validity(card_no, pin_no):
                        self.customer_login_status = True
                        self.card_no = card_no
                        print('You have successfully logged in!')
                    else:
                        print('Wrong card number or PIN!')
        print('Bye!')

    def initialize_database(self):
        self.database_connector = sqlite3.connect('card.s3db')
        self.database_driver = self.database_connector.cursor()
        self.database_driver.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
        self.database_connector.commit()

    def check_balance(self):
        self.database_driver.execute(f'SELECT balance FROM card WHERE number = {self.card_no}')
        self.database_connector.commit()

        return self.database_driver.fetchone()[0]

    def add_income(self):
        income = int(input('Enter income: '))
        self.database_driver.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {self.card_no}')
        self.database_connector.commit()
        print("Income was added!")

    def transfer_balance(self):
        card_no = input("Transfer\nEnter card number:")
        luhan_validity = (self.adding_luhan_checksum(card_no[:len(card_no)-1]) == card_no)

        self.database_driver.execute(f'SELECT * FROM card WHERE number = "{card_no}"')
        self.database_connector.commit()
        data = self.database_driver.fetchone()

        if not luhan_validity:
            print('Probably you made mistake in the card number. Please try again!')
        elif card_no == self.card_no:
            print("You can't transfer money to the same account!")
        elif data is None:
            print('Such a card does not exist.')
        else:
            amount = int(input('Enter how much money you want to transfer:'))
            if self.check_balance() < amount:
                print('Not enough money!')
            else:
                self.database_driver.execute(f'UPDATE card SET balance = balance + {amount} WHERE number = {card_no}')
                self.database_connector.commit()
                self.database_driver.execute(f'UPDATE card SET balance = balance - {amount} WHERE number = {self.card_no}')
                self.database_connector.commit()
                print('Success!')

    def close_account(self):
        self.database_driver.execute(f'DELETE FROM card WHERE number = {self.card_no};')
        self.database_connector.commit()
        print('The account has been closed!')

        self.card_no = None
        self.customer_login_status = False

    def create_account(self):
        card_no = str(Bank.CARD_NO)
        pin_no = str(Bank.PIN_NO)

        Bank.CARD_NO += 1
        Bank.PIN_NO += 1
        Bank.ID += 1

        card_no = self.adding_luhan_checksum(card_no)
        print(f"Your card has been created\nYour card number:\n{card_no}\nYour card PIN:\n{pin_no}")

        self.database_driver.execute(f"insert into card (id, number, pin, balance) values ({Bank.ID}, {card_no}, {pin_no}, {0});")
        self.database_connector.commit()

    def check_account_validity(self, card_no, pin_no):
        self.database_driver.execute(f'SELECT * FROM card WHERE number = "{card_no}" and pin = "{pin_no}"')
        self.database_connector.commit()

        if self.database_driver.fetchone() is not None:
            return True
        return False

    def adding_luhan_checksum(self,card_no):
        bit = [int(x) for x in card_no]
        bit = [bit[i] * 2 if i % 2 == 0 else bit[i] for i in range(0, len(bit))]
        bit = [x - 9 if x > 9 else x for x in bit]

        sumation = sum(bit)
        checksum = (math.ceil(sumation / 10) * 10) - sumation

        return (card_no + str(checksum))

if __name__ == '__main__':
    bank = Bank()
    bank.operation()
