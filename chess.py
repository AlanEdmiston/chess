EDITOR_URL = "https://lichess.org/editor/"

def expand_fen(fen):
    expanded = ""
    i = 0
    for square in fen:
        i += 1
        if square.isdigit():
            expanded += '1' * int(square)
        else:
            expanded += square
        if len(expanded)  > 70:
            return expanded + fen[i:]
    return expanded

def reduce_fen(fen):
    reduced = ""
    counter = 1
    for square in fen:
        if square == '1':
            counter += 1
        else:
            if counter > 0:
                reduced += str(counter)
            counter = 0
            reduced += square
    # print (reduced)
    return reduced

def get_diagonals(fen, i, j, c, is_king=False):
    pos = i * 9 + j
    moves = []
    blocked = [False, False, False, False]
    r = 7
    if is_king: r = 1
    for k in range (r):
        if not blocked[0]: 
            new_pos = (i + k) * 9 + j + k
            if i + k < 8 and j + k < 8:
                if fen[new_pos].isdigit():
                    moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
                else: 
                    blocked[0] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
            else: blocked[0] = True

        if not blocked[1]:
            new_pos = (i + k) * 9 + j - k
            if i + k < 8 and j - k >= 0:
                if fen[new_pos].isdigit():
                    moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
                else: 
                    blocked[1] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
            else: blocked[1] = True

        if not blocked[2]:
            new_pos = (i - k) * 9 + j + k
            if i + k < 8 and j - k >= 0:
                if fen[new_pos].isdigit():
                    moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
                else: 
                    blocked[2] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
            else: blocked[2] = True

        if not blocked[3]:
            new_pos = (i - k) * 9 + j - k
            if i - k >= 0 and j - k >= 0:
                if fen[new_pos].isdigit():
                    moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
                else: 
                    blocked[3] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
            else: blocked[3] = True

        if blocked[0] and blocked[1] and blocked[2] and blocked[3]:
            break

    return moves


def get_straights(fen, i, j, c, is_king=False):
    moves = []
    blocked = [False, False, False, False]
    pos = i * 9 + j
    r = 7
    if is_king: r = 1
    for k in range (r):
        if not blocked[0]: 
            new_pos = (i + k) * 9 + j
            if i + k < 8:
                if fen[new_pos].isdigit():
                    moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
                else: 
                    blocked[0] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
            else: blocked[0] = True

        if not blocked[1]: 
            new_pos = (i - k) * 9 + j
            if i - k >= 0:
                if fen[new_pos].isdigit():
                    moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
                else: 
                    blocked[1] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
            else: blocked[1] = True

        if not blocked[2]: 
            new_pos = i * 9 + j + k
            if j + k < 8:
                if fen[new_pos].isdigit():
                    moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
                else: 
                    blocked[2] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])
            else: blocked[2] = True

        if not blocked[3]: 
            new_pos = i * 9 + j - k
            if j - k >= 0:
                if fen[new_pos].isdigit():
                    moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
                else: 
                    blocked[3] = True
                    if fen[new_pos].isupper() != c.isupper():
                        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
            else: blocked[3] = True

        if blocked[0] and blocked[1] and blocked[2] and blocked[3]:
            break
    
    return moves

def get_knight_moves(fen, i, j, c):
    moves = []
    pos = i * 9 + j

    new_pos = (i + 2) * 9 + j + 1
    if i + 2 < 8 and j + 1 < 8 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])

    new_pos = (i + 1) * 9 + j + 2
    if i + 1 < 8 and j + 2 < 8 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])

    new_pos = (i + 2) * 9 + j - 1
    if i + 2 < 8 and j - 1 >= 0 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])

    new_pos = (i + 1) * 9 + j - 2
    if i + 1 < 8 and j - 2 >= 0 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:pos] + "1" + fen[pos + 1: new_pos] + c + fen[new_pos + 1:])

    new_pos = (i - 2) * 9 + j + 1
    if i - 2 >= 0 and j + 1 < 8 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])

    new_pos = (i - 1) * 9 + j + 2
    if i - 1 >= 0 and j + 2 < 8 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])

    new_pos = (i - 2) * 9 + j - 1
    if i - 2 >= 0 and j - 1 >= 0 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])

    new_pos = (i - 1) * 9 + j - 2
    if i - 1 >= 0 and j - 2 >= 0 and (fen[new_pos] == '1' or fen[new_pos].isupper() != c.isupper()):
        moves.append(fen[:new_pos] + c + fen[new_pos + 1: pos] + "1" + fen[pos + 1:])
        
    return moves


class Board:
    def __init__(self, fen):
        #pieces, to move, castling, en passant, move, 50 move rule ply count
        self.__fen__ = expand_fen(fen)

    def reset(self):
        self.__fen__ = expand_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def set_fen(self, fen):
        self.__fen__ = expand_fen(fen)
    
    def get_fen(self):
        return reduce_fen(self.__fen__)
    
    def export_to_editor(self):
        return EDITOR_URL + self.__fen__ + "?color=white"
    
    def get_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                c = self.__fen__[i * 9 + j]
                if (c == 'r' and ) or c == 'R':
                    moves += get_straights(self.__fen__, i, j, c)

                elif c == 'n' or c == 'N':
                    moves += get_knight_moves(self.__fen__, i, j, c)

                elif c == 'b' or c == 'B':
                    moves += get_diagonals(self.__fen__, i, j, c)

                elif c == 'q' or c == 'Q':
                    moves += get_diagonals(self.__fen__, i, j, c)
                    moves += get_straights(self.__fen__, i, j, c)

                elif c == 'k' or c == 'K':
                    moves += get_diagonals(self.__fen__, i, j, c, True)
                    moves += get_straights(self.__fen__, i, j, c, True)

                elif c == 'p':
                    pos = i * 9 + j
                    if i + 1 < 8 and self.__fen__[pos + 9] == '1':
                        moves.append(self.__fen__[:pos] + "1" + self.__fen__[pos + 1: pos + 9] + c + self.__fen__[pos + 9 + 1:])
                        if i == 1 and self.__fen__[pos + 18] == '1':
                            moves.append(self.__fen__[:pos] + "1" + self.__fen__[pos + 1: pos + 18] + c + self.__fen__[pos + 18 + 1:])
                    
                    if j + 1 < 8 and self.__fen__[(i + 1) * 9 + j + 1] != '1' and self.__fen__[(i + 1) * 9 + j + 1].isupper():
                        moves.append(self.__fen__[:pos] + "1" + self.__fen__[pos + 1: pos + 10] + c + self.__fen__[pos + 10 + 1:])

                    if j - 1 >= 0 and self.__fen__[(i + 1) * 9 + j - 1] != '1' and self.__fen__[(i + 1) * 9 + j - 1].isupper():
                        moves.append(self.__fen__[:pos] + "1" + self.__fen__[pos + 1: pos + 8] + c + self.__fen__[pos + 8 + 1:])

                elif c == 'P':
                    pos = i * 9 + j
                    if i - 1 < 8 and self.__fen__[pos - 9] == '1':
                        moves.append(self.__fen__[:pos - 9] + c + self.__fen__[pos - 9 + 1: pos] + "1" + self.__fen__[pos + 1:])
                        if i == 6 and self.__fen__[pos - 18] == '1':
                            moves.append(self.__fen__[:pos - 18] + c + self.__fen__[pos - 18 + 1: pos] + "1" + self.__fen__[pos + 1:])
                    
                    if j + 1 < 8 and self.__fen__[(i - 1) * 9 + j + 1] != '1' and self.__fen__[(i - 1) * 9 + j + 1].isupper():
                        moves.append(self.__fen__[:pos - 8] + c + self.__fen__[pos - 8 + 1: pos] + "1" + self.__fen__[pos + 1:])

                    if j - 1 >= 0 and self.__fen__[(i - 1) * 9 + j - 1] != '1' and self.__fen__[(i - 1) * 9 + j - 1].isupper():
                        moves.append(self.__fen__[:pos - 10] + c + self.__fen__[pos - 10 + 1: pos] + "1" + self.__fen__[pos + 1:])

        return moves


def main():
    board = Board("")
    board.reset()
    print(board.get_moves())


if __name__ == "__main__":
    main()