"""
Tests for LSP (Liskov Substitution Principle) implementation.
Verifies that Circle, Square, and Rectangle can all be used wherever a
Shape is expected without breaking any Shape-contract postconditions.
"""
import math
import pytest

from src.lsp.circle import Circle
from src.lsp.rectangle import Rectangle
from src.lsp.shape import Shape
from src.lsp.square import Square


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def total_area(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)


def resize_all(shapes: list[Shape], factor: float) -> list[Shape]:
    return [s.resize(factor) for s in shapes]


# ---------------------------------------------------------------------------
# Circle
# ---------------------------------------------------------------------------

class TestCircle:
    def test_area(self):
        c = Circle(5)
        assert math.isclose(c.area(), math.pi * 25)

    def test_resize_returns_new_instance(self):
        c = Circle(4)
        resized = c.resize(2)
        assert isinstance(resized, Circle)
        assert resized.radius == 8
        assert c.radius == 4  # original unchanged

    def test_resize_area_postcondition(self):
        c = Circle(3)
        factor = 3
        assert math.isclose(c.resize(factor).area(), c.area() * factor ** 2)

    def test_resize_negative_factor_raises(self):
        with pytest.raises(ValueError):
            Circle(3).resize(-1)

    def test_invalid_radius_raises(self):
        with pytest.raises(ValueError):
            Circle(0)


# ---------------------------------------------------------------------------
# Square
# ---------------------------------------------------------------------------

class TestSquare:
    def test_area(self):
        s = Square(6)
        assert s.area() == 36

    def test_resize_returns_new_instance(self):
        s = Square(4)
        resized = s.resize(2)
        assert isinstance(resized, Square)
        assert resized.side == 8
        assert s.side == 4  # original unchanged

    def test_resize_area_postcondition(self):
        s = Square(5)
        factor = 3
        assert math.isclose(s.resize(factor).area(), s.area() * factor ** 2)

    def test_resize_zero_factor_raises(self):
        with pytest.raises(ValueError):
            Square(5).resize(0)

    def test_invalid_side_raises(self):
        with pytest.raises(ValueError):
            Square(-1)


# ---------------------------------------------------------------------------
# Rectangle
# ---------------------------------------------------------------------------

class TestRectangle:
    def test_area(self):
        r = Rectangle(4, 5)
        assert r.area() == 20

    def test_resize_uniform(self):
        r = Rectangle(3, 4)
        r2 = r.resize(2)
        assert r2.width == 6
        assert r2.height == 8

    def test_resize_area_postcondition(self):
        r = Rectangle(3, 4)
        factor = 2
        assert math.isclose(r.resize(factor).area(), r.area() * factor ** 2)

    def test_resize_axes_non_uniform(self):
        r = Rectangle(4, 6)
        r2 = r.resize_axes(2, 0.5)
        assert r2.width == 8
        assert math.isclose(r2.height, 3.0)

    def test_invalid_dimensions_raise(self):
        with pytest.raises(ValueError):
            Rectangle(0, 5)


# ---------------------------------------------------------------------------
# LSP substitution: all shapes work behind the Shape interface
# ---------------------------------------------------------------------------

class TestLSPSubstitution:
    def setup_method(self):
        self.shapes: list[Shape] = [Circle(1), Square(2), Rectangle(3, 4)]

    def test_total_area_works_with_any_shape(self):
        area = total_area(self.shapes)
        expected = math.pi * 1 + 4 + 12
        assert math.isclose(area, expected)

    def test_resize_all_preserves_area_ratio(self):
        factor = 2
        original_areas = [s.area() for s in self.shapes]
        resized = resize_all(self.shapes, factor)
        for orig, new_shape in zip(original_areas, resized):
            assert math.isclose(new_shape.area(), orig * factor ** 2)

    def test_square_does_not_extend_rectangle(self):
        """Classic LSP fix: Square must NOT be a subtype of Rectangle."""
        assert not issubclass(Square, Rectangle)
