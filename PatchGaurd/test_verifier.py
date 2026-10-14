from verifier import verify_negative_withdrawal
from Sample_code import withdraw

def fixed_withdraw(balance,amount):
    if amount<0:
        return balance
    return balance-amount

def buggy_withdraw(balance,amount):
    return balance-amount

def test_fixed_function_does_not_reproduce_bug():
    finding= verify_negative_withdrawal(fixed_withdraw)

    assert finding.verification_status== "not_reproduced"

def test_buggy_function_reproduces_bug():
    finding= verify_negative_withdrawal(buggy_withdraw)

    assert finding.verification_status== "reproduced"

def test_real_sample_function_does_not_reproduce_bug():
    finding=verify_negative_withdrawal(withdraw)

    assert finding.verification_status=="not_reproduced"