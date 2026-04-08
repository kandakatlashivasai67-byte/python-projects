class DepositError(Exception):
    pass

class WithdrawError(Exception):
    pass

class InSuffFundError(Exception):
    pass

class InvalidPinError(Exception):
    pass

class CustomerNotFoundError(Exception):
    pass