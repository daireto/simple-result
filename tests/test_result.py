import pytest

from simple_result import Ok, Err, UnwrapError, Result, ResultOption

class TestOk:
    def test_repr_returns_ok_with_value_inside_parentheses(self):
        assert repr(Ok(1)) == 'Ok(1)'

    def test_eq_returns_true_when_comparing_with_same_value(self):
        assert Ok(1) == Ok(1)

    def test_eq_returns_false_when_comparing_with_different_value(self):
        assert Ok(1) != Ok(2)

    def test_ne_returns_false_when_comparing_with_same_value(self):
        assert not (Ok(1) != Ok(1))

    def test_ne_returns_true_when_comparing_with_different_value(self):
        assert Ok(1) != Ok(2)

    def test_hash_returns_same_value_when_called_multiple_times(self):
        assert hash(Ok(1)) == hash(Ok(1))

    def test_hash_returns_different_value_when_comparing_with_different_value(self):
        assert hash(Ok(1)) != hash(Ok(2))

    def test_bool_returns_true(self):
        assert bool(Ok(1))

    def test_value_property_returns_value(self):
        assert Ok(1).value == 1

    def test_error_property_returns_none(self):
        assert Ok(1).error is None

    def test_code_property_returns_zero(self):
        assert Ok(1).code == 0

    def test_unwrap_value_returns_value(self):
        assert Ok(1).unwrap_value() == 1

    def test_unwrap_error_raises_unwrap_error(self):
        with pytest.raises(UnwrapError):
            Ok(1).unwrap_error()


class TestErr:
    def test_repr_returns_err_with_value_inside_parentheses(self):
        exc = ValueError('error message')
        assert repr(Err(ValueError('error message'))) == f'Err({exc!r})'

    def test_eq_returns_true_when_comparing_with_same_value(self):
        exc = ValueError('error message')
        assert Err(exc) == Err(exc)

    def test_eq_returns_false_when_comparing_with_different_value(self):
        assert Err(ValueError('error message')) != Err(ValueError('other error message'))

    def test_ne_returns_false_when_comparing_with_same_value(self):
        exc = ValueError('error message')
        assert not (Err(exc) != Err(exc))

    def test_ne_returns_true_when_comparing_with_different_value(self):
        assert Err(ValueError('error message')) != Err(ValueError('other error message'))

    def test_hash_returns_same_value_when_called_multiple_times(self):
        exc = ValueError('error message')
        assert hash(Err(exc)) == hash(Err(exc))

    def test_hash_returns_different_value_when_comparing_with_different_value(self):
        assert hash(Err(ValueError('error message'))) != hash(
            Err(ValueError('other error message'))
        )

    def test_bool_returns_false(self):
        assert not bool(Err(ValueError('error message')))

    def test_value_property_returns_none(self):
        assert Err(ValueError('error message')).value is None

    def test_error_property_returns_error(self):
        exc = ValueError('error message')
        assert Err(exc).error is exc

    def test_code_property_returns_one_by_default(self):
        assert Err(ValueError('error message')).code == 1

    def test_code_property_returns_custom_code(self):
        assert Err(ValueError('error message'), code=2).code == 2

    def test_unwrap_value_raises_unwrap_error(self):
        with pytest.raises(UnwrapError):
            Err(ValueError('error message')).unwrap_value()

    def test_unwrap_error_returns_error(self):
        exc = ValueError('error message')
        assert Err(exc).unwrap_error() is exc


class TestUnwrapError:
    def test_result_property_returns_original_result(self):
        res = Ok(1)
        exc = UnwrapError(res, 'error message')
        assert exc.result is res


class TestResultOption:
    def test_result_option_isinstance_checks_ok_or_err(self):
        assert isinstance(Ok(1), ResultOption)
        assert isinstance(Err(ValueError('error message')), ResultOption)
