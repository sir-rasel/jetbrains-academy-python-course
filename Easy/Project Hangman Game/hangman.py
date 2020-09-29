import random

class Hangman:
    def __init__(self,word_list = ['python', 'java', 'kotlin', 'javascript']):
        self.word_list = word_list

        self.lives = None
        self.acceptable_word = None
        self.covered_letter = None
        self.choosen_letter = None
        self.needed_letter = None
        self.remain_letter = None

    def action(self):
        while True:
            choice = input('Type "play" to play the game, "exit" to quit:')
            if choice == "play":
                self.play_game()
            elif choice == "exit":
                return

    def start_game(self):
        print("H A N G M A N")
        random.seed()
        self.lives = 8
        self.acceptable_word = random.choice(self.word_list)
        self.covered_letter = list("-" * len(self.acceptable_word))
        self.choosen_letter = set()
        self.needed_letter = set(self.acceptable_word)
        self.wining_state = False
        self.remain_letter = len(self.acceptable_word)

    def play_game(self):
        self.start_game()
    
        while self.lives and self.remain_letter:
            print()
            print("".join(self.covered_letter))
            guess = input("Input a letter:",)
            if len(guess) != 1:
                print("You should input a single letter")
            elif guess in self.choosen_letter:
                print("You already typed this letter")
            elif guess.islower() == False:
                print("It is not an ASCII lowercase letter")
            elif guess in self.needed_letter:
                self.choosen_letter.add(guess)
                self.change_resulting_word(guess)
            else:
                self.choosen_letter.add(guess)
                print("No such letter in the word")
                self.lives -= 1

        self.check_wining_status()

    def change_resulting_word(self, guess):
        for i in range(0,len(self.acceptable_word)):
            if self.acceptable_word[i] == guess:
                self.covered_letter[i] = guess
                self.remain_letter -= 1
        
    def check_wining_status(self):
        if self.remain_letter == 0:
            print("You guessed the word! {}{}You survived!".format("".join(self.covered_letter), "\n"))
        else:
            print("You are hanged!")

instance = Hangman()
instance.action()