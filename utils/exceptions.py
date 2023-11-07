
class NoBookings(Exception):
    def __init__(self, message="This property doesn't have bookings") -> None:
        self.message = message
        super().__init__(self.message)


class NoProperyData(Exception):
    def __init__(self, message="Something is wrong, there is no property information recorded") -> None:
        self.message = message
        super().__init__(self.message)


class NoRequestResponse(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class NonSuccessfulRequest(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)
