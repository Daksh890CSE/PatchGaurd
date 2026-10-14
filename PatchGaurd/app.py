from fastapi import FastAPI,HTTPException
from schemas import CodeAnalysisRequest
from ai_analyzer import analyze_code

app=FastAPI(title="PatchGuard API")

@app.get("/health")
def health_check():
    return{"status":"healthy", "project":"Patchguard"}

@app.post("/analyze")
def analyze(request: CodeAnalysisRequest):
    try:
        findings= analyze_code(request.code)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Code analysis failed. Check the AI service and response format."
        ) from exc
    
    return{
        "findings":[
            {
                "bug_type":finding.bug_type,
                "function":finding.function,
                "description":finding.description,
                "severity":finding.severity,
                "verification_status":finding.verification_status,
            }
            for finding in findings
        ]
    }