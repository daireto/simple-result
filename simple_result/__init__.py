"""A simple Rust-like Result type for Python."""

from .result import Err, Ok, Result, ResultOption, UnwrapError

__all__ = [
    'Err',
    'Ok',
    'Result',
    'ResultOption',
    'UnwrapError',
]

__version__ = '0.2.0'
