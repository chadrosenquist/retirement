import unittest
from decimal import Decimal
from decimal import localcontext

from tests.assertequaldec import AssertEqualDec
from retirement import Retirement
from retirement import Account
from retirement import AccountCommon


class RetirementTestCase(AssertEqualDec):
    def test_simple_lump_sum(self):
        """Tests a simple lump sum, compounded annually."""
        retire = Retirement()
        retire.lump_sums.append(Account(name="401(k)", initial_value=100000.00, roth=False))
        # TO DO: Add tests!


class AccountTestCase(AssertEqualDec):
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


class AccountTaxTestCase(AssertEqualDec):
    """Tests related to pre and post tax.

    The two test accounts, normal_401k and roth_401k, both have the same
    amount of money.  But because one is a normal 401(k) and the other is a Roth,
    their values before and after taxes are different.
    """
    def setUp(self):
        self.common = AccountCommon(inflation=Decimal('2.0'),
                                    federal_tax_rate=Decimal('20.0'),
                                    state_tax_rate=Decimal('5.0'))
        self.normal_401k = Account(roth=False,
                                   initial_value=Decimal('100000'),
                                   years=10,
                                   interest=Decimal('5.0'),
                                   common=self.common)
        self.roth_401k = Account(roth=True,
                                 initial_value=Decimal('100000'),
                                 years=10,
                                 interest=Decimal('5.0'),
                                 common=self.common)

    def test_convert_value_to_aftertax(self):
        """Test money after federal and state taxes."""
        self.assertEqual(Decimal('7500'),
                         Account.convert_value_to_aftertax(Decimal('10000'), self.common))

    def test_convert_value_to_pretax(self):
        """Test money before federal and state taxes."""
        self.assertEqual(Decimal('13333.33333333333333333333333'),
                         Account.convert_value_to_pretax(Decimal('10000'), self.common))

    def test_convert_to_aftertax(self):
        """Compare after tax."""
        self.normal_401k.compute_future_value()
        self.roth_401k.compute_future_value()
        self.assertEqual(Decimal('100219.5703314487228115457216'), self.normal_401k.future_value_aftertax())
        self.assertEqual(Decimal('133626.0937752649637487276288'), self.roth_401k.future_value_aftertax())

    def test_convert_to_pretax(self):
        """Compare pre tax."""
        self.normal_401k.compute_future_value()
        self.roth_401k.compute_future_value()
        self.assertEqual(Decimal('133626.0937752649637487276288'), self.normal_401k.future_value_pretax())
        self.assertEqual(Decimal('178168.1250336866183316368384'), self.roth_401k.future_value_pretax())
        self.assertEqualDec(Decimal('133626.09'), self.normal_401k.future_value_pretax())
        self.assertEqualDec(Decimal('178168.13'), self.roth_401k.future_value_pretax())

if __name__ == '__main__':
    unittest.main()
