import random

class Bank:
    customer_account = dict()
    IIN = 400000

    def __init__(self):
        self.banking_status = True
        self.customer_login_status = False
    
    def __str__(self):
        if self.customer_login_status:
            return " 1. Balance \n 2. Log out \n 0. Exit"
        else:
            return " 1. Create an account \n 2. Log into account \n 0. Exit"
    def operation(self):
        while self.banking_status:
            print(self)
            choice = int(input())
            
            if choice == 0:
                break
            elif self.customer_login_status:
                if choice == 1:
                    print('Balance: 0')
                else:
                    self.customer_login_status = False
                    print('You have successfully logged out!')
            else:
                if choice == 1:  
                    self.create_account()
                else:
                    card_no = input('Enter your card number: ')
                    pin_no = int(input('Enter your PIN: '))

                    if self.check_account_validity(card_no, pin_no):
                        self.customer_login_status = True
                        print('You have successfully logged in!')
                    else:
                        print('Wrong card number or PIN!')
        print('Bye!')

    def create_account(self):
        account_number = random.randint(0000000000, 9999999999)
        card_no = str(Bank.IIN) + str(account_number)
        pin_no = random.randint(0000, 9999)

        Bank.customer_account[card_no] = pin_no
        print(f" Your card has been created \n Your card number: \n {card_no} \n Your card PIN: \n {pin_no}")
    
    def check_account_validity(self, card_no, pin_no):
        if Bank.customer_account.get(card_no, str(-1)) == pin_no:
            return True
        return False

if __name__ == '__main__':
    bank = Bank()
    bank.operation()