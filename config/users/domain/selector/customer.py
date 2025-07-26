from ...models import Customer



class CustomerSelector:
    @staticmethod
    def get_or_create(email: str) -> tuple['Customer', bool]:
        customer, created = Customer.objects.get_or_create(email=email)
        return customer, created