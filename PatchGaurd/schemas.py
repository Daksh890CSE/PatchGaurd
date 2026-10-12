from pydantic import BaseModel, Field

class CodeAnalysisRequest(BaseModel):
    code:str=Field(
        min_length=1,
        description="Python source code to analyze"
    )