"""Add later!!!

"""

from decimal import Decimal


DEFAULT_INFLATION = Decimal('2.0')
DEFAULT_FEDERAL_TAX_RATE = Decimal('25.0')
DEFAULT_STATE_TAX_RATE = Decimal('3.75')


class Retirement(object):
    """Add later!

    """
    def __init__(self):
        self.lump_sums = []


class AccountCommon(object):
    """Represents factors common to all retirement accounts in a portfolio.

    Attributes
    ----------
        inflation: Inflation rate, in percent.
        federal_tax_rate: Federal tax rate.
        state_tax_rate: State tax rate.
    """
    def __init__(self,
                 inflation=DEFAULT_INFLATION,
                 federal_tax_rate=DEFAULT_FEDERAL_TAX_RATE,
                 state_tax_rate=DEFAULT_STATE_TAX_RATE):
        """Constructor

        :param inflation: Interest rate.  Defaults to  DEFAULT_INFLATION.
        :param federal_tax_rate: Federal tax rate.  Defaults to DEFAULT_FEDERAL_TAX_RATE.
        :param state_tax_rate: State tax rate.  Defaults to DEFAULT_STATE_TAX_RATE.
        """
        self.inflation = inflation
        self.federal_tax_rate = federal_tax_rate
        self.state_tax_rate = state_tax_rate


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
        final_interest: Final interest rate.  Defaults to None.
    """
    def __init__(self,
                 name="401(k)",
                 initial_value=Decimal('0'),
                 roth=False,
                 interest=Decimal('0'),
                 years=Decimal('0'),
                 final_interest=None,
                 common=None):
        """Constructor.

        :param name: Name of the fund.
        :param initial_value: Initial value.
        :param roth: Roth?  True or False
        :param interest: Interest rate, in percent.
        :param years: Years
        :param final_interest: Final interest rate.  Defaults to normal interest rate.
        :param common: AccountCommon object.  Values common to all accounts.
        """
        self.name = name
        self.initial_value = initial_value
        self.roth = roth
        self.future_value = None
        self.interest = interest
        self.years = years
        self.common = common or AccountCommon()
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
        converted_inflation_rate = self._convert_interest_rate(self.common.inflation)
        converted_final_rate = self._convert_interest_rate(self.final_interest)
        average_interest = (converted_interest_rate + converted_final_rate) / Decimal('2')
        self.future_value = self.initial_value * (average_interest / converted_inflation_rate) ** self.years
        return self.future_value

    @staticmethod
    def _convert_interest_rate(rate):
        return Decimal('1.0') + rate / Decimal('100')

    @staticmethod
    def convert_value_to_aftertax(value, common):
        """Apply estimated taxes to the value.

        :param value: The value of the account.
        :param common: AccountCommon object.  Holds the federal and state taxes.
        :return: The value after taxes are taken out.
        """
        federal_taxes = value * common.federal_tax_rate / Decimal('100')
        state_taxes = value * common.state_tax_rate / Decimal('100')
        return value - federal_taxes - state_taxes

    @staticmethod
    def convert_value_to_pretax(value, common):
        pass