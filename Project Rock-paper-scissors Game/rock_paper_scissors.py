from random import choice

default_list_ = ["paper", "scissors", "rock"]
chosen_list_ = list()
ratings = dict()

def get_data_from_file():
    global ratings
    with open('rating.txt', 'r') as file:
        for line in file:
            line = line.strip('\n').split()
            ratings[line[0]] = int(line[1])

def set_data_into_file():
    global ratings
    with open('rating.txt', 'w') as file:
        for item in ratings:
            file.writelines(item + ' ' + str(ratings[item]) + '\n' )

def update_rating(new_score, player_name):
    global ratings
    if player_name not in ratings:
        ratings[player_name] = 0
    else:
        ratings[player_name] += new_score

def get_rating(player_name):
    global ratings
    if player_name not in ratings:
        ratings[player_name] = 0
    return ratings[player_name]

def isWin(player_choice, computer_choice):
    global chosen_list_

    player_index = chosen_list_.index(player_choice)
    new_list_ = chosen_list_[player_index + 1:] + chosen_list_[:player_index]

    computer_index = new_list_.index(computer_choice)

    if computer_index < len(new_list_) // 2:
        return False
    return True
    
def play_game():
    global default_list_, chosen_list_, current_rating
    player_name = input("Enter your name: ")
    print("Hello, {}".format(player_name))
    
    chosen_list_ = input().replace(" ", "").split(",")
    if chosen_list_[0] == '':
        chosen_list_ = default_list_
    
    print("Okay, let's start")
    current_rating = ratings[player_name] if player_name in ratings else 0

    while True:
        player_choice = input()

        if player_choice == "!exit":
            break
        elif player_choice == "!rating":
            print("Your rating:", get_rating(player_name))
        elif player_choice not in chosen_list_:
            print("Invalid input")
        else:
            computer_choice = choice(chosen_list_)
            if computer_choice == player_choice:
                print("There is a draw ({})".format(computer_choice))
                update_rating(50, player_name)
            else:
                win_status = isWin(player_choice, computer_choice)
                if win_status == True:
                    print("Well done. Computer chose {} and failed".format(computer_choice))
                    update_rating(100, player_name)
                else:
                    print("Sorry, but computer chose {}".format(computer_choice))

    print("Bye!")

get_data_from_file()
play_game()
set_data_into_file()