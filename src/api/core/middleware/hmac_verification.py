import os
import hmac
import hashlib
import time
from fastapi import Request, HTTPException, status

async def verify_hmac(request: Request) -> bool:
    """
    Verify HMAC signature for incoming requests
    Use with Depends() on specific routes that need HMAC verification
    """
    secret = os.getenv("HMAC_SECRET")
    if not secret:
        raise ValueError("Missing HMAC_SECRET environment variable")
    
    signature = request.headers.get('x-signature')
    payload = request.headers.get('x-payload')
    
    if not signature or not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HMAC verification failed"
        )
    
    # Validate timestamp
    try:
        timestamp = int(payload)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HMAC verification failed"
        )
    
    current_time = int(time.time() * 1000)  # Current time in milliseconds
    allowed_drift = 60_000  # 60 seconds
    
    if abs(current_time - timestamp) > allowed_drift:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HMAC verification failed"
        )
    
    # Generate expected signature
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures using constant-time comparison
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HMAC verification failed"
        )
    
    return True