import random

def generate_otp():
    """6 digit ka unique OTP generate karega"""
    return str(random.randint(100000, 999999))