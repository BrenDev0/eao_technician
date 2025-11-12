import hmac
import hashlib
import time
import os

def generate_hmac_headers(secret: str):
        """Generate HMAC headers for authenticated requests"""
        timestamp = int(time.time() * 1000)  
        payload = str(timestamp)
        
        signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            'x-signature': signature,
            'x-payload': payload,
            'Content-Type': 'application/json'
        }