"""
JWT VERIFICATION PROCESS - Demo educativo
"""

import json
import base64
import hmac
import hashlib
from datetime import datetime

def verify_jwt_demo(jwt_token, secret_key):
    """Dimostra come Flask-JWT-Extended verifica un JWT"""
    
    print("🔍 VERIFICA JWT - Step by step:")
    print(f"JWT ricevuto: {jwt_token[:50]}...")
    
    try:
        # 1. Dividi il JWT nelle 3 parti
        parts = jwt_token.split('.')
        if len(parts) != 3:
            print("❌ JWT malformato - non ha 3 parti")
            return False
            
        header_b64, payload_b64, signature_b64 = parts
        print("✅ JWT ha 3 parti corrette")
        
        # 2. Decodifica header e payload
        header = json.loads(base64.urlsafe_b64decode(header_b64 + '=='))
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '=='))
        
        print(f"📋 Header: {header}")
        print(f"📦 Payload: {payload}")
        
        # 3. Verifica scadenza
        exp_timestamp = payload.get('exp')
        if exp_timestamp and exp_timestamp < datetime.now().timestamp():
            print("❌ JWT scaduto!")
            return False
        print("✅ JWT non scaduto")
        
        # 4. Ricalcola la firma
        message = f"{header_b64}.{payload_b64}"
        expected_signature = base64.urlsafe_b64encode(
            hmac.new(
                secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
        ).decode().rstrip('=')
        
        # 5. Confronta le firme
        received_signature = signature_b64
        if expected_signature == received_signature:
            print("✅ FIRMA VALIDA - JWT autentico!")
            print(f"👤 User ID estratto: {payload.get('sub')}")
            return payload
        else:
            print("❌ FIRMA NON VALIDA - JWT contraffatto!")
            return False
            
    except Exception as e:
        print(f"💥 Errore verifica JWT: {e}")
        return False

# Esempio di uso
if __name__ == "__main__":
    # Questo è quello che fa Flask-JWT-Extended internamente
    fake_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1IiwidXNlcm5hbWUiOiJtYXJpbyIsImV4cCI6MTY5MTIzNDU2N30.signature"
    secret = "my-secret-key"
    
    result = verify_jwt_demo(fake_jwt, secret)
    
    print("\n🎯 CONCLUSIONE:")
    print("- Server NON salva il JWT")
    print("- Server verifica solo la FIRMA crittografica")
    print("- Se la firma è valida → JWT è autentico")
    print("- Se la firma è invalida → JWT è contraffatto")
