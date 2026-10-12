from finding import BugFinding

def test_bug_finding_default_to_unverified():
    finding= BugFinding(
        bug_type="invalid input handling",
        function="withdraw",
        description="negative amounts increases the balance.",
        severity="high"
    )

    assert finding.function == "withdraw"
    assert finding.severity == "high"
    assert finding.verification_status == "unverified"