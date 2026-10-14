from Sample_code import withdraw

def test_negative_withdrawal_does_not_increase_balance():
    result=withdraw(100,-20)
    assert result==100

def test_valid_withdrawal_reduces_balances():
    result=withdraw(100,30)
    assert result==70

def test_withdrawal_exceeding_balance_does_not_change_balance():
    result=withdraw(100,150)
    assert result==100