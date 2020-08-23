class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f"(x: {self.x}, y: {self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Coord):
            return self.x == o.x and self.y == o.y
        return NotImplemented

    def __ne__(self, o: object) -> bool:
        x = self.__eq__(o)
        if x is not NotImplemented:
            return not x
        return NotImplemented
