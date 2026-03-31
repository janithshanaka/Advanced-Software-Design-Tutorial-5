"""
LSP - Liskov Substitution Principle
Shape hierarchy redesigned so every subclass can be safely substituted
for its parent without altering program correctness.

Design decisions
----------------
* ``Shape`` is the common base; it exposes ``area()`` and a *uniform*
  ``resize(factor)`` that every shape supports.
* ``NonUniformlyResizable`` is a separate mixin for shapes that support
  independent scaling on each axis.  Clients that only need the basic
  ``Shape`` contract are never exposed to the non-uniform API.
* ``Square`` does NOT inherit from ``Rectangle``.  A square cannot honour
  the rectangle contract (independent width/height mutation), so making it
  a sub-type of Rectangle violates LSP.  Both are independent concrete shapes.

Before refactoring
------------------
``Square`` attempted to override ``resize(factor)`` with a two-argument
version, causing runtime errors when callers passed a single scalar
factor (as expected by the ``Shape`` contract).

After refactoring
-----------------
Every concrete shape's ``resize(factor)`` takes exactly one argument and
returns a *new* shape instance (immutable style) so the base-class contract
is always satisfied.
"""
from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Abstract base for all shapes."""

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""

    @abstractmethod
    def resize(self, factor: float) -> "Shape":
        """
        Return a *new* shape uniformly scaled by *factor*.

        Precondition:  factor > 0
        Postcondition: result.area() == self.area() * factor ** 2
        """


class NonUniformlyResizable(ABC):
    """
    Optional mixin for shapes that support independent axis scaling.

    Kept separate so that clients coding to the ``Shape`` interface are
    never forced to handle non-uniform scaling (ISP / LSP synergy).
    """

    @abstractmethod
    def resize_axes(self, x_factor: float, y_factor: float) -> "Shape":
        """Return a new shape scaled by *x_factor* and *y_factor* independently."""
