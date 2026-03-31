"""
LSP - Liskov Substitution Principle
Square: concrete Shape that satisfies the full Shape contract.

Key LSP fix: Square does NOT extend Rectangle.
A Rectangle contract allows width and height to vary independently, which a
Square cannot honour (it would violate the invariant width == height).
Making Square a standalone Shape ensures safe substitution everywhere a
Shape is expected.
"""
from src.lsp.shape import Shape


class Square(Shape):
    """A square with equal sides."""

    def __init__(self, side: float) -> None:
        if side <= 0:
            raise ValueError("Side length must be positive.")
        self._side = side

    @property
    def side(self) -> float:
        return self._side

    def area(self) -> float:
        return self._side ** 2

    def resize(self, factor: float) -> "Square":
        if factor <= 0:
            raise ValueError("Resize factor must be positive.")
        return Square(self._side * factor)

    def __repr__(self) -> str:
        return f"Square(side={self._side})"
