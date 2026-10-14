import ollama,json
from finding import BugFinding

MODEL_NAME = "llama3.1:8b"

def analyze_code(code:str) -> list[BugFinding]:
    response=ollama.chat(
        model=MODEL_NAME,
        format="json",
        messages=[
            {
                "role":"system",
                "content":(
                    "You are PatchGuard, a Python code review assistant. "
                    "Identify potential bugs, explain why they may occur. "
                    "Return only valid json with this structure: "
                    '{"findings":[{"bug_type":"...",'
                    '"function": "...",'
                    '"description": "...",'
                    '"severity": "low|medium|high|critical",}]}'
                    "The finding value must be a list."
                    "use an empty list if no bugs are likely found."
                    "Do not include markdown code fences or text outside the JSON."
                    "Do not claim a bug has been verified unless a test "
                    "has actually reproduced it. "
                    "treat findings as potential and unverified."
                ),
            },
            {
                "role":"user",
                "content":f"Analyze this python code for potential bugs:\n\n{code}",
            },
        ],
    )

    raw_result= response.message.content
    return parse_findings(response.message.content)

def parse_findings(raw_result:str)-> list[BugFinding]:
    parsed_result=json.loads(raw_result)

    if not isinstance(parsed_result,dict):
        raise ValueError("AI response must be a json object")

    if "findings" not in parsed_result:
        raise ValueError("AI response is missing the 'findings' field")

    if not isinstance(parsed_result["findings"],list):
        raise ValueError("'findings' must be a list")

    required_fields={
        "bug_type",
        "function",
        "description",
        "severity"
    }

    for finding in parsed_result["findings"]:
        if not isinstance(finding,dict):
            raise ValueError("Each finding must be a json object")

        missing_fields=required_fields-finding.keys()

        if missing_fields:
            raise ValueError(f"AI finding is a missing fields:{missing_fields}")

        if not all(
            isinstance(finding[field],str) and finding[field].strip()
            for field in required_fields
        ):
            raise ValueError("All required finding fields must be non empty strings")

        allowed_severities={"low","medium","high","critical"}

        if finding["severity"] not in allowed_severities:
            raise ValueError(f"Invalid severity: {finding['severity']}")  

    findings=[]

    for finding in parsed_result["findings"]:
        bug_finding=BugFinding(
            bug_type=finding["bug_type"],
            function=finding["function"],
            description=finding["description"],
            severity=finding["severity"],
            verification_status="unverified"
        ) 

        findings.append(bug_finding)

    return findings