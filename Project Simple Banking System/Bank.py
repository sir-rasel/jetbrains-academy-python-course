import math

class Bank:
    customer_account = dict()
    CARD_NO = 400000000000000
    PIN_NO = 1000

    def __init__(self):
        self.banking_status = True
        self.customer_login_status = False
    
    def __str__(self):
        if self.customer_login_status:
            return "1. Balance\n2. Log out\n0. Exit"
        else:
            return "1. Create an account\n2. Log into account\n0. Exit"
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
                    pin_no = input('Enter your PIN: ')

                    if self.check_account_validity(card_no, pin_no):
                        self.customer_login_status = True
                        print('You have successfully logged in!')
                    else:
                        print('Wrong card number or PIN!')
        print('Bye!')

    def create_account(self):
        card_no = str(Bank.CARD_NO)
        pin_no = str(Bank.PIN_NO)

        Bank.CARD_NO += 1
        Bank.PIN_NO += 1

        card_no = self.adding_luhan_checksum(card_no)

        Bank.customer_account[card_no] = pin_no
        print(f"Your card has been created\nYour card number:\n{card_no}\nYour card PIN:\n{pin_no}")
    
    def check_account_validity(self, card_no, pin_no):
        if Bank.customer_account.get(card_no, str(-1)) == pin_no:
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
