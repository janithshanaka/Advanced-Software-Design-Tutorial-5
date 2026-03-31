"""
LSP - Liskov Substitution Principle
Circle: concrete Shape that satisfies the full Shape contract.

Circles support only *uniform* scaling via ``resize(factor)``.
Non-uniform axis scaling would produce an ellipse, which is a different
shape entirely, so Circle does NOT implement NonUniformlyResizable – this
keeps the interface honest and avoids surprising callers.
"""
import math

from src.lsp.shape import Shape


class Circle(Shape):
    """A circle with a given radius."""

    def __init__(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("Radius must be positive.")
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    def area(self) -> float:
        return math.pi * self._radius ** 2

    def resize(self, factor: float) -> "Circle":
        if factor <= 0:
            raise ValueError("Resize factor must be positive.")
        return Circle(self._radius * factor)

    def __repr__(self) -> str:
        return f"Circle(radius={self._radius})"
