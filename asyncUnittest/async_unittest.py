from loguru import logger
import traceback
import asyncio
import beeprint


class AsyncTestCase:
    @classmethod
    async def setUpClass(cls) -> None:
        pass

    @classmethod
    async def tearDownClass(cls) -> None:
        pass

    async def setUp(self) -> None:
        pass

    async def tearDown(self) -> None:
        pass

    def assertEqual(self, a, b):
        if a != b:
            raise AssertionError(
                f"\n{beeprint.pp(a, output=False, sort_keys=False, string_break_enable=False)}!=\n{beeprint.pp(b, output=False, sort_keys=False, string_break_enable=False)}")

    def assertTrue(self, a):
        self.assertEqual(True, a)


def run():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    start = loop.time()
    error_count = 0

    async def subclass_test(AsyncTestCase_subclass):
        await AsyncTestCase_subclass.setUpClass()

        async def test_one_method(attribute: str):
            async_test_case = None
            try:
                async_test_case = AsyncTestCase_subclass()
                await async_test_case.setUp()

                test_function = getattr(async_test_case, attribute)
                if callable(test_function):
                    if not asyncio.iscoroutinefunction(test_function):
                        test_function()
                    else:
                        await asyncio.create_task(test_function())

            except:
                logger.error(traceback.format_exc())
                nonlocal error_count
                error_count += 1
            finally:
                try:
                    await async_test_case.tearDown()
                except:
                    pass

        test_one_method_tasks = []
        # find all test
        for attr in dir(AsyncTestCase_subclass):
            if 'test' in attr.lower() and attr.strip('_') == attr:
                test_one_method_tasks.append(asyncio.create_task(test_one_method(attr)))
        # await asyncio.wait(one_test_tasks)
        [await task for task in test_one_method_tasks]

        await AsyncTestCase_subclass.tearDownClass()

    async def main():
        subclass_test_tasks = [asyncio.create_task(subclass_test(sub)) for sub in AsyncTestCase.__subclasses__()]
        [await task for task in subclass_test_tasks]

    loop.run_until_complete(main())
    (logger.warning if not error_count else logger.error)(
        f'Spent seconds: {loop.time() - start}, error count:{error_count}')


if __name__ == '__main__':
    class Test(AsyncTestCase):
        @classmethod
        async def setUpClass(cls) -> None:
            cls.a = await asyncio.sleep(2, 10)
            logger.info('setUpClass')

        async def setUp(self) -> None:
            self.b = await asyncio.sleep(2, 5)
            logger.info('setUp')

        def test(self):
            self.assertEqual(self.b / self.a, 3)

        async def test2(self):
            self.b / await asyncio.sleep(2, 0)

        async def test3(self):
            res = await asyncio.sleep(2, 0)
            self.assertEqual(res, self.b)
            self.assertEqual(res, self.a)

        async def test4(self):
            res = await asyncio.sleep(2, 0)
            self.assertTrue(res != 0)

        async def tearDown(self) -> None:
            logger.info('tearDown')

        @classmethod
        async def tearDownClass(cls) -> None:
            logger.info('tearDownClass')


    run()
