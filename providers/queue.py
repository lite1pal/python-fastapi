from abc import ABC, abstractmethod


class QueueProvider(ABC):
    @abstractmethod
    def enqueue_customer_notes_summary(
        self,
        *,
        customer_id: int,
    ) -> None:
        raise NotImplementedError


class FakeQueueProvider(QueueProvider):
    def enqueue_customer_notes_summary(
        self,
        *,
        customer_id: int,
    ) -> None:
        print(
            "[fake-queue] enqueued customer notes summary "
            f"for customer_id={customer_id}"
        )
