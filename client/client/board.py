from pieces import BasePiece


class Board:
    def __init__(self) -> None:
        self.turn = 1
        self.curr_board = {}

        for i in 'abcdefgh':
            for j in '12345678':
                name, color = None, None

                if i in 'ah':
                    name = 'R'

                if i in 'bg':
                    name = 'N'

                if i in 'cf':
                    name = 'B'

                if i == 'd':
                    name = 'Q'

                if i == 'e':
                    name = 'K'

                if j in '27':
                    name = 'p'

                if j in '12':
                    color = 'w'

                if j in '78':
                    color = 'b'

                if name is None or color is None:
                    self.curr_board[(i, j)] = ' '
                else:
                    self.curr_board[(i, j)] = BasePiece(name=name, color=color)

                self.prev_board = self.curr_board.copy()

    def get_possible_moves(self, i: str, j: str) -> list[tuple[str, str]]:
        # TODO(marilius): en passant, рокировка
        ...

    def move(self, i0: str, j0: str, i1: str, j1: str) -> str:
        if (i1, j1) in self.get_possible_moves(i0, j0):
            name0 = self.curr_board[(i0, j0)].piece_name

            if isinstance(self.curr_board[(i1, j1)], BasePiece):
                name1 = self.curr_board[(i1, j1)].piece_name
                sym = 'x'
            else:
                name1 = ''
                sym = '-'

            # TODO(marilius): check, promote
            check = ''
            promote = ''

            # TODO(marilius): Castling 0-0, 0-0-0
            return f'{name0}{i0}{j1}{sym}{name1}{i1}{j1}{check}{promote}'

    def print(self) -> None:
        for j in reversed('12345678'):
            for i in 'abcdefgh':
                print(self.curr_board[(i, j)], end='')
            print()


test = Board()
test.print()
