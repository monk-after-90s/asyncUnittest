from loguru import logger
import traceback
import asyncio
import beeprint


class AsyncTestCase:
    enable_test = True

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

    def assertEqual(self, *args):
        if any([args[0] != arg for arg in args]):
            raise AssertionError(
                f"\n{beeprint.pp(args, output=False, sort_keys=False, string_break_enable=False)}\nitems do not equal each other.")

    def assertTrue(self, *args):
        self.assertEqual(True, *args)

    def assertGreaterThan(self, a, b):
        try:
            self.assertTrue(a > b)
        except AssertionError:
            raise AssertionError(
                f"\n\n{beeprint.pp(a, output=False, sort_keys=False, string_break_enable=False)}\nis not greater than \n\n{beeprint.pp(b, output=False, sort_keys=False, string_break_enable=False)}.")

    def assertLessThan(self, a, b):
        try:
            self.assertTrue(a < b)
        except AssertionError:
            raise AssertionError(
                f"\n\n{beeprint.pp(a, output=False, sort_keys=False, string_break_enable=False)}\nis not less than \n\n{beeprint.pp(b, output=False, sort_keys=False, string_break_enable=False)}.")

    def assertIs(self, a, b):
        try:
            self.assertTrue(a is b)
        except AssertionError:
            raise AssertionError(
                f"\n\n{beeprint.pp(a, output=False, sort_keys=False, string_break_enable=False)}\nis not \n\n{beeprint.pp(b, output=False, sort_keys=False, string_break_enable=False)}.")

    def assertIsNot(self, a, b):
        try:
            self.assertTrue(a is not b)
        except AssertionError:
            raise AssertionError(
                f"\n\n{beeprint.pp(a, output=False, sort_keys=False, string_break_enable=False)}\nis \n\n{beeprint.pp(b, output=False, sort_keys=False, string_break_enable=False)}.")

    def assertIn(self, item, sequence):
        try:
            self.assertTrue(item in sequence)
        except AssertionError:
            raise AssertionError(
                f"\n\n{beeprint.pp(item, output=False, sort_keys=False, string_break_enable=False)}\nis not in \n\n{beeprint.pp(sequence, output=False, sort_keys=False, string_break_enable=False)}.")


def run():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    start = loop.time()
    error_count = 0
    all_test_method = []
    error_tracebacks = []

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
                nonlocal error_tracebacks
                error_tracebacks.append(traceback.format_exc())
                nonlocal error_count
                error_count += 1
            finally:
                all_test_method.remove(str(AsyncTestCase_subclass) + '.' + attribute)
                logger.warning(
                    f'Test method {attribute} is complete.Left:{beeprint.pp(all_test_method, output=False, sort_keys=False, string_break_enable=False)}')
                try:
                    await async_test_case.tearDown()
                except:
                    pass

        test_one_method_tasks = []
        # find all test
        for attr in dir(AsyncTestCase_subclass):
            if 'test' in attr.lower() and attr.strip('_') == attr:
                test_one_method_tasks.append(asyncio.create_task(test_one_method(attr)))
                all_test_method.append(str(AsyncTestCase_subclass) + '.' + attr)
        # await asyncio.wait(one_test_tasks)
        [await task for task in test_one_method_tasks]

        await AsyncTestCase_subclass.tearDownClass()

    async def main():
        subclass_test_tasks = [asyncio.create_task(subclass_test(sub)) \
                               for sub in AsyncTestCase.__subclasses__() if sub.enable_test]
        [await task for task in subclass_test_tasks]
        loop.stop()

    loop.create_task(main())
    loop.run_forever()
    for error_traceback in error_tracebacks:
        logger.error(error_traceback)
    (logger.warning if not error_count else logger.error)(
        f'Spent seconds: {loop.time() - start}, error count:{error_count}')
    # clear
    to_cancel = asyncio.all_tasks(loop)

    async def clear_tasks():
        for task in to_cancel:
            task.cancel()
        await asyncio.sleep(1)

    loop.run_until_complete(clear_tasks())
    loop.run_until_complete(loop.shutdown_asyncgens())

    loop.close()


if __name__ == '__main__':
    class Test(AsyncTestCase):
        # enable_test = False

        @classmethod
        async def setUpClass(cls) -> None:
            cls.a = await asyncio.sleep(2, 10)
            logger.info('setUpClass')

        async def setUp(self) -> None:
            self.b = await asyncio.sleep(2, 5)
            logger.info('setUp')

        # def test(self):
        #     self.assertEqual(self.b / self.a, 3)
        #
        # async def test2(self):
        #     self.b / await asyncio.sleep(2, 0)
        #
        # async def test3(self):
        #     res = await asyncio.sleep(2, 0)
        #     self.assertEqual(res, self.b)
        #     self.assertEqual(res, self.a)

        # async def test4(self):
        #     res = await asyncio.sleep(2, 1)
        #     self.assertTrue(res != 0)

        # async def test_great_than(self):
        #     res = await asyncio.sleep(2, 1)
        #     self.assertGreaterThan(res, 2)
        # async def test_less_than(self):
        #     res = await asyncio.sleep(2, 1)
        #     self.assertLessThan(res, 1)
        # async def test_is(self):
        #     res = await asyncio.sleep(2, 1)
        #     self.assertIs(res, 1.0)
        # async def test_is_not(self):
        #     res = await asyncio.sleep(2, 1.0)
        #     self.assertIsNot(res, 1.0)

        async def test_is_in(self):
            self.assertIn(4, [1, 2, 3])

        async def tearDown(self) -> None:
            logger.info('tearDown')

        @classmethod
        async def tearDownClass(cls) -> None:
            logger.info('tearDownClass')


    run()
