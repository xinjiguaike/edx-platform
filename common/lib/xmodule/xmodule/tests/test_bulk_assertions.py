import ddt
from xmodule.tests import BulkAssertionTest

@ddt.ddt
class TestBulkAssertionTestCase(BulkAssertionTest):

    @ddt.data(
        ('assertTrue', True),
        ('assertFalse', False),
        ('assertIs', 1, 1),
        ('assertIsNot', 1, 2),
        ('assertIsNone', None),
        ('assertIsNotNone', 1),
        ('assertIn', 1, (1, 2, 3)),
        ('assertNotIn', 5, (1, 2, 3)),
        ('assertIsInstance', 1, int),
        ('assertNotIsInstance', '1', int),
        ('assertRaises', KeyError, {}.__getitem__, '1'),
    )
    @ddt.unpack
    def test_passing_asserts_passthrough(self, assertion, *args):
        getattr(self, assertion)(*args)


    @ddt.data(
        ('assertTrue', False),
        ('assertFalse', True),
        ('assertIs', 1, 2),
        ('assertIsNot', 1, 1),
        ('assertIsNone', 1),
        ('assertIsNotNone', None),
        ('assertIn', 5, (1, 2, 3)),
        ('assertNotIn', 1, (1, 2, 3)),
        ('assertIsInstance', '1', int),
        ('assertNotIsInstance', 1, int),
        ('assertRaises', ValueError, lambda: None),
    )
    @ddt.unpack
    def test_failing_asserts_passthrough(self, assertion, *args):
        # Use super(BulkAssertionTest) to make sure we get un-adulturated assertions
        with super(BulkAssertionTest, self).assertRaises(AssertionError):
            getattr(self, assertion)(*args)

    def test_no_bulk_assert_equals(self):
        # Use super(BulkAssertionTest) to make sure we get un-adulturated assertions
        with super(BulkAssertionTest, self).assertRaises(AssertionError):
            self.assertEquals(1, 2)

    @ddt.data(
        ('assertEqual', 1, 2),
        ('assertEquals', 1, 2),
        ('assertItemsEqual', (1, 1, 2), (2, 2, 1)),
    )
    @ddt.unpack
    def test_bulk_assert_equals(self, asserterFn, *args):
        asserter = getattr(self, asserterFn)
        contextmanager = self.bulk_assertions()

        contextmanager.__enter__()
        asserter(*args)

        # Use super(BulkAssertionTest) to make sure we get un-adulturated assertions
        with super(BulkAssertionTest, self).assertRaises(AssertionError):
            contextmanager.__exit__(None, None, None)

    @ddt.data(
        ('assertEqual', (1, 1), (1, 2)),
        ('assertEquals', (1, 1), (1, 2)),
        ('assertItemsEqual', ((1, 1, 2), (2, 1, 1)), ((1, 1, 2), (2, 2, 1))),
    )
    @ddt.unpack
    def test_bulk_assert_closed(self, asserterFn, pass_args, fail_args):
        asserter = getattr(self, asserterFn)

        with self.bulk_assertions():
            asserter(*pass_args)
            asserter(*pass_args)

        # Use super(BulkAssertionTest) to make sure we get un-adulturated assertions
        with super(BulkAssertionTest, self).assertRaises(AssertionError):
            asserter(*fail_args)
