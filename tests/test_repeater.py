from time import monotonic
from typing import Any

import pytest

from src.maltsev_repeater.repeater import Repeater


class TestRepeater:
    __calls_count: int = 0

    def test_when_not_configured(self) -> None:
        # setup
        @self.__record_calls_count
        def action() -> Any:
            return None

        repeater = Repeater(action=action)

        # act
        try:
            repeater.run()
            raise AssertionError('runtime error not raised')
        except Exception as exception:
            assert type(exception) == RuntimeError
            assert str(exception) == 'repeater not configured'

        # assert
        assert self.__calls_count == 0

    @pytest.mark.parametrize('action_result', [None, 1, 2.50, True, 'Hello World!'])
    def test_when_success_on_first_attempt(self, action_result: Any) -> None:
        # setup
        @self.__record_calls_count
        def action() -> Any:
            return action_result

        repeater = Repeater(action=action)
        repeater.configure(attempts=10, delay=0.01)

        # act
        result = repeater.run()

        # assert
        assert self.__calls_count == 1

        assert result.is_success is True
        assert result.is_failed is False
        assert result.value == action_result

    @pytest.mark.parametrize('action_result', [None, 1, 2.50, True, 'Hello World!'])
    def test_when_success_on_last_attempt(self, action_result: Any) -> None:
        # setup
        @self.__record_calls_count
        def action() -> Any:
            if self.__calls_count == 10:
                return action_result
            else:
                return Repeater.Next()

        repeater = Repeater(action=action)
        repeater.configure(attempts=10, delay=0.01)

        # act
        result = repeater.run()

        # assert
        assert self.__calls_count == 10

        assert result.is_success is True
        assert result.is_failed is False
        assert result.value == action_result

    def test_when_success_with_arguments(self) -> None:
        # setup
        @self.__record_calls_count
        def action(last_name: str, first_name: str, middle_name: str | None = None) -> Any:
            return f'Hello, {first_name}!'

        repeater = Repeater(action=action)
        repeater.configure(attempts=10, delay=0.01)

        # act
        result = repeater.run(first_name='Ivan', last_name='Ivanov')

        # assert
        assert self.__calls_count == 1

        assert result.is_success is True
        assert result.is_failed is False
        assert result.value == 'Hello, Ivan!'

    def test_when_failed(self) -> None:
        # setup
        @self.__record_calls_count
        def action() -> Any:
            return Repeater.Fail(message='error message abc')

        repeater = Repeater(action=action)
        repeater.configure(attempts=10, delay=0.01)

        # act
        result = repeater.run()

        # assert
        assert self.__calls_count == 1

        assert result.is_success is False
        assert result.is_failed is True
        assert result.error_message == 'error message abc'

    def test_when_failed_because_attempts_exceeded(self) -> None:
        # setup
        start_time = monotonic()

        @self.__record_calls_count
        def action() -> Any:
            return Repeater.Next()

        repeater = Repeater(action=action)
        repeater.configure(attempts=10, delay=0.2)

        # act
        result = repeater.run()

        # assert
        assert self.__calls_count == 10
        assert start_time <= monotonic() - 1.8

        assert result.is_success is False
        assert result.is_failed is True
        assert result.error_message == 'number of attempts exceeded (attempts: 10, delay: 0.2)'

    def test_when_raise_exception(self) -> None:
        # setup
        @self.__record_calls_count
        def action() -> Any:
            raise NotImplementedError('not implemented abc')

        repeater = Repeater(action=action)
        repeater.configure(attempts=10, delay=0.01)

        # act
        try:
            repeater.run()
            raise AssertionError('not implemented error not raised')
        except Exception as exception:
            assert type(exception) == NotImplementedError
            assert str(exception) == 'not implemented abc'

        # assert
        assert self.__calls_count == 1

    def __record_calls_count(self, function):
        def wrapper(*args, **kwargs):
            self.__calls_count += 1
            return function(*args, **kwargs)

        return wrapper
