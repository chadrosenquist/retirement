import unittest
from decimal import Decimal

from retirement import Retirement
from retirement import Account
from retirement import AccountCommon


class RetirementTestCase(unittest.TestCase):
    def test_simple_lump_sum(self):
        """Tests a simple lump sum, compounded annually."""
        retire = Retirement()
        retire.lump_sums.append(Account(name="401(k)", initial_value=100000.00, roth=False))
        # TO DO: Add tests!


class AccountTestCase(unittest.TestCase):
    def setUp(self):
        self.common = AccountCommon(inflation=Decimal('2.0'))
        self.account = Account(name="401(k)",
                               initial_value=Decimal('100000.00'),
                               roth=False,
                               years=Decimal('10'),
                               common = self.common)

    def test_str(self):
        """Tests __str__"""
        self.assertEqual('name=401(k), initial_value=100000.00, roth=False', str(self.account))

    def test_repr(self):
        """Tests __repr__"""
        self.assertEqual("Account(name=401(k), initial_value=Decimal('100000.00'), roth=False)",
                         repr(self.account))

    def test_simple(self):
        """Tests a simple lump sum, compounded annually.  No inflation."""
        self.common.inflation = Decimal('0.0')
        self.account.interest = Decimal('5.0')
        future_value = self.account.compute_future_value()
        self.assertEqual(Decimal('162889.462677744140625'), future_value)

    def test_with_inflation(self):
        """Tests a simple lump sum, compounded annually.  Inflation."""
        self.account.interest = Decimal('5.0')
        future_value = self.account.compute_future_value()
        self.assertEqual(Decimal('133626.0937752649637487276288'), future_value)

    def test_with_final_interest_rate(self):
        """Tests with a final interest rate.

        For example, the interest rate starts off high because you have more money in
        stocks.  As you approach retirement, the interest gets lower because of more
        money in bonds.
        """
        self.account.interest = Decimal('8.0')
        self.account.final_interest = Decimal('5.0')
        future_value = self.account.compute_future_value()
        self.assertEqual(Decimal('153990.6528265677899626287748'), future_value)


class AccountTaxTestCase(unittest.TestCase):
    """Tests related to pre and post tax."""
    def setUp(self):
        self.common = AccountCommon(inflation=Decimal('2.0'),
                                    federal_tax_rate=Decimal('20.0'),
                                    state_tax_rate=Decimal('5.0'))
        self.account1 = Account(roth=False,
                                initial_value=Decimal('100000'),
                                years=10,
                                interest=Decimal('5.0'),
                                common=self.common)
        self.account2 = Account(roth=True,
                                initial_value=Decimal('100000'),
                                years=10,
                                interest=Decimal('5.0'),
                                common=self.common)

    def test_convert_value_to_aftertax(self):
        self.assertEqual(Decimal('7500'),
                         Account.convert_value_to_aftertax(Decimal('10000'), self.common))

    def test_convert_value_to_pretax(self):
        # TO DO
        pass

    def test_convert_to_aftertax(self):
        self.account1.compute_future_value()
        self.account2.compute_future_value()
        # TO DO

    def test_convert_to_pretax(self):
        self.account1.compute_future_value()
        self.account2.compute_future_value()
        # TO DO

if __name__ == '__main__':
    unittest.main()
