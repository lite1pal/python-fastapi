from abc import ABC, abstractmethod


class EmailProvider(ABC):
    @abstractmethod
    def send_customer_created(
        self,
        *,
        to_email: str,
        customer_name: str,
        company: str | None,
    ) -> None: ...


class FakeEmailProvider(EmailProvider):
    def send_customer_created(
        self,
        *,
        to_email: str,
        customer_name: str,
        company: str | None,
    ) -> None:
        print(
            f"[fake-email] sent welcome email to {to_email} "
            f"for {customer_name} ({company})"
        )
