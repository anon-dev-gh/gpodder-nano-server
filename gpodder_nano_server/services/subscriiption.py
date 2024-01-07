from gpodder_nano_server.domain.device import Device


class SubscriptionUploader:
    def upload_subscription(self) -> None:
        pass

class SubscriptionUpdater:
    def update_subscription(self) -> None:
        pass

class SubscriptionChangesFetcher:
    def fetch_subscription_change(self, device: Device) -> None:
        pass

