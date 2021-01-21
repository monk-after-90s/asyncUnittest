# asyncUnittest

asyncUnittest is created for fully asynchronous unit test,which is inspired by unittest. I hear that the newest unittest
has supported asynchronous test already. Well, maybe that is a better choice.

---

### [Install](#Install) · [Usage](#Usage) ·

---

## Install

[asyncUnittest in **PyPI**](https://pypi.org/project/asyncUnittest/)

```shell
pip install asyncUnittest
```

## Usage

#### simple example

```python
from asyncUnittest import AsyncTestCase


class Test(AsyncTestCase):
    enable_test = True

    @classmethod
    async def setUpClass(cls) -> None:
        print('setUpClass')

    async def setUp(self) -> None:
        print('setUp')

    async def test1(self):
        print('test1')

    async def test2(self):
        print('test2')
        self.assertTrue(0)

    def test3(self):
        print('test3')

    async def tearDown(self) -> None:
        print('tearDown')

    @classmethod
    async def tearDownClass(cls) -> None:
        print('tearDownClass')
```

#### AsyncTestCase

If you are familiar with unittest, this is intuitive. Implement your test case class by inheriting 'AsyncTestCase'
imported from asyncUnittest.

#### enable_test

The property 'enable_test' is True as default. You do not need to explicitly define it. If you want to close the
inheriting test case, assign False to it.

#### setUpClass

The test case runs with the first step of calling and awaiting 'setUpClass', before anything else happens. It could be
omitted.

#### setUp

All test methods run concurrently. Before each test method runs, its belonging 'setUp' would be called and awaited.It
could be omitted.

#### test method

A test method may be a normal function or coroutine function.

Any method is a test method as long as string 'test' is in their name's lower case copy, starting or ending with no '
\_'. For example, test_connect and cancel_test are OK, but \_test_connect, \_test_connect_, \_cancel_test_ and
cancel_test_
will be ignored. You can close some test method by adding '_'.

#### assertTrue

"assertTrue" is an assertion method, which asserts all its arguments true. You can find more assertion methods in your
editor hint. More will be implemented in the future.

#### tearDown

After each test method completes, its belonging 'tearDown' would be called and awaited.It could be omitted.

#### tearDownClass

After everything else completes in the test case, the last step is to call and await 'tearDownClass'.It could be
omitted.

#### run

```python
from asyncUnittest import run
```

When "run" is called, any test case in the same global scope would run. So you can run one test case:

```python
class Test(AsyncTestCase):
    ...


run()
```

Or you can import multiple test cases to the target scope and run them concurrently. For example:

```python
from Gear_test import TestGear
from method_run_when_test import TestInstance_run_when
from run_when_test import TestRunWhen
from asyncUnittest import run

run()
```

#### result

The test result would be print in python console:

```shell
setUpClass
setUp
tearDown
setUp
setUp
setUp
test3
tearDown
test1
test2
tearDown
tearDown
tearDownClass
2021-01-21 15:35:00.339 | WARNING  | asyncUnittest.async_unittest:test_one_method:99 - Test method enable_test is complete.Left:['<class '__main__.Test'>.test1', '<class '__main__.Test'>.test2', '<class '__main__.Test'>.test3']

2021-01-21 15:35:00.341 | WARNING  | asyncUnittest.async_unittest:test_one_method:99 - Test method test3 is complete.Left:['<class '__main__.Test'>.test1', '<class '__main__.Test'>.test2']

2021-01-21 15:35:00.341 | WARNING  | asyncUnittest.async_unittest:test_one_method:99 - Test method test1 is complete.Left:['<class '__main__.Test'>.test2']

2021-01-21 15:35:00.342 | WARNING  | asyncUnittest.async_unittest:test_one_method:99 - Test method test2 is complete.Left:[]

2021-01-21 15:35:00.342 | ERROR    | asyncUnittest.async_unittest:run:126 - Traceback (most recent call last):
  File "/Users/90houlaoheshang/Desktop/asyncUnittest/asyncUnittest/async_unittest.py", line 90, in test_one_method
    await asyncio.create_task(test_function())
  File "/Users/90houlaoheshang/Desktop/asyncUnittest/test.py", line 19, in test2
    self.assertTrue(0)
  File "/Users/90houlaoheshang/Desktop/asyncUnittest/asyncUnittest/async_unittest.py", line 30, in assertTrue
    self.assertEqual(True, *args)
  File "/Users/90houlaoheshang/Desktop/asyncUnittest/asyncUnittest/async_unittest.py", line 26, in assertEqual
    raise AssertionError(
AssertionError: 
(True, 0)

items do not equal each other.

2021-01-21 15:35:00.342 | ERROR    | asyncUnittest.async_unittest:run:127 - Spent seconds: 0.008960776000000004, error count:1
```

"Test method * is complete.Left:[...]" shows which test method is completed and which are still running.

"Traceback" shows error tracebacks.

"Spent seconds...error count..." shows spent time and error count.