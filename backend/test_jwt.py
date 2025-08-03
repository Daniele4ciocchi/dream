#!/usr/bin/env python3
"""
Test JWT per debug
"""
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'test-secret-key'
jwt = JWTManager(app)

with app.app_context():
    print("🔍 Test JWT...")
    
    # Test 1: Crea token con stringa
    try:
        user_id = "123"
        token = create_access_token(identity=user_id)
        print(f"✅ Token creato con identity='{user_id}': {token[:50]}...")
        
        # Decodifica il token per vedere cosa contiene
        decoded = decode_token(token)
        print(f"🔍 Token decodificato: {decoded}")
        
    except Exception as e:
        print(f"❌ Errore creazione token con stringa: {e}")
    
    # Test 2: Crea token con intero
    try:
        user_id = 123
        token = create_access_token(identity=user_id)
        print(f"✅ Token creato con identity={user_id}: {token[:50]}...")
        
        # Decodifica il token per vedere cosa contiene
        decoded = decode_token(token)
        print(f"🔍 Token decodificato: {decoded}")
        
    except Exception as e:
        print(f"❌ Errore creazione token con intero: {e}")
    
    # Test 3: Crea token con additional claims
    try:
        user_id = "123"
        additional_claims = {"username": "test", "email": "test@test.com"}
        token = create_access_token(
            identity=user_id, 
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=1)
        )
        print(f"✅ Token creato con claims: {token[:50]}...")
        
        # Decodifica il token per vedere cosa contiene
        decoded = decode_token(token)
        print(f"🔍 Token con claims decodificato: {decoded}")
        
    except Exception as e:
        print(f"❌ Errore creazione token con claims: {e}")
