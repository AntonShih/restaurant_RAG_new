# core/auth/password.py

def verify_password(expected: str, actual: str) -> bool:
    return expected == actual