import unittest
from unittest.util import safe_repr
from decimal import Decimal


class AssertEqualDec(unittest.TestCase):
    """Provides functions to easily compare Decimal numbers.

    Have your test cases inherit from AssertEqualDec instead of unittest.TestCase"""
    def assertEqualDec(self, first, second, msg=None):
        """Compares two Decimals with a precision of two."""
        first_quantized = first.quantize(Decimal('.01'))
        second_quantized = second.quantize(Decimal('.01'))
        if not first_quantized == second_quantized:
            msg = self._formatMessage(msg, '%s != %s' % (safe_repr(first_quantized),
                                                         safe_repr(second_quantized)))
            raise self.failureException(msg)
