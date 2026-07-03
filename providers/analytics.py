from abc import ABC, abstractmethod


  class AnalyticsProvider(ABC):
      @abstractmethod
      def track_customer_created(
          self,
          *,
          customer_id: int,
          email: str,
          status: str,
      ) -> None:
          raise NotImplementedError

      @abstractmethod
      def track_customer_archived(
          self,
          *,
          customer_id: int,
      ) -> None:
          raise NotImplementedError

      @abstractmethod
      def track_customer_notes_summary_requested(
          self,
          *,
          customer_id: int,
      ) -> None:
          raise NotImplementedError


  class FakeAnalyticsProvider(AnalyticsProvider):
      def track_customer_created(
          self,
          *,
          customer_id: int,
          email: str,
          status: str,
      ) -> None:
          print(
              "[fake-analytics] customer_created "
              f"customer_id={customer_id} email={email} status={status}"
          )

      def track_customer_archived(
          self,
          *,
          customer_id: int,
      ) -> None:
          print(
              "[fake-analytics] customer_archived "
              f"customer_id={customer_id}"
          )

      def track_customer_notes_summary_requested(
          self,
          *,
          customer_id: int,
      ) -> None:
          print(
              "[fake-analytics] customer_notes_summary_requested "
              f"customer_id={customer_id}"
          )