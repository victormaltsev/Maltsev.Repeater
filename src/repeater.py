from time import sleep
from typing import Any

from src.repeater_result import RepeaterResult


class Repeater:
    __action: Any = None
    __attempts: int = None
    __delay: float = None

    def __init__(self, action: Any):
        self.__action = action

    def configure(self, attempts: int, delay: float) -> 'Repeater':
        self.__attempts = attempts
        self.__delay = delay
        return self

    def run(self, **kwargs: Any) -> 'RepeaterResult':
        count = 1
        while self.__attempts >= count:
            action_result = self.__perform_action(**kwargs)
            match type(action_result):
                case Repeater.Next if self.__attempts == count:
                    break
                case Repeater.Next:
                    count += 1
                    sleep(self.__delay)
                case Repeater.Fail:
                    repeater_result = RepeaterResult(is_success=False, is_failed=True)
                    repeater_result.error_message = action_result.message
                    return repeater_result
                case _:
                    repeater_result = RepeaterResult(is_success=True, is_failed=False)
                    repeater_result.value = action_result
                    return repeater_result

        repeater_result = RepeaterResult(is_success=False, is_failed=True)
        repeater_result.error_message = f'number of attempts exceeded (attempts: {self.__attempts}, delay: {self.__delay})'
        return repeater_result

    def __perform_action(self, **kwargs: Any) -> Any:
        if kwargs:
            return self.__action(**kwargs)
        else:
            return self.__action()

    class Next:
        pass

    class Fail:
        __message: str = None

        def __init__(self, message: str):
            self.__message = message

        @property
        def message(self) -> str:
            return self.__message
