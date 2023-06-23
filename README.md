# Maltsev.Repeater

\
Usage Repeater.Next and returns string:

```python
calls_count: int = 0


def action(multiplier: int) -> str | Repeater.Next:
    global calls_count
    calls_count += 1
    if calls_count == 5:
        return 'Hello World!'
    else:
        print(f'calls_count: {calls_count}, result: {multiplier * calls_count}')
        return Repeater.Next()


repeater = Repeater(action=action)
repeater.configure(attempts=10, delay=0.2)

result = repeater.run(multiplier=2)
if result.is_success:
    print(result.value)

# output:
# -> calls_count: 1, result: 2
# -> calls_count: 2, result: 4
# -> calls_count: 3, result: 6
# -> calls_count: 4, result: 8
# -> Hello World!
```

\
Usage Repeater.Next and Repeater.Fail:

```python
calls_count: int = 0


def action(multiplier: int) -> Repeater.Next | Repeater.Fail:
    global calls_count
    calls_count += 1
    if calls_count == 5:
        return Repeater.Fail(message='failed abc')
    else:
        print(f'calls_count: {calls_count}, result: {multiplier * calls_count}')
        return Repeater.Next()


repeater = Repeater(action=action)
repeater.configure(attempts=10, delay=0.2)

result = repeater.run(multiplier=2)
if result.is_success:  # not success, because action returns Repeater.Fail
    print('is success statement')
    print(result.value)

if result.is_failed:
    print('is failed statement')
    print(result.error_message)

# output:
# -> calls_count: 1, result: 2
# -> calls_count: 2, result: 4
# -> calls_count: 3, result: 6
# -> calls_count: 4, result: 8
# -> is failed statement
# -> failed abc
```

\
Usage Repeater.Next and raise AssertionError:

```python
calls_count: int = 0


def action(multiplier: int) -> Repeater.Next:
    global calls_count
    calls_count += 1
    if calls_count == 5:
        raise AssertionError('assertion error abc')
    else:
        print(f'calls_count: {calls_count}, result: {multiplier * calls_count}')
        return Repeater.Next()


repeater = Repeater(action=action)
repeater.configure(attempts=10, delay=0.2)

try:
    _ = repeater.run(multiplier=2)
except AssertionError as error:
    print(error)

# output:
# -> calls_count: 1, result: 2
# -> calls_count: 2, result: 4
# -> calls_count: 3, result: 6
# -> calls_count: 4, result: 8
# -> assertion error abc
```
