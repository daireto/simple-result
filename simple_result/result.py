from abc import ABC, abstractmethod
from typing import Any, Final, Generic, Literal, TypeAlias, TypeVar

T_co = TypeVar('T_co', covariant=True)
E_co = TypeVar('E_co', bound=Exception, covariant=True)


class _Option(ABC):
    @property
    @abstractmethod
    def value(self):  # noqa: ANN202
        """Return the value if Ok, None if Err."""
        ...

    @property
    @abstractmethod
    def error(self):  # noqa: ANN202
        """Return the error if Err, None if Ok."""
        ...

    @abstractmethod
    def unwrap_value(self):  # noqa: ANN202
        """Return the value if Ok, raise an UnwrapError if Err."""
        ...

    @abstractmethod
    def unwrap_error(self):  # noqa: ANN202
        """Return the error if Err, raise an UnwrapError if Ok."""
        ...


class Ok(_Option, Generic[T_co]):
    """A value that indicates success."""

    __match_args__ = ('value',)
    __slots__ = ('_value',)

    def __init__(self, value: T_co) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f'Ok({self._value!r})'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ok) and self._value == other._value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))

    def __bool__(self) -> Literal[True]:
        return True

    @property
    def value(self) -> T_co:
        """Return the value."""
        return self._value

    @property
    def error(self) -> None:
        return None

    @property
    def code(self) -> int:
        return 0

    def unwrap_value(self) -> T_co:
        """Return the value."""
        return self._value

    def unwrap_error(self) -> None:
        """Raise an UnwrapError since this type is Ok."""
        raise UnwrapError(
            self,
            f'called `Result.unwrap_error()` on an `Ok` value: {self._value!r}',
        )


class Err(_Option, Generic[E_co]):
    """A value that signifies failure."""

    __match_args__ = ('error', 'code')
    __slots__ = ('_code', '_value')

    def __init__(self, error: E_co, code: int = 1) -> None:
        self._value = error
        self._code = code

    def __repr__(self) -> str:
        return f'Err({self._value!r})'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Err) and self._value == other._value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self._value))

    def __bool__(self) -> Literal[False]:
        return False

    @property
    def value(self) -> None:
        return None

    @property
    def error(self) -> E_co:
        """Return the error."""
        return self._value

    @property
    def code(self) -> int:
        """Return the error code."""
        return self._code

    def unwrap_value(self) -> None:
        """Raise an UnwrapError since this type is Err."""
        raise UnwrapError(
            self,
            f'called `Result.unwrap_value()` on an `Err` value: {self._value!r}',
        ) from self._value

    def unwrap_error(self) -> E_co:
        """Return the error."""
        return self._value


Result: TypeAlias = Ok[T_co] | Err[E_co]

ResultOption: Final = (Ok, Err)
"""A type to use in ``isinstance`` checks.

E.g. ``isinstance(res, ResultOption)``.
Same as using ``isinstance(res, (Ok, Err))``.
"""


class UnwrapError(Exception):
    """Exception raised from ``.unwrap_<...>`` calls.

    The original ``Result`` can be accessed via the ``.result`` attribute,
    but this is not intended for regular use, as type information is lost:
    This class doesn't know about both ``T_co`` and ``E_co``, since it's
    raised from ``Ok()`` or ``Err()`` which only knows about either
    ``T_co`` or ``E``, not both.
    """

    _result: Result[object, Exception]

    def __init__(self, result: Result[object, Exception], message: str) -> None:
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any, Any]:
        """Returns the original result."""
        return self._result
