import time
from collections import defaultdict
from fastapi import Request
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.database.session import SessionLocal
from backend.models.url import URL
from backend.utils.validators import is_valid_url
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import string
import random

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()

RATE_LIMIT = 5          # max requests
RATE_WINDOW = 60        # seconds

rate_limit_store = defaultdict(list)


class URLRequest(BaseModel):
    long_url: str
    expiry_minutes: Optional[int] = 1440  # default = 24 hours
    custom_alias: Optional[str] = None



def generate_short_code(db: Session, length: int = 6):
    characters = string.ascii_letters + string.digits

    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        exists = db.query(URL).filter(URL.short_code == code).first()
        if not exists:
            return code


import re

def is_valid_alias(alias: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9\-]{3,30}$", alias))



@router.post("/shorten")
def shorten_url(
    request: URLRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    client_ip = http_request.client.host
    user_agent = http_request.headers.get("user-agent")
    current_time = time.time()

    # Remove old timestamps
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip]
        if current_time - t < RATE_WINDOW
    ]

    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )

    rate_limit_store[client_ip].append(current_time)

    long_url = request.long_url.strip()

    if len(long_url) > 2048:
        raise HTTPException(
            status_code=400,
            detail="URL too long (max 2048 characters)"
        )
    
    if request.expiry_minutes is not None and request.expiry_minutes > 525600:
        raise HTTPException(
            status_code=400,
            detail="expiry_minutes cannot exceed 1 year"
        )

    if request.expiry_minutes is not None and request.expiry_minutes <= 0:
        raise HTTPException(
            status_code=400,
            detail="expiry_minutes must be a positive number"
        )

    if not is_valid_url(long_url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # EXPIRY CALCULATED ONCE (FIX)
    expires_at = (
        datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
        if request.expiry_minutes is not None
        else None
    )

    existing = db.query(URL).filter(URL.original_url == long_url).first()

    if existing:
        if existing.expires_at and datetime.utcnow() > existing.expires_at:
            db.delete(existing)
            db.commit()
        else:
            if request.expiry_minutes is not None:
                existing.expires_at = expires_at
                db.commit()

            return {
                "short_code": existing.short_code,
                "short_url": f"http://localhost:8000/{existing.short_code}"
            }

    # Handle custom alias
    if request.custom_alias:
        alias = request.custom_alias.strip()

        if not is_valid_alias(alias):
            raise HTTPException(
                status_code=400,
                detail="Alias must be 3–30 characters (letters, numbers, hyphens only)"
            )

        alias_exists = db.query(URL).filter(URL.short_code == alias).first()

        if alias_exists:
            if alias_exists.original_url == long_url:
                return {
                    "short_code": alias_exists.short_code,
                    "short_url": f"http://localhost:8000/{alias_exists.short_code}"
                }
            if alias_exists.expires_at and datetime.utcnow() > alias_exists.expires_at:
                db.delete(alias_exists)
                db.commit()
            else:
                raise HTTPException(
                    status_code=409,
                    detail="Custom alias already in use"
                )

        short_code = alias
    else:
        short_code = generate_short_code(db)

    # USE PRECOMPUTED expiry
    new_url = URL(
        short_code=short_code,
        original_url=long_url,
        expires_at=(
            datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
            if request.expiry_minutes else None
        ),
        clicks=0,
        created_ip=client_ip,
        user_agent=user_agent
    )


    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_code": short_code,
        "short_url": f"http://localhost:8000/{short_code}"
    }



from datetime import datetime

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # EXPIRY CHECK
    if url_entry.expires_at and datetime.utcnow() > url_entry.expires_at:
        db.delete(url_entry)
        db.commit()
        raise HTTPException(
            status_code=410,
            detail="This short URL has expired and is no longer available"
        )


    # CLICK COUNT
    url_entry.clicks += 1
    db.commit()

    return RedirectResponse(
        url=url_entry.original_url,
        status_code=302
    )


@router.get("/stats/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    if url_entry.expires_at and datetime.utcnow() > url_entry.expires_at:
        raise HTTPException(
            status_code=410,
            detail="This short URL has expired and is no longer available"
        )

    return {
        "short_code": url_entry.short_code,
        "original_url": url_entry.original_url,
        "clicks": url_entry.clicks,
        "created_at": url_entry.created_at
    }
