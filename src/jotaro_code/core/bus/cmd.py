
from pydantic import BaseModel, Field




class PongResult(BaseModel):
    server_version: str
    uptime_ms: int
    received_at: str  # ISO 8601