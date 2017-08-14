import unittest

from retirement import Mortgage


class MortgageTest(unittest.TestCase):
    def test_thirty_year(self):
        """The owner has a 30 year loan and is about 5 years into the loan.

        The owner wants to know about how much longer it'll take to pay off the loan.
        """
        mortgage = Mortgage(loan_amount=200000.00,
                            interest=4.00,
                            payment=1200.00)

        months_left = mortgage.calculate_months_left()
        self.assertEqual(months_left, 244)

    def test_thirty_year_w_extra(self):
        """The owner has a 30 year loan and is about 5 years into the loan.

        The owner wants to know about how much longer it'll take to pay off the loan
        if the owner pays extra each month.
        """
        mortgage = Mortgage(loan_amount=200000.00,
                            interest=4.00,
                            payment=1200.00,
                            extra=300.00)

        months_left = mortgage.calculate_months_left()
        self.assertEqual(months_left, 177)

    def test_interest_exceeds_payment(self):
        """The monthly interest on the loan exceeds the monthly payment."""
        mortgage = Mortgage(loan_amount=200000,
                            interest=10.00,
                            payment=1000)
        with self.assertRaises(ValueError):
            mortgage.calculate_months_left()

if __name__ == '__main__':
    unittest.main()
