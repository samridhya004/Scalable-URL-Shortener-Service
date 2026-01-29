from pydantic import BaseModel
from typing import Optional

class URLRequest(BaseModel):
    long_url: str
    expiry_minutes: Optional[int] = 60


class URLResponse(BaseModel):
    short_code: str
    short_url: str


class URLStats(BaseModel):
    original_url: str
    short_code: str
    clicks: int
    created_at: str
    expires_at: str
