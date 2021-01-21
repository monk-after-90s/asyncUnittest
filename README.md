# asyncUnittest

asyncUnittest is created for fully asynchronous unit test inspired by unittest. I hear that the newest unittest has
support asynchronous test already. Well, maybe that is a better choice.

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

The test case runs with the first step of calling and await 'setUpClass', before anything else happens.

#### setUp

All test methods run concurrently. Before each test method runs, its belonging 'setUp' would be called and awaited.

#### test method

A test method may be a normal function or coroutine function.

Define test methods with 'test' in their name's lower case copy, starting or ending with no '_'. For example,
test_connect and cancel_test are OK, but _test_connect and cancel_test_ will be ignored. You can close some test method
by adding '_'.

#### tearDown

After each test method completes, its belonging 'tearDown' would be called and awaited.

#### tearDownClass

After everything else completes in the test case, the last step is to call and await 'tearDownClass'.
