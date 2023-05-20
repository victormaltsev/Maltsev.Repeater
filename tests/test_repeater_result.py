import pytest

from src.repeater_result import RepeaterResult


class TestRepeaterResult:
    @pytest.mark.parametrize('is_success, is_failed', [(True, True), (True, False), (False, True), (False, False)])
    def test_setup_constructor(self, is_success: bool, is_failed: bool) -> None:
        # setup
        # nothing

        # act
        result = RepeaterResult(is_success=is_success, is_failed=is_failed)

        # assert
        assert result.is_success == is_success
        assert result.is_failed == is_failed

        try:
            _ = result.value
            raise AssertionError('value error not raised (property "value")')
        except Exception as exception:
            assert type(exception) == ValueError
            assert str(exception) == 'property "value" not set'

        try:
            _ = result.error_message
            raise AssertionError('value error not raised (property "error_message")')
        except Exception as exception:
            assert type(exception) == ValueError
            assert str(exception) == 'property "error_message" not set'

    def test_first_setup_value(self) -> None:
        # setup
        result = RepeaterResult(is_success=True, is_failed=False)

        # act
        result.value = 'value abc'
        result.error_message = 'error_message abc'

        # assert
        assert result.value == 'value abc'
        assert result.error_message == 'error_message abc'

    def test_second_setup_value(self) -> None:
        # setup
        result = RepeaterResult(is_success=True, is_failed=False)
        result.value = 'value abc'
        result.error_message = 'error_message abc'

        # act
        try:
            result.value = 'value (second)'
            raise AssertionError('value error not raised (property "value")')
        except Exception as exception:
            assert type(exception) == ValueError
            assert str(exception) == 'property "value" already set'

        try:
            result.error_message = 'error_message (second)'
            raise AssertionError('value error not raised (property "error_message")')
        except Exception as exception:
            assert type(exception) == ValueError
            assert str(exception) == 'property "error_message" already set'

        # assert
        assert result.value == 'value abc'
        assert result.error_message == 'error_message abc'
