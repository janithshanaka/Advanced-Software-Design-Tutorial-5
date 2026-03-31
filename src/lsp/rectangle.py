"""
LSP - Liskov Substitution Principle
Rectangle: concrete Shape that also supports non-uniform axis scaling.

Rectangle is kept independent from Square to avoid the classic LSP
violation of having Square extend Rectangle.
"""
from src.lsp.shape import NonUniformlyResizable, Shape


class Rectangle(Shape, NonUniformlyResizable):
    """A rectangle with independent width and height."""

    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def area(self) -> float:
        return self._width * self._height

    def resize(self, factor: float) -> "Rectangle":
        if factor <= 0:
            raise ValueError("Resize factor must be positive.")
        return Rectangle(self._width * factor, self._height * factor)

    def resize_axes(self, x_factor: float, y_factor: float) -> "Rectangle":
        if x_factor <= 0 or y_factor <= 0:
            raise ValueError("Scale factors must be positive.")
        return Rectangle(self._width * x_factor, self._height * y_factor)

    def __repr__(self) -> str:
        return f"Rectangle(width={self._width}, height={self._height})"
