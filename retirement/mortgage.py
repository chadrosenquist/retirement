class Mortgage(object):
    """Class for simple mortgage payment calculations."""
    def __init__(self,
                 loan_amount,
                 interest,
                 payment,
                 extra=0):
        """Create a mortgage object.

        :param loan_amount: The loan amount, or the amount of money currently left to pay off.
        :param interest: The years interest on the loan, in percentage.
        :param payment: The monthly payment.
        :param extra: The amount of extra payment each month, applied directly to principal.
        """

        self.loan_amount = loan_amount
        self.interest = interest
        self.payment = payment
        self.extra = extra

    def calculate_months_left(self):
        """Calculates the number of months left to pay off a loan.

        :return: Number of months left to pay off the loan.
        :raises ValueError: If the interest payment exceeds the monthly payment.
        """


        monthly_interest = self.interest / 12.0
        months = 0
        principal = self.loan_amount

        while principal > 0.0:
            interest_payment = monthly_interest / 100.0 * principal
            principal_payment = self.payment - interest_payment
            if principal_payment <= 0.0:
                raise ValueError("Error: The interest payment, %s, exceeds the monthly payment, %s" %
                                 (interest_payment, self.payment))
            principal -= principal_payment
            principal -= self.extra
            months += 1

        return months
