from collections import UserList
from typing import IO, List, Optional, TypeVar

from helpers import open_file


_T = TypeVar("_T")


class CellGroup(UserList):
    """
    Bingo board's row or column.
    """
    def mark(self, drawn_number: int) -> Optional[int]:
        """
        Marks drawn number (if such exists).

        :param drawn_number: number that was drawn
        :return: index of marked number or `None`
        """
        if drawn_number not in self:
            return

        drawn_number_index = self.index(drawn_number)
        self[drawn_number_index] = None
        return drawn_number_index

    def is_complete(self) -> bool:
        """
        Is this row/column complete?

        :return: if all cells are marked
        """
        return all(el is None for el in self)


class Board:
    """
    Bingo board.
    """
    def __init__(self, rows: List[List]):
        self.rows = [CellGroup(row) for row in rows]

    @property
    def unmarked_sum(self) -> int:
        """
        Gets unmarked sum.

        :return: sum of all unmarked cells.
        """
        return sum(sum(el for el in l if el is not None) for l in self.rows)

    def mark(self, drawn_number: int) -> bool:
        """
        Marks drawn number (if such exists).

        :param drawn_number: number that was drawn
        :return: if drawn number completed the board
        """
        for row in self.rows:
            col_idx = row.mark(drawn_number)
            if col_idx is None:
                continue

            column = CellGroup([r[col_idx] for r in self.rows])
            return row.is_complete() or column.is_complete()
        return False


class Player:
    """
    Bingo player.
    """
    score: Optional[int] = None
    rank: Optional[int] = None

    def __init__(self, board):
        self.board = Board(board)

    def play(self, drawn_number: int) -> Optional[bool]:
        """
        Plays drawn number.

        :param drawn_number: number that was drawn
        :return: if player has won, `None` if didn't play
        """
        if self.score:
            # no point in playing if already won
            return

        has_won = self.board.mark(drawn_number)
        if has_won:
            # BINGO! Let's calculate score.
            self.score = self.board.unmarked_sum * drawn_number
        return has_won


class Bingo:
    """
    Game of Bingo.
    """
    def __init__(self, boards):
        self.players = [Player(b) for b in boards]

    @property
    def winners(self) -> List[Player]:
        """
        Gets winners.
        :return: winners
        """
        return [p for p in self.players if p.rank is not None]

    @property
    def last_winner(self) -> Optional[Player]:
        """
        Gets last winner.
        :return: last winner if exists
        """
        try:
            return sorted(self.winners, key=lambda p: -1 * p.rank)[0]
        except IndexError:
            pass

    @property
    def next_rank(self) -> int:
        """
        Gets next winner's rank.
        :return: next rank
        """
        try:
            return self.last_winner.rank + 1
        except AttributeError:
            return 0

    def play(self, drawn_number) -> None:
        """
        Plays drawn number.

        :param drawn_number: Number that was drawn
        """
        for player in self.players:
            has_won = player.play(drawn_number)
            if has_won:
                player.rank = self.next_rank


class BingoRunner:
    """
    Bingo runner.
    """
    def __init__(self, drawn_numbers, boards):
        self.drawn_numbers = drawn_numbers
        self.bingo = Bingo(boards)

    @classmethod
    def from_file(cls: _T, file: IO) -> _T:
        """
        Creates `BingoRunner` from file.
        :param file: file with data for a game of Bingo
        :return: Bingo runner for file
        """
        drawn_numbers = [int(el) for el in file.readline().split(',')]
        file.readline()

        boards, board = [], []
        for line in file.readlines():
            if line.isspace():
                boards.append(board)
                board = []
            else:
                board.append([int(el) for el in line.split()])
        boards.append(board)

        return cls(drawn_numbers, boards)

    def __call__(self, only_one_win=True) -> int:
        """
        Runs Bingo game.

        :param only_first_winner: if game should stop after first win
        :return: score of last winner
        """
        for drawn_number in self.drawn_numbers:
            self.bingo.play(drawn_number)
            if only_one_win and self.bingo.winners:
                break
        return self.bingo.last_winner.score


assert BingoRunner.from_file(open_file("example.txt"))() == 4512
assert BingoRunner.from_file(open_file("input.txt"))() == 35711
assert BingoRunner.from_file(open_file("example.txt"))(False) == 1924
assert BingoRunner.from_file(open_file("input.txt"))(False) == 5586
