# simple-result

<p align="center">
    <a href="https://pypi.org/project/simple-result" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/simple-result" alt="Supported Python versions">
    </a>
    <a href="https://pypi.org/project/simple-result" target="_blank">
        <img src="https://img.shields.io/pypi/v/simple-result" alt="Package version">
    </a>
    <a href="https://github.com/daireto/simple-result/actions" target="_blank">
        <img src="https://github.com/daireto/simple-result/actions/workflows/publish.yml/badge.svg" alt="Publish">
    </a>
    <a href="/LICENSE" target="_blank">
        <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
    </a>
</p>

A very simple, fully typed Rust-like Result type for Python 3.

If you need a Result type only for checking if an operation succeeded or failed,
and don't need to perform special actions like chaining operations, mapping, etc.,
then this library is for you.

If you are looking for a more feature-rich Result type, check out
[rustedpy/result](https://github.com/rustedpy/result).

## Installation

```bash
# Using pip
pip install simple-result

# Using Poetry
poetry add simple-result

# Using uv
uv add simple-result
```

## Usage

```python
import random

from simple_result import Err, Ok, Result

def fetch_data() -> Result[str, ConnectionError]:
    fetched = random.choice([True, False])
    if fetched:
        return Ok('Data fetched!')
    return Err(ConnectionError('Error fetching data!'))
```

Check if the result is Ok or Err using type narrowing:

```python
if res := fetch_data():
    print(res.value) # "Data fetched!"
    print(res.error) # None
else:
    print(res.error) # "Error fetching data!"
    print(res.value) # None
```

Or using `match`:

```python
match fetch_data():
    case Ok(data):
        print(data) # "Data fetched!"
    case Err(error):
        print(error) # "Error fetching data!"

match fetch_data():
    case Ok(data):
        print(data) # "Data fetched!"
    case Err(error, code):
        print(error, code) # "Error fetching data! 1"
```

Call `.unwrap_value()` to get the value or raise an `UnwrapError` if the result
is `Err`:

```python
from simple_result import UnwrapError

try:
    res = Err(ConnectionError('Error fetching data!'))
    print(res.unwrap_value())
except UnwrapError as exc:
    print(str(exc)) # called `Result.unwrap_value()` on an `Err` value
    print(exc.result.error) # "Error fetching data!"
```

Call `.unwrap_error()` to get the error or raise an `UnwrapError` if the result
is `Ok`:

```python
try:
    res = Ok('Data fetched!')
    print(res.unwrap_error())
except UnwrapError as exc:
    print(str(exc)) # called `Result.unwrap_error()` on an `Ok` value
    print(exc.result.value) # "Data fetched!"
```

Compare results:

```python
assert Ok(1) == Ok(1)
assert Ok(1) != Ok(2)

exc = ValueError('error')
assert Err(exc) == Err(exc)

other_exc = ValueError('other error')
assert Err(exc) != Err(other_exc)
```

Check if the result is `Ok` or `Err` using `isinstance`:

```python
from simple_result import ResultOption

res = fetch_data()
assert isinstance(res, ResultOption)
assert isinstance(res, (Ok, Err))
```

## Contributing

See the [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.

## Support

If you find this project useful, give it a ⭐ on GitHub!
