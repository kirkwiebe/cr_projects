
class Hudlie:
    """A typical Hudlie and his/her attributes."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
