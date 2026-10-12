from dataclasses import dataclass
from typing import Literal

@dataclass
class BugFinding:
    bug_type: str
    function: str
    description: str
    severity: Literal["low", "medium", "high", "critical"]
    verification_status: Literal[
        "unverified",
        "reproduced",
        "not_reproduced"
    ] = "unverified"