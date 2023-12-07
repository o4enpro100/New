import random

class Pos:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return str(self.x, self.y)

class ShipOnePos(Pos):
    def __init__(self, x, y, visible=True, alive=True):
        super().__init__(x, y)
        self.visible = visible
        self.alive = alive

class Ship:
    def __init__(self, position) -> None:
        self.lvl = len(position)
        self.pos = position

    def __str__(self):
        message = f"Ship lvl={self.lvl}: "
        for _pos in self.pos:
            message += f'({str(_pos.x+1)}, {_pos.y+1}) '
        return message

    @staticmethod
    def GenShip(lvl, w, h):
        pos = []
        down_right = random.randint(0, 1)
        if down_right:
            x = random.randint(0, w - 1)
            y = random.randint(0, h - lvl)
            for i in range(lvl):
                pos.append(Pos(x, y + i))
        else:
            x = random.randint(0, w - lvl)
            y = random.randint(0, h - 1)
            for i in range(lvl):
                pos.append(Pos(x + i, y))

        return Ship(pos)


class GameBoard:

    def __init__(self, w, h, ships, display=[' ', '\u25A0', 'X', 'T']) -> None:
        self.width = w
        self.height = h
        self.space = display[0]
        self.disp_ship = display[1]
        self.hit = display[2]
        self.miss = display[3]
        self.ships_points = self.countShipPoints(ships)
        self.hit_count = 0
        self.clearBoard()
        # self.board = [[self.space] * self.width for i in range(self.height)]

        i = 0
        while not self.genereteAllShips(ships):
            i += 1
            if i > 1000:
                self.ready = False
                return
        self.ready = True


    def getBoard(self):
        return self.board

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getSpace(self):
        return self.space

    def getCell(self, x, y):
        return self.board[x][y]

    def setCell(self, x, y, simb):
        self.board[x][y] = simb

    def clearBoard(self):
        self.board = [[self.space] * self.width for i in range(self.height)]

    def addShipToBoard(self, ship):
        for _pos in ship.pos:
            self.board[_pos.x][_pos.y] = self.disp_ship

    def addShip1lvlInFreeCell(self):
        for i in range(0, self.width-1):
            for j in range(0, self.height-1):
                ship = Ship([Pos(i, j)])
                if self.checkCollision(ship):
                    return ship
        return None

    def addNewShip(self, lvl):
        ship = Ship.GenShip(lvl, self.width, self.height)
        i = 0
        while not self.checkCollision(ship):
            ship = Ship.GenShip(lvl, self.width, self.height)
            i += 1
            if i > 100:
                if lvl == 1:
                    ship = self.addShip1lvlInFreeCell()
                    if ship != None:
                        break
                return False
        self.addShipToBoard(ship)
        return True

    def genereteAllShips(self, ships):
        for ship in ships:
            for i in range(ship[1]):
                if not self.addNewShip(ship[0]):
                    self.clearBoard()
                    return False
        return True

    def checkCollision(self, ship):
        for _pos in ship.pos:
            for i in range(3):
                for j in range(3):
                    x = _pos.x + i - 1
                    y = _pos.y + j - 1
                    if not (0 <= x <= self.width-1) or not (0 <= y <= self.height-1):
                        continue
                    if self.board[x][y] != self.space:
                        return False
        return True

    def countShipPoints(self, ships):
        count = 0
        for ship in ships:
            count += ship[0] * ship[1]
        return count

class GameGui:
    def __init__(self, width, height, user_board, PC_board):
        self.width = width
        self.height = height
        self.user_board = user_board
        self.PC_board = PC_board
        self.last_message = ''
        self.message_history = []
        self.side = 0

    def askPosToHit(self):
        try:
            x, y = map(int, input("Введите координаты цели (два числа через пробел):").split())
        except ValueError as e:
            self.last_message = 'Не правильный ввод данных (введите числа). Повторите снова!'
            return Pos(0, 0)
        if not (0 < x <= self.width) or not ((0 < y <= self.height)):
            self.last_message = 'Координаты не попадают в диапазон поля. Повторите снова!'
            return Pos(0, 0)
        return Pos(x, y)

    def swapSide(self):
        self.side = 0 if self.side == 1 else 1

    def addMessage(self, message):
        self.message_history.append(message)
        if len(self.message_history) > 5:
            self.message_history.pop(0)

    def printHistory(self):
        print('')
        print('')
        for i in range(len(self.message_history)):
            print(self.message_history[i])

    def GameRuin(self):

        while self.checkWin():
            if self.side == 0:
                self.printHistory()
                self.DrawTwoBoard()
                print(self.last_message)
                hit_pos = self.askPosToHit()
                while hit_pos == Pos(0, 0):
                    self.DrawTwoBoard()
                    print()
                    print(self.last_message)
                    self.last_message = ''
                    hit_pos = self.askPosToHit()
                if ((PC_board.getCell(hit_pos.x-1, hit_pos.y-1) == PC_board.hit)
                        or (PC_board.getCell(hit_pos.x-1, hit_pos.y-1) == PC_board.miss)):
                    self.addMessage('Вы уже стреляли сюда! Выберите новую цель')
                    continue
                if PC_board.getCell(hit_pos.x-1, hit_pos.y-1) == PC_board.disp_ship:
                    PC_board.setCell(hit_pos.x-1, hit_pos.y-1, self.PC_board.hit)
                    self.addMessage('Вы попали! Стреляйте снова!')
                    PC_board.hit_count += 1
                else:
                    PC_board.setCell(hit_pos.x-1, hit_pos.y-1, self.PC_board.miss)
                    self.printHistory()
                    self.DrawTwoBoard()
                    self.addMessage('Вы промахнулись! Ход переходит к сопернику.')
                    print('Вы промахнулись! Ход переходит к сопернику.')
                    input('Нажмите Enter для продолжения:')
                    self.side = 1
            else:
                #  Compucter
                self.printHistory()
                self.DrawTwoBoard()
                hit_pos = Pos(random.randint(0, self.width-1), random.randint(0, self.height-1))
                while ((user_board.getCell(hit_pos.x, hit_pos.y) == user_board.hit)
                       or (user_board.getCell(hit_pos.x, hit_pos.y) == user_board.miss)):
                        hit_pos = Pos(random.randint(0, self.width-1), random.randint(0, self.height-1))

                if user_board.getCell(hit_pos.x, hit_pos.y) == user_board.disp_ship:
                    user_board.setCell(hit_pos.x, hit_pos.y, self.user_board.hit)
                    self.addMessage(f'Компьютер стреляет в точку ({hit_pos.x+1}:{hit_pos.y+1}) и попадает по Вашему кораблю. Компьютер стреляет снова!')
                    self.printHistory()
                    self.DrawTwoBoard()
                    user_board.hit_count += 1
                    print('')
                    input('Нажмите Enter для продолжения:')
                else:
                    user_board.setCell(hit_pos.x, hit_pos.y, self.user_board.miss)
                    self.addMessage(f'Компьютер стреляет в точку ({hit_pos.x+1}:{hit_pos.y+1}) и промахивается. Ход переходит к Вам, стреляйте!!')
                    self.side = 0

    def checkWin(self):
        if user_board.hit_count == user_board.ships_points:
            print('ВЫ ПРОИГРАЛИ!')
            return False
        if PC_board.hit_count == PC_board.ships_points:
            print('ВЫ ПОБЕДИЛИ!')
            return False
        return True

    def DrawTwoBoard(self):
        user_board = self.user_board.getBoard()
        PC_board = self.PC_board.getBoard()
        print()
        spl = ' '
        print(' Поле пользователя:', '\t'*(self.width+1), 'Поле компьютера:')
        up_str = [f'{i+1} |' for i in range(self.width)]
        print('  |', *up_str, '\t' * 5, '  |', *up_str)
        #print(' ',*[f'{i+1} |' for i in range(self.width)], '\t'*5, *[f'{i+1} |' for i in range(self.width)])

        for i in range(self.width):
            if i > 8: spl = ''

            spl2 = ''
            one_str = spl + str(i+1) + '| '
            for j in range(self.height):
                if j > 8: spl2 = ' '
                one_str += user_board[i][j] + spl2 + ' | '

            spl2 = ''
            one_str += '\t'*5 + spl + str(i+1) + ' | '
            for j in range(self.height):
                if j > 8: spl2 = ' '
                if PC_board[i][j] == self.PC_board.disp_ship:
                    one_str += self.PC_board.space + spl2 + ' | '
                else:
                    one_str += PC_board[i][j] + spl2 + ' | '

            print(one_str)
        print('')
        print(f' (Поражено {self.user_board.hit_count} из {self.user_board.ships_points})', '\t'*(self.width+1),
              f'(Поражено {self.PC_board.hit_count} из {self.PC_board.ships_points})')


if __name__ == '__main__':
    # const
    board_width = 6
    board_height = 6
    display = ['0', '\u25A0', 'X', 'T']   # [space, ship, miss, hit]
    quantity_ships = [[5, 0], [4, 0], [3, 1], [2, 2], [1, 4]]   # [lvl, quantity]

    user_board = GameBoard(board_width, board_height, quantity_ships, display)
    PC_board = GameBoard(board_width, board_height, quantity_ships, display)
    if (not user_board.ready) or (not PC_board.ready):
        print('Не могу создать игру с такими условиями!')

    gui = GameGui(board_width, board_height, user_board, PC_board)
    gui.GameRuin()
