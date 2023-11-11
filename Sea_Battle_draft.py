import random

# Исключение
class BoardOutException(Exception):
    pass
class ShipOutException(Exception):
    pass
class ShotTwiceException(Exception):
    pass

class EndShips(Exception):
    pass


# класс точек, координаты с 0 до 5
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot({self.x}, {self.y})'

# класс кораблей
class Ship:
    def __init__(self, length, head, horizontal):
        self.length = length
        self.head = head
        self.horizontal = horizontal
        #Здоровье при создании равно длинне корабля
        self.hp = length

    # свойство генерации точек корабля
    @property
    def dots(self):
        dots_list = []
        for i in range(self.length):
            dot_x = self.head.x
            dot_y = self.head.y
            if self.horizontal:
                dot_y += i
            else:
                dot_x += i
            dots_list.append(Dot(dot_x, dot_y))
        return dots_list


#Класс доски

class Board:
    def __init__(self, size=6, hid=False):
        self.size = size
        #при hid = true доска противника, скрываем корабли и помогаем стрелять рядом с поврежденным кораблем
        self.hid = hid
        self.field = [['o'] * size for i in range(size)]
        self.ships = []
        self.busy = []
        self.shots = []
        self.ships_count = 0
        self.damaged_dot=Dot(-1,-1)
    # функция добавления корабля
    def add_ship(self, ship):
        for d in ship.dots:
            if d in self.busy or self.out(d):
                raise ShipOutException

        for d in ship.dots:
            self.field[d.y][d.x] = "■"
            self.busy.append(d)
        self.ships.append(ship)
        self.ships_count += 1

    # функция проверки вхождения точки в состав поля
    def out(self, dot):
        return not (0 <= dot.x < self.size and 0 <= dot.y < self.size)

    # функция установки границ корабля
    def set_board(self, ship, show=False):
        boarder=[[i, j] for i in (-1, 0, 1) for j in (-1, 0, 1)]
        for d in ship.dots:
            for cx, cy in boarder:
                c_dot = Dot(d.x + cx, d.y + cy)
                if not self.out(c_dot):
                    if self.field[c_dot.y][c_dot.x] != "T" and self.field[c_dot.y][c_dot.x] != 'X':
                        if show:
                            self.field[c_dot.y][c_dot.x] = '.'
                            self.shots.append(Dot(c_dot.x, c_dot.y))
                        else:
                            self.busy.append(c_dot)

    # функция выстрела
    def shot(self, dot):
        check=False
        #Помощь компьютеру стрелять рядом с поврежденной клеткой

        if not(self.hid) and self.damaged_dot!=Dot(-1,-1):
            print("раненая точка",self.damaged_dot)
            if bool(random.randint(0,1)):
                count = 1
            else:
                count = -1
            if bool(random.randint(0,1)):
                dot_ai = Dot(self.damaged_dot.x+count,self.damaged_dot.y)
            else:
                dot_ai = Dot(self.damaged_dot.x, self.damaged_dot.y+count)
            print("Компьютер передумал и стреляет в координаты: ", dot_ai)
            dot = dot_ai

        if self.out(dot):
            print("Выстрел за пределами поля")
            raise BoardOutException()
        if dot in self.shots:
            print("Выстрел в это поле уже проводился")
            raise ShotTwiceException()
        self.busy.append(dot)
        self.shots.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                self.field[dot.y][dot.x] = 'X'
                ship.hp -= 1
                if ship.hp == 0:
                    print('Корабль убит')
                    self.set_board(ship, show=True)
                    self.ships_count -= 1
                    print(self)
                    check = True
                    if not(self.hid):
                        self.damaged_dot=Dot(-1,-1)

                else:
                    print('Корабль ранен')
                    print(self)
                    if not(self.hid):
                        self.damaged_dot = dot
                check = True
        if not(check):
            self.field[dot.y][dot.x] = 'T'
            print('Мимо, смена хода')
        return check
    # функция вывода состояния поля
    def __str__(self):
        s = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, j in enumerate(self.field):
            s += f'\n{i + 1} | ' + ' | '.join(j) + ' |'
        if self.hid:
            s = s.replace('■', 'o')
        return s

class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        dot1=Dot(7,5)
        return dot1

    def move(self):
        while True:
            try:
                if not self.enemy_board.shot(self.ask()):
                    return True
            except BoardOutException:
                print("Вы стреляете за пределы поля, стреляйте еще раз")
                continue
            except ShotTwiceException:
                print("Вы сюда уже стреляли, стреляйте еще раз")
                continue
            except EndShips:
                print("Корабли закончились")
                return False


class User(Player):
    def ask(self):
        while True:
            if self.enemy_board.ships_count != 0:
                s=input("Введите координаты выстрела в формате X Y")
                try:
                    x=int(s[0])
                    y=int(s[-1])
                except ValueError:
                        print("Введите целое число")
                        continue
                else:
                    return Dot(x - 1, y - 1)
            else:
                raise EndShips

class AI(Player):
    def ask(self):
        dot1 = Dot(random.randint(0, self.board.size - 1), random.randint(0, self.board.size - 1))
        print("Компьютер стреляет в координаты: ", Dot(dot1.x+1,dot1.y+1))
        return dot1

class Game():
    def __init__(self):
        self.user_board = self.random_board(False)
        self.ai_board = self.random_board(True)
        self.player = User(self.user_board,self.ai_board)
        self.ai = AI(self.ai_board,self.user_board)

    def random_board_draft(self, hide):
        board1 = Board(6, hide)
        ship_size_list = [3, 2, 2, 1, 1, 1, 1]
        for ship_size in ship_size_list:
            #Оказывается не всегда на поле можно разместить все корабли, защита от бесконечного цикла
            trys = 0
            while True:
                try:
                    ship = Ship(ship_size, Dot(random.randint(0, board1.size), random.randint(0, board1.size)), bool(random.randint(0,1)))
                    board1.add_ship(ship)
                    board1.set_board(ship,False)
                    break
                except ShipOutException:
                    trys+=1
                    if trys<1000:
                        continue
                    else:
                        return False
        return board1

    def random_board(self, hide):
        board1=self.random_board_draft(hide)
        while not(board1):
            board1=self.random_board_draft(hide)
        return board1

    def greet(self):
        print("Добро пожаловать в игру ""Морской Бой\n"
              "Она написана в рамках итогового задания продолжения погружения в ООП\n"
              "SkilFactory студентом Тимофеем Буенковым\n"
              "Корабли расставятся автоматически\n"
              "Компьютер будет ходить сам, Вам же придется вводить координаты ввода с клавиаьуры\n"
              "не переживайте сделать что-то неправильно, компьютер поправит Вас, если Вы выстрелите за пределы поля или повторно\n"
              "отображаться будут 2 доски, очередь хода и количество непотопленных кораблей\n"
              "компьютер вашу доску не видит, честно)))\n"
                "Удачи Вам\n"
              "Это ваша доска:")
        print(self.user_board)

    def mode(self):
        if self.user_board.ships_count == 0:
            print("Победил КОмпьютер")
            return False
        elif self.ai_board.ships_count == 0:
            print("Победил Игрок")
            return False
        else:
            return True



    def loop(self):

        while self.mode():
            print("Ваш ход игрок, карта для стрельбы:")
            print(self.ai_board)
            print("Живых кораблей противника осталось: ",self.ai_board.ships_count)
            print("Ваших кораблей осталось: ", self.user_board.ships_count)
            self.player.move()
            print(self.ai_board)
            if self.ai_board.ships_count != 0:
                print("Ход компьютера")
                self.ai.move()
                print(self.user_board)
    def start(self):
        self.greet()
        self.loop()

game1 = Game()
game1.start()
