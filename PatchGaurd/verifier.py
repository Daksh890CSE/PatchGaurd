from finding import BugFinding
from _collections_abc import Callable


def verify_negative_withdrawal(withdraw_function:Callable[[int,int],int],) -> BugFinding:
    balance=100
    amount=-20

    actual_balance=withdraw_function(balance,amount)
    expected_balance=balance

    if actual_balance !=expected_balance:
        status="reproduced"
    else:
        status="not_reproduced"

    return BugFinding(
        bug_type="invalid input handling",
        function="withdraw",
        description="A negative withdrawal amount increases the balance.",
        severity="high",
        verification_status=status,
    )