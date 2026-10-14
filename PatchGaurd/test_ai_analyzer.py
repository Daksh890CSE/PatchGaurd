import json,pytest
from ai_analyzer import analyze_code,parse_findings
from finding import BugFinding

def test_analyze_code_returns_a_response():
    code="""
def withdraw(balance, amount):
    return balance - amount
"""

    result=analyze_code(code)

    assert isinstance(result,list)
    assert all(isinstance(item,BugFinding)for item in result)

def test_analyzer_identifies_negative_withdrawal_bug():
    code="""
def withdraw(balance, amount):
    if amount <= balance:
        return balance - amount
    return balance
    """

    result=analyze_code(code)
    assert isinstance(result,list)

    for finding in result:
        assert isinstance(finding,BugFinding)
        assert finding.verification_status=="unverified"

def test_parse_findings_returns_unverified_finding():
    raw_result ="""
    {
        "findings":[
            {
                "bug_type": "missing_input_validation",
                "function": "withdraw",
                "description": "Negative amounts are not rejected.",
                "severity": "medium"
            }
        ]
    }
    """

    findings=parse_findings(raw_result)

    assert len(findings)==1
    assert isinstance(findings[0],BugFinding)
    assert findings[0].function =="withdraw"
    assert findings[0].severity =="medium"
    assert findings[0].verification_status == "unverified"

def test_parse_findings_rejects_invalid_severity():
    raw_result ="""
        {
            "findings":[
                {
                    "bug_type": "missing_input_validation",
                    "function": "withdraw",
                    "description": "Negative amounts are not rejected.",
                    "severity": "urgent"
                }
            ]
        }
        """

    with pytest.raises(ValueError,match="Invalid severity"):
        parse_findings(raw_result)

def test_parse_findings_rejects_missing_fields():
    raw_result ="""
        {
            "findings":[
                {
                    "bug_type": "missing_input_validation",
                    "function": "withdraw",
                    "severity": "urgent"
                }
            ]
        }
        """
    
    with pytest.raises(ValueError,match="missing fields"):
        parse_findings(raw_result)

def test_parse_findings_rejects_malformed_json():
    raw_result='{"findings":['

    with pytest.raises(json.JSONDecodeError):
        parse_findings(raw_result)