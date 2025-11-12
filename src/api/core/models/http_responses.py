from pydantic import BaseModel

class CommonHttpResponse(BaseModel):
    detail: str