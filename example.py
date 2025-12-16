import random

from simple_result import Ok, Err, UnwrapError, Result, ResultOption


def fetch_data() -> Result[str, ConnectionError]:
    fetched = random.choice([True, False])
    if fetched:
        return Ok('Data fetched!')
    return Err(ConnectionError('Error fetching data!'))


def using_type_narrowing() -> None:
    print('Using type narrowing')
    if res := fetch_data():
        print(res.unwrap_value()) # "Data fetched!"
        assert res.value == 'Data fetched!'
        assert res.error is None
    else:
        print(res.unwrap_error()) # "Error fetching data!"
        assert res.value is None
        assert str(res.error) == 'Error fetching data!'


def using_match() -> None:
    print('Using match')
    match fetch_data():
        case Ok(data):
            print(data) # "Data fetched!"
        case Err(error):
            print(error) # "Error fetching data!"


def using_match_with_code() -> None:
    print('Using match with code')
    match fetch_data():
        case Ok(data):
            print(data) # "Data fetched!"
        case Err(error, code):
            print(error, code) # "Error fetching data! 1"


if __name__ == '__main__':
    using_type_narrowing()
    using_match()
    using_match_with_code()
