from typing import Any


class RepeaterResult:
    __is_success: bool = None
    __is_failed: bool = None

    __value: Any = None
    __value_is_set: bool = False

    __error_message: str = None
    __error_message_is_set: bool = False

    def __init__(self, is_success: bool, is_failed: bool):
        self.__is_success = is_success
        self.__is_failed = is_failed

    @property
    def is_success(self) -> bool:
        return self.__is_success

    @property
    def is_failed(self) -> bool:
        return self.__is_failed

    @property
    def value(self) -> Any:
        if self.__value_is_set:
            return self.__value
        else:
            raise ValueError('property "value" not set')

    @value.setter
    def value(self, value: Any) -> None:
        if self.__value_is_set:
            raise ValueError('property "value" already set')
        else:
            self.__value = value
            self.__value_is_set = True

    @property
    def error_message(self) -> str:
        if self.__error_message_is_set:
            return self.__error_message
        else:
            raise ValueError('property "error_message" not set')

    @error_message.setter
    def error_message(self, error_message: str) -> None:
        if self.__error_message_is_set:
            raise ValueError('property "error_message" already set')
        else:
            self.__error_message = error_message
            self.__error_message_is_set = True
