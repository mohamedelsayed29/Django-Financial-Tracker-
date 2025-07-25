import secrets
import string

class OTPService:
    @staticmethod
    def generate_otp(length=6):
        digits = string.digits  # OTPs are typically numeric
        otp = ''.join(secrets.choice(digits) for _ in range(length))
        return otp

    @staticmethod
    def validate_otp(otp, user_otp):
        """Validate the provided OTP against the user's stored OTP."""
        return otp == user_otp  