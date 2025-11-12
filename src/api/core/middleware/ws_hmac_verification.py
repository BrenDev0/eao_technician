import os
import hmac
import hashlib
import time


async def verify_hmac_ws(signature: str, payload: str) -> bool:
    """
    Verify HMAC signature for WebSocket connections.
    """
    secret = os.getenv("HMAC_SECRET")
    if not secret or not signature or not payload:
        return False
    try:
        timestamp = int(payload)
    except ValueError:
        return False
    current_time = int(time.time() * 1000)
    allowed_drift = 60_000
    if abs(current_time - timestamp) > allowed_drift:
        return False
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)