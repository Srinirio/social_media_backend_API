import random
import secrets

def generate_otp() -> int:
    """
    Here we generation the OTP
    """
    otp = random.randint(1000,9999)
    print(otp)
    
    return otp

def generateSecretKey() -> str:
    generated_key = secrets.token_hex(16)
    return generated_key

