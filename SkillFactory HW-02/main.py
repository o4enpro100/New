

field = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
side = 'x'

def print_field():
    print("  1 2 3")
    for i in range(3):
        print(i+1, field[i][0], field[i][1], field[i][2])

def swap_side(side): return 'o' if side == 'x' else 'x'

def step():
    x, y = map(int, input(f"Ход {side.upper()}. Введите 2 числа через пробел (1..3): ").split())
    if not (1 <= x < 4) or not ((1 <= y < 4)):
        print("Некорректный ввод (Пример: '3 1)'")
        return False
    if (field[x-1][y-1] == 'x') or (field[x-1][y-1] == 'o'):
        print("Ячейка уже занята! Повторите ввод.")
        return False
    field[x-1][y-1] = side
    return True

def win():

    def getline(row = -1, col = -1):
        if col == -1: return field[row][0] + field[row][1] + field[row][2]
        elif row == -1: return field[0][col] + field[1][col] + field[2][col]

    def check_win(line):
        if line == 'xxx':
            print("Выиграли X!")
            return True
        elif line == 'ooo':
            print("Выиграли O!")
            return True
        return False

    for i in range(3):
        if (check_win(getline(row = i))) or (check_win(getline(col = i))): return True
    if check_win(field[0][0]+field[1][1]+field[2][2]): return True
    if check_win(field[0][2]+field[1][1]+field[2][0]): return True
    return False

print_field()
while not win():
    while not step(): pass
    print_field()
    side = swap_side(side)
