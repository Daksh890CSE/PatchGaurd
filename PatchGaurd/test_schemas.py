import pytest
from pydantic import ValidationError

from schemas import CodeAnalysisRequest

def test_valid_code_request_is_accepted():
    request = CodeAnalysisRequest(code="print('Hello PatchGuard')")

    assert request.code == "print('Hello PatchGuard')"

def test_empty_code_request_is_rejected():
    with pytest.raises(ValidationError):
        CodeAnalysisRequest(code="")