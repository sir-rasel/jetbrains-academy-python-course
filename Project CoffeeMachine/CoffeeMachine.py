class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.disposable_cups = 9
        self.money = 550

        self.state = None

    def __str__(self):
        return ("The coffee machine has:\n" 
        + "{} of water\n".format(self.water) 
        + "{} of milk\n".format(self.milk)
        + "{} of coffee beans\n".format(self.coffee_beans)
        + "{} of disposable cups\n".format(self.disposable_cups)
        + "{} of money\n".format(self.money))

    def remaining(self):
        print("The coffee machine has:")
        print("{} of water".format(self.water))
        print("{} of milk".format(self.milk))
        print("{} of coffee beans".format(self.coffee_beans))
        print("{} of disposable cups".format(self.disposable_cups))
        print("{} of money".format(self.money))

    def buy_espresso(self):
        if self.water < 250:
            print("Sorry, not enough water!")
        elif self.coffee_beans < 16:
            print("Sorry, not enough coffee beans!")
        elif self.disposable_cups < 1:
            print("Sorry, not enough disposable cups!")
        else:
            self.money += 4
            self.water -= 250
            self.coffee_beans -= 16
            self.disposable_cups -= 1
            print("I have enough resources, making you a coffee!")

    def buy_latte(self):
        if self.water < 350:
            print("Sorry, not enough water!")
        elif self.milk < 75:
            print("Sorry, not enough milk!")
        elif self.coffee_beans < 20:
            print("Sorry, not enough coffee beans!")
        elif self.disposable_cups < 1:
            print("Sorry, not enough disposable cups!")
        else:
            self.money += 7
            self.water -= 350
            self.milk -= 75
            self.coffee_beans -= 20
            self.disposable_cups -= 1
            print("I have enough resources, making you a coffee!")

    def buy_cappuccino(self):
        if self.water < 200:
            print("Sorry, not enough water!")
        elif self.milk < 100:
            print("Sorry, not enough milk!")
        elif self.coffee_beans < 12:
            print("Sorry, not enough coffee beans!")
        elif self.disposable_cups < 1:
            print("Sorry, not enough disposable cups!")
        else:
            self.money += 6
            self.water -= 200
            self.milk -= 100
            self.coffee_beans -= 12
            self.disposable_cups -= 1
            print("I have enough resources, making you a coffee!")

    def buy(self):
        choosen_coffee = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:",)
        
        if choosen_coffee == "back":
            return

        choosen_coffee = int(choosen_coffee)
        if choosen_coffee == 1:
            self.buy_espresso()
        elif choosen_coffee == 2:
            self.buy_latte()
        else:
            self.buy_cappuccino()

    def fill(self):
        self.water += int(input("Write how many ml of water do you want to add:",))
        self.milk += int(input("Write how many ml of milk do you want to add:",))
        self.coffee_beans += int(input("Write how many grams of coffe beans do you want to add:",))
        self.disposable_cups += int(input("Write how many disposable cups of coffee do you want to add:",))
            
    def take(self):
        print("I gave you ${}".format(self.money))
        self.money = 0
    
    def choose_action(self):
        self.state = input("Write action (buy, fill, take, remaining, exit):",)
        if self.state == "buy":
            self.buy()
        elif self.state == "fill":
            self.fill()
        elif self.state == "take":
            self.take()
        elif self.state == "remaining":
            self.remaining()
        return self.state

# Test machine operation
machine = CoffeeMachine()
while machine.choose_action() != "exit":
    pass
# print(machine)