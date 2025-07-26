import secrets
import string
from ..selector.customer import CustomerSelector
from ...models import Otp
from django.db import transaction
from django.utils import timezone

class OTPService:
    @staticmethod
    def generate_otp(length: int = 6):
        digits = string.digits  
        otp = ''.join(secrets.choice(digits) for _ in range(length))
        return otp

    @staticmethod
    @transaction.atomic
    def _store_otp_in_db(*, otp: str, user_id: str):
        customer, created = CustomerSelector.get_or_create(email=user_id)
        Otp.objects.filter(
            customer=customer,
            is_expired=False

            ).update(
                is_expired=True , expired_at=timezone.now()
            )
        Otp.objects.create(
            otp=otp,
            customer=customer,
            expired_at=timezone.now() + timezone.timedelta(minutes=5)
        )
        return customer, otp