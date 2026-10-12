from fastapi import FastAPI
from schemas import CodeAnalysisRequest

app=FastAPI(title="PatchGuard API")

@app.get("/health")
def health_check():
    return{"status":"healthy", "project":"Patchguard"}

@app.post("/analyze")
def analyze(request: CodeAnalysisRequest):
    return{
        "message" : "code recieved successfully",
        "code_length" : len(request.code)
    }