from random import randint

class BoardException(Exception):
    pass

class Ship:
    def __init__(self, size, bow, direction):
        self.size = size
        self.bow = bow
        self.direction = direction
        self.lives = size

    @property
    def dots(self):
        location_ = []
        for i in range(self.size):
            c = [self.bow[0], self.bow[1]]
            c[0 if self.direction else 1] += i
            location_.append(tuple(c))
        return location_


#•  ■  ✕ ⊗ ⨷

class Board:
    def __init__(self, hide):
        self.field = [[' ' for _ in range(6)] for _ in range(6)]
        self.hide = hide
        self.ships = []
        self.dead_ship = 0

    def add_ship(self, size):
        s = Ship(size, [randint(0, 6-size), randint(0, 6-size)], randint(0, 1))
        for h, v in s.dots:
            if self.field[h][v] == ' ':
                self.field[h][v] = '■'
            else: return
        self.ships.append(s)
        self.contour(s.dots)

    def contour(self, ship):
        at = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]
        for i in ship:
            for x, y in at:
                dot = (i[0] + x, i[1] + y)
                if 0 <= dot[0] < 6 and 0 <= dot[1] < 6:
                    if dot not in ship:
                        self.field[dot[0]][dot[1]] = '•'

    def end_draw(self):
        self.field = [[' ' for _ in range(6)] for _ in range(6)]
        if self.hide == False:
            for s in self.ships:
                for x, y in s.dots:
                    self.field[x][y] = '■'

    def shot(self, dot):
        x, y = dot
        for s in self.ships:
            if dot in s.dots:
                self.field[x][y] = '⊗'
                s.lives -= 1
                if s.lives == 0:
                    self.contour(s.dots)
                    self.dead_ship += 1
                return 1
        if self.field[x][y] == ' ':
            self.field[x][y] = '•'
        elif self.field[x][y] == '•' or self.field[x][y] == '⊗':
            print('Клетка занята!')
            return 2
        return 3

class Player:
    def ask(self):
        pass

class User(Player):
    def ask(self, f):
        while True:
            dot = input('Введите координаты: ').split()
            print()

            try:
                if len(dot) != 2:
                    raise BoardException('Введите 2 координаты!')

                x, y = dot

                if not x.isdigit() or not y.isdigit():
                    raise BoardException('Введите числа!')

                x, y = int(x), int(y)

                if 0 > x or x > 5 or 0 > y or y > 5:
                    raise BoardException('Неверные координаты!')
                break
            except BoardException as e:
                print(e)
                continue

        return (x, y)

class AI(Player):
    def ask(self):
        x, y = randint(0, 5), randint(0, 5)
        return (x, y)

class Game:
    def __init__(self):
        self.user = User()
        self.ai = AI()
        self.board_player = self.generate_board(False)
        self.board_ai = self.generate_board(True)

    def greet(self):
        print('''
Здравствуйте! Проект "Морской Бой".
Чтобы сделать ход, введите координаты.
Пример: x y
''')

    def generate_board(self, hide):
        ships = [3, 2, 2, 1, 1, 1, 1]
        while True:
            board = Board(hide)
            for i in ships:
                board.add_ship(i)
            if len(board.ships) == len(ships):
                board.end_draw()
                return board
                break
            else:
                continue

    def start(self):
        self.greet()
        self.move()

    def draw_boards(self):
        print('  | 0  1  2  3  4  5 |\t\t\t\t  | 0  1  2  3  4  5 |')
        for r in range(6):
            row = '  '.join(self.board_player.field[r])
            row_ai = '  '.join(self.board_ai.field[r])
            print(f'{r} | {row} |\t\t\t\t{r} | {row_ai} |')
        print()

    def check(self, board):
        if board.dead_ship == len(board.ships):
            self.draw_boards()
            return True
        return False

    def move(self):
        step = 1
        while True:
            self.draw_boards()
            if step == 1:
                dot = self.user.ask(self.board_ai)
                shot = self.board_ai.shot(dot)
                if self.check(self.board_ai):
                    return print('Победил пользователь!')
            else:
                dot = self.ai.ask()
                shot = self.board_player.shot(dot)
                self.check(self.board_player)
                if self.check(self.board_player):
                    return print('Победил ИИ!')
            if shot == 3:
                step = 1 if step == 0 else 0



game = Game()
game.start()

