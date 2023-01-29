import math
import random as r

from enums import Play_modes, Win_types


BOARD_SIZE:tuple[int, int]  = (8, 6)
CONNECT_NUM:int             = 4
PLAYER_SYMBOLS:list[str]    = ['O', 'X', 'Z', 'G']
PLAYER_NAMES:list[str]      = []
PLAY_MODE:Play_modes        = Play_modes.P_PC


PLAYER_RATIO_IN_P_PC_MODE:float = (1/len(PLAYER_SYMBOLS))
PLAYER_RATIO_IN_PC_P_MODE:float = 0.5
EMPTY_SYMBOL:str    = '.'
BOARD_SEP:str       = " "
BOARD_BORDER:str    = "|"


PLAYER_NUM = len(PLAYER_SYMBOLS)


turn_num = 0
# False = Computer, True = Player
player_types:list[bool] = []




def make_board():
    board:list[list[str]] = []
    for _ in range(BOARD_SIZE[1]):
        board_row = []
        for _ in range(BOARD_SIZE[0]):
            board_row.append(EMPTY_SYMBOL)
        board.append(board_row)
    return board


def get_player_num(turn_number:int|None=None):
    if turn_number is None:
        turn_number = turn_num
    return (turn_number - 1) % PLAYER_NUM


def get_player_symbol(player_num:int|None = None):
    if player_num is None:
        player_num = get_player_num()
    if 0 <= player_num < PLAYER_NUM:
        return PLAYER_SYMBOLS[player_num]
    else:
        return 'E'


def get_player_type(player_num:int|None = None):
    if player_num is None:
        player_num = get_player_num()
    if 0 <= player_num < PLAYER_NUM:
        return player_types[player_num]
    else:
        return True


def get_player_name(player_num:int|None = None):
    if player_num is None:
        player_num = get_player_num()
    if 0 <= player_num < PLAYER_NUM:
        return PLAYER_NAMES[player_num]
    else:
        return '[ERROR]'


def make_player_types():
    global player_types
    for x in range(PLAYER_NUM):
        if PLAY_MODE == Play_modes.P_P:
            player_types.append(True)
        elif PLAY_MODE == Play_modes.PC_PC:
            player_types.append(False)
        elif PLAY_MODE == Play_modes.P_PC:
            player_types.append(True if (x + 1) / PLAYER_NUM <= PLAYER_RATIO_IN_P_PC_MODE else False)
        elif PLAY_MODE == Play_modes.PC_P:
            player_types.append(True if (x + 1) / PLAYER_NUM > PLAYER_RATIO_IN_PC_P_MODE else False)


def correct_player_names():
    global PLAYER_NAMES
    total_p_num = player_types.count(True)
    total_c_num = player_types.count(False)
    p_num = 0
    c_num = 0
    for x in range(PLAYER_NUM):
        if len(PLAYER_NAMES) <= x:
            if player_types[x]:
                name = f"Player{'' if total_p_num == 0 else f' {p_num + 1}'}"
                p_num += 1
            else:
                name = f"Computer{'' if total_c_num == 0 else f' {c_num + 1}'}"
                c_num += 1
            PLAYER_NAMES.append(name)


def get_computer_move(text, board:list[list[str]]):
    move = -1
    check_result = (False, -1)
    while not check_result[0]:
        # computer making move logic
        move = int(r.randint(0, BOARD_SIZE[0] - 1))
        
        check_result = check_valid_move(move, board, False)
    print(f"{text}{move + 1}")
    return move


def get_player_move(text:str):
    move = None
    while move is None:
        try: move = int(input(text))
        except TypeError: print("Not a number!")
    return move - 1


def get_move(board:list[list[str]]):
    move = -1
    p_name = get_player_name()
    symbol = get_player_symbol()
    text = f"{p_name} ({symbol}) move: "
    if get_player_type():
        move = get_player_move(text)
    else:
        move = get_computer_move(text, board)
    return move

def check_valid_move(move:int, board:list[list[str]], write_out=True) -> tuple[bool, int]:
    if move < 0 or move >= BOARD_SIZE[0]:
        if write_out:
            print(f"Column number should be between 1 and {BOARD_SIZE[0]}")
        return (False, -1)
    else:
        for x in range(len(board) - 1, -1, -1):
            if board[x][move] == EMPTY_SYMBOL:
                return (True, x)
        return (False, -1)


def make_move(move:int, board:list[list[str]]):
    check_result = check_valid_move(move, board)
    if check_result[0]:
        board[check_result[1]][move] = get_player_symbol()
        return (check_result[1], move)
    else:
        return None


def check_spot(pos:tuple[int, int], symbol:str, board:list[list[str]]):
    return board[pos[0]][pos[1]] == symbol


def check_row(symbol:str, pos:tuple[int, int], board:list[list[str]]):
    same = 0
    row = pos[1]
    while row >= 0 and same < CONNECT_NUM and check_spot((pos[0], row), symbol, board):
        row -= 1
        same += 1
    row = pos[1] + 1
    while row < len(board[0]) and same < CONNECT_NUM and check_spot((pos[0], row), symbol, board):
        row += 1
        same += 1
    return same >= CONNECT_NUM


def check_col(symbol:str, pos:tuple[int, int], board:list[list[str]]):
    same = 0
    col = pos[0]
    while col >= 0 and same < CONNECT_NUM and check_spot((col, pos[1]), symbol, board):
        col -= 1
        same += 1
    col = pos[0] + 1
    while col < len(board) and same < CONNECT_NUM and check_spot((col, pos[1]), symbol, board):
        col += 1
        same += 1
    return same >= CONNECT_NUM


def check_diag_1(symbol:str, pos:tuple[int, int], board:list[list[str]]):
    same = 0
    col = pos[0]
    row = pos[1]
    while col >= 0 and row >= 0 and same < CONNECT_NUM and check_spot((col, row), symbol, board):
        col -= 1
        row -= 1
        same += 1
    col = pos[0] + 1
    row = pos[1] + 1
    while col < len(board) and row < len(board[0]) and same < CONNECT_NUM and check_spot((col, row), symbol, board):
        col += 1
        row += 1
        same += 1
    return same >= CONNECT_NUM


def check_diag_2(symbol:str, pos:tuple[int, int], board:list[list[str]]):
    same = 0
    col = pos[0]
    row = pos[1]
    while col >= 0 and row < len(board[0]) and same < CONNECT_NUM and check_spot((col, row), symbol, board):
        col -= 1
        row += 1
        same += 1
    col = pos[0] + 1
    row = pos[1] - 1
    while col < len(board) and row >= 0 and same < CONNECT_NUM and check_spot((col, row), symbol, board):
        col += 1
        row -= 1
        same += 1
    return same >= CONNECT_NUM


def check_draw(board:list[list[str]]):
    col = 0
    while col < len(board[0]) and board[0][col] != EMPTY_SYMBOL:
        col += 1
    return col >= len(board[0])


def check_win(newest_symbol_pos:tuple[int, int], board:list[list[str]]):
    symbol = board[newest_symbol_pos[0]][newest_symbol_pos[1]]
    if check_row(
            symbol, newest_symbol_pos, board
        ) or check_col(
            symbol, newest_symbol_pos, board
        ) or check_diag_1(
            symbol, newest_symbol_pos, board
        ) or check_diag_2(
            symbol, newest_symbol_pos, board
        ):
        return Win_types.WIN
    if check_draw(board):
        return Win_types.DRAW
    return Win_types.NO_WIN


def move(board:list[list[str]]):
    valid = False
    newest_symbol_pos = (0, 0)
    while not valid:
        move = get_move(board)
        newest_symbol_pos = make_move(move, board)
        if newest_symbol_pos is not None:
            valid = True
        else:
            print("Invalid move.")
    return check_win(newest_symbol_pos, board) # type: ignore


def display_board(board:list[list[str]]):
    col_const_width = int(math.log(len(board[0]), 10)) + 1
    for row in board:
        for x in range(len(row)):
            print(row[x], end=BOARD_SEP*col_const_width)
        print()
    print()
    for x in range(BOARD_SIZE[0]):
        print(x + 1, end=BOARD_SEP*(col_const_width - int(math.log(x + 1, 10))))
    print()


def display_result(result:Win_types, turns:int):
    if result != Win_types.NO_WIN:
        if result == Win_types.DRAW:
            print(f"Draw", end="")
        else:
            print(get_player_name(get_player_num(turns)), end="")
        print(f" in {turns} turns!")
    else:
        print("The game is still going.")


def main():
    global turn_num
    turn_num = 0
    make_player_types()
    correct_player_names()
    board = make_board()
    result = Win_types.NO_WIN
    display_board(board)
    while result == Win_types.NO_WIN:
        turn_num += 1
        result = move(board)
        display_board(board)
    display_result(result, turn_num)


if __name__ == "__main__":
    main()