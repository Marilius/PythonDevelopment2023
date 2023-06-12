"""
Chess piece realisation.
"""


class BasePiece:
    """class represents chess pieces
    """
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.moved = False

    @property
    def piece_name(self) -> str:
        return self.name if self.name != 'p' else ''

    def move(self) -> None:
        self.moved = True

    def __str__(self) -> str:
        return self.name


class NotPieceException(Exception):
    """field is empty

    :param Exception: _description_
    :type Exception: _type_
    """
    ...
