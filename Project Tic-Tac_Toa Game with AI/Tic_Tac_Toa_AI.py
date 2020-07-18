from itertools import product
from random import choice
from collections import Counter


class OccupiedCell(Exception): 
    pass

class Field:
    coords = sorted(product(range(1, 4), repeat=2), key=lambda a: (- a[1], a[0]))

    def __init__(self, start=None):
        if start is None:
            self.cells = dict(zip(Field.coords, [' ' for n in range(9)]))
        else:
            self.cells = dict(zip(Field.coords, start))
        self.is_X_turn = bool(Counter(self.cells.values())[' '] % 2)
        self.state = 'Game not finished'

    def __str__(self):
        return ('---------\n'
                '| {} {} {} |\n'
                '| {} {} {} |\n'
                '| {} {} {} |\n'
                '---------').format(*self.cells.values())

    @property
    def free_cells(self):
        return [key for key in self.cells if self.cells[key] == ' ']

    def get_symbol(self, current=True):
        return ('X' if self.is_X_turn else 'O') if current else ('O' if self.is_X_turn else 'X')

    def evaluate(self, coord):
        return any(map(lambda a: len(set(a)) == 1 and ' ' not in set(a),
                       [[self.cells[(coord[0]), n] for n in range(1, 4)],
                        [self.cells[n, (coord[1])] for n in range(1, 4)],
                        [self.cells[n, n] for n in range(1, 4)],
                        [self.cells[n, 4 - n] for n in range(1, 4)]
                        ]))

    def update(self, coord, with_current_symbol=True, raise_OccupiedCell=True):
        if any(n < 1 or n > 3 for n in [*coord]):
            raise IndexError
        if raise_OccupiedCell and not self.cells[coord] == ' ':
            raise OccupiedCell

        symbol = self.get_symbol(with_current_symbol)
        self.cells[coord] = symbol
        self.is_X_turn = not self.is_X_turn
        if self.evaluate(coord):
            self.state = "{} wins".format(symbol)
            return True
        elif not Counter(self.cells.values())[' ']:
            self.state = 'Draw'
        return False


class Game:
    def __init__(self):
        self.players = []
        self.field = None
        self.main()

    def user_moves(self):
        while True:
            try:
                x, y = [int(n) for n in input('Enter the coordinates: (x y) > ').split()]
            except ValueError:
                print('You should enter numbers!')
                continue
            try:
                self.field.update((x, y))
            except IndexError:
                print('Coordinates should be from 1 to 3!')
                continue
            except OccupiedCell:
                print('This cell is occupied! Choose another one!')
                continue
            return True

    def make_random_move(self, coords=None):
        coord = choice(self.field.free_cells) if coords is None else choice(coords)
        self.field.update(coord)

    def bot_easy(self):
        print('Making move level "easy"')
        self.make_random_move()

    def get_candidate_moves(self, field=None):
        if field is None:
            field = self.field
        scenarios = {cell: Field(field.cells.values()) for cell in field.free_cells}
        return [cell for cell, field_obj in scenarios.items() if field_obj.update(cell)] or \
               [cell for cell, field_obj in scenarios.items() if field_obj.update(cell, True, False)]

    def bot_medium(self):
        print('Making move level "medium"')
        candidate_moves = self.get_candidate_moves()
        return self.make_random_move(candidate_moves) if candidate_moves else self.make_random_move()

    def minimax(self, field=None, deep=0):
        if field is None:
            field = self.field
        branches = {}
        for cell in field.free_cells:
            scenario = Field(field.cells.values())
            if scenario.update(cell):
                branches[cell] = -1 if deep % 2 else 1
            elif scenario.state.endswith('Draw'):
                branches[cell] = 0
            else:
                branches[cell] = self.minimax(scenario, deep + 1)
        if deep:
            return min(branches.values()) if deep % 2 else max(branches.values())
        else:
            return {
                1: [cell for cell in branches if branches[cell] == 1],
                0: [cell for cell in branches if branches[cell] == 0],
                -1: [cell for cell in branches if branches[cell] == -1]
            }

    def bot_hard(self):
        print('Making move level "hard"')
        all_moves = self.minimax()
        if all_moves[1]:
            return self.make_random_move(all_moves[1])
        if all_moves[0]:
            return self.make_random_move(all_moves[0])
        if all_moves[-1]:
            return self.make_random_move(all_moves[-1])

    @classmethod
    def player_move(cls, key):
        player_move = {
            'user': cls.user_moves,
            'easy': cls.bot_easy,
            'medium': cls.bot_medium,
            'hard': cls.bot_hard
        }
        return player_move[key]

    def play(self):
        print(self.field)
        for turn in range(9 - len(self.field.free_cells), 9):
            Game.player_move(self.players[turn % 2])(self)
            print(self.field)
            if not self.field.state == 'Game not finished':
                print(self.field.state)
                break

    def set_players(self, command):
        try:
            start_command, first_player, second_player = command.split()
            if all(player in ['user', 'easy', 'medium', 'hard'] for player in [first_player, second_player]):
                self.players = [first_player, second_player]
                return True
            else:
                return False
        except ValueError:
            return False

    def main(self):
        while True:
            command = input('Input command: > ')
            if command == 'exit':
                break
            elif self.set_players(command):
                self.field = Field()
                self.play()
            else:
                print('Bad parameters!')


if __name__ == '__main__':
    Game()
