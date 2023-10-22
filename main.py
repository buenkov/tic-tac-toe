#функция создания игрового поля
def creating_board():
    index_board = [[i, j] for i in range(1, 4) for j in range(1, 4)]
    dict_board = {}
    for index in index_board:
        dict_board[tuple(index)] = "-"

    return dict_board

#функция вывода состояния игрового поля
def view_board(dict_board):
    print("  1 2 3")
    for i in (1,2,3):
        s=str(i)
        for j in (1,2,3):
            s = s + " " + dict_board[i,j]
        print(s)

#функция смены хода
def change_move():
    symbols = ["x", "o"]
    i = 0
    while True:
        yield symbols[i]
        i = (i + 1) % len(symbols)


#функция хода и записи
def moving(move):
    s=input(f"Сейчас ходит игрок {move}, Введите через пробел диапазон, куда поставим символ {move}:")
    if not((s[0] in ["1","2","3"])and(s[-1] in ["1","2","3"])):
        print("Вы ввели неправильные координаты. Введите пож-ста число от 1 до 3, затем пробел и еще одно число от 1 до 3-ех")
        return moving(move)
    if dict_board[int(s[0]),int(s[-1])] == "-":
        dict_board[int(s[0]),int(s[-1])] = move
        return dict_board
    else:
        print("Это поле занято выберите другое")
        return moving(move)


#функция проверки выигрыша по диагоналям
def check_diagonals(winner):
    check = False
    if all([dict_board[1,1] == winner,
            dict_board[2,2] == winner,
            dict_board[3,3] == winner]):
        check = True
    if all([dict_board[1,3] == winner,
            dict_board[2,2] == winner,
            dict_board[3,1] == winner]):
        check = True
    if check:
        return winner
    else:
        return "-"


#функция проверки выигрыша по горизонталям и вертикалям
def check_winner_r_c(winner):
    for i in range(1,4):
        rows = True
        columns = True
        for j in range(1,4):
            rows = rows * dict_board[i,j] == winner
            columns = columns * dict_board[j, i] == winner
        if rows+columns:
            return winner
            break
    else:
        return "-"
#функция проверки выигрыша по горизонталям и вертикалям
def check_winners(winner):
    if (check_winner_r_c(winner) != "-")or(check_diagonals(winner)!="-"):
        return winner
    else:
        return "-"

#функция проверки на ничью
def check_draw():
    draw = True
    for i in range(1,4):
        for j in range(1,4):
            draw = draw and dict_board[i,j] != "-"
    if draw:
        return True
    else:
        return False


#сама программа

dict_board = creating_board()
move_generator = change_move()
view_board(dict_board)


while True:
    if check_draw():
        print("Ничья")
        break
    else:
        move = next(move_generator)
        moving(move)
        view_board(dict_board)
        if check_winners("x") == "x":
            print("Победил x")
            break
        elif check_winners("o") == "o":
            print("Победил o")
            break
