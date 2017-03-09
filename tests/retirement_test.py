import unittest
from decimal import Decimal

from retirement import Retirement
from retirement import LumpSum


class RetirementTestCase(unittest.TestCase):
    def test_simple_lump_sum(self):
        """Tests a simple lump sum, compounded annually."""
        retire = Retirement()
        retire.lump_sums.append(LumpSum(name="401(k)", initial_value=100000.00, roth=False))
        # TO DO: Add tests!


class LumpSumTestCase(unittest.TestCase):
    def setUp(self):
        self.lumpsum = LumpSum(name="401(k)", initial_value=Decimal('100000.00'), roth=False)

    def test_str(self):
        """Tests __str__"""
        self.assertEqual('name=401(k), initial_value=100000.00, roth=False', str(self.lumpsum))

    def test_repr(self):
        """Tests __repr__"""
        self.assertEqual("LumpSum(name=401(k), initial_value=Decimal('100000.00'), roth=False)",
                         repr(self.lumpsum))

    def test_simple(self):
        """Tests a simple lump sum, compounded annually.  No inflation."""
        future_value = self.lumpsum.compute_future_value(interest=Decimal('5.0'),
                                                         years=Decimal('10'),
                                                         inflation=Decimal('0.0'))
        self.assertEqual(Decimal('162889.462677744140625'), future_value)

    def test_with_inflation(self):
        """Tests a simple lump sum, compounded annually.  Inflation."""
        future_value = self.lumpsum.compute_future_value(interest=Decimal('5.0'),
                                                         years=Decimal('10'),
                                                         inflation=Decimal('2.0'))
        self.assertEqual(Decimal('133626.0937752649637487276288'), future_value)

    def test_with_final_interest_rate(self):
        """Tests with a final interest rate.

        For example, the interest rate starts off high because you have more money in
        stocks.  As you approach retirement, the interest gets lower because of more
        money in bonds.
        """
        future_value = self.lumpsum.compute_future_value(interest=Decimal('8.0'),
                                                         years=Decimal('10'),
                                                         inflation=Decimal('2.0'),
                                                         final_interest=Decimal('5.0'))
        self.assertEqual(Decimal('153990.6528265677899626287748'), future_value)

    def test_convert_to_pretax(self):
        # TO DO!
        pass

    def test_convert_to_posttax(self):
        # TO DO!
        pass

if __name__ == '__main__':
    unittest.main()
