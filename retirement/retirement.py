"""Add later!!!

"""

from decimal import Decimal


DEFAULT_INFLATION = Decimal('2.0')


class Retirement(object):
    """Add later!

    """
    def __init__(self):
        self.lump_sums = []


class Account(object):
    """Represents an retirement account.

    Call the constructor with the initial amount of money in the account.
    Then call compute_future_value() to compute how much money the account
    will have in the future with various economic conditions.

    Attributes
    ----------
        name: Name of the fund.
        initial_value: Initial value.
        roth: Roth?  True or False
        future_value: Last computed future value.
        interest: Interest rate, in percent.
        years: Years
        inflation: Inflation rate, in percent.
        final_interest: Final interest rate.  Defaults to None.
    """
    def __init__(self,
                 name="401(k)",
                 initial_value=Decimal('0'),
                 roth=False,
                 interest=Decimal('0'),
                 years=Decimal('0'),
                 inflation=DEFAULT_INFLATION,
                 final_interest=None):
        """Constructor.

        :param name: Name of the fund.
        :param initial_value: Initial value.
        :param roth: Roth?  True or False
        :param interest: Interest rate, in percent.
        :param years: Years
        :param inflation: Inflation rate, in percent.
        :param final_interest: Final interest rate.  Defaults to normal interest rate.
        """
        self.name = name
        self.initial_value = initial_value
        self.roth = roth
        self.future_value = None
        self.interest = interest
        self.years = years
        self.inflation = inflation
        self._final_interest = final_interest

    @property
    def final_interest(self):
        """Return final interest rate.  If not set, return the normal interest rate."""
        return self._final_interest or self.interest

    @final_interest.setter
    def final_interest(self, value):
        self._final_interest = value

    def __str__(self):
        """Returns LumpSum as a human readable string.

        >>> str(Account(name="401(k)", initial_value=Decimal('100000.00'), roth=False))
        'name=401(k), initial_value=100000.00, roth=False'
        """
        return 'name={0}, initial_value={1}, roth={2}'.format(self.name, self.initial_value, self.roth)

    def __repr__(self):
        """Returns LumpSum with more debug info.

        >>> repr(Account(name="401(k)", initial_value=Decimal('100000.00'), roth=False))
        "LumpSum(name=401(k), initial_value=Decimal('100000.00'), roth=False)"
        """
        return '{0}(name={1}, initial_value={2}, roth={3})'.format(self.__class__.__name__,
                                                                   self.name,
                                                                   repr(self.initial_value),
                                                                   self.roth)

    def compute_future_value(self):
        """Computes the future value of the lump sum.

        The future value is represented in todays dollars.
        Inflation is taken into account.

        If a final interest rate is given, the interest rate changes each year, moving from
        the intial interest rate to the final.  This is used to simulate the fact that as
        you get older, you shift your money to less risky investments.

        :return: Future value.
        """
        converted_interest_rate = self._convert_interest_rate(self.interest)
        converted_inflation_rate = self._convert_interest_rate(self.inflation)
        converted_final_rate = self._convert_interest_rate(self.final_interest)
        average_interest = (converted_interest_rate + converted_final_rate) / Decimal('2')
        self.future_value = self.initial_value * (average_interest / converted_inflation_rate) ** self.years
        return self.future_value

    @staticmethod
    def _convert_interest_rate(rate):
        return Decimal('1.0') + rate / Decimal('100')
