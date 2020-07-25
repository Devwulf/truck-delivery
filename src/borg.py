class Borg:
    """
    Used as a base class for singletons.
    """
    _shared_state = {}
    def __init__(self):
        """
        Space: O(1) Time: O(1)
        """
        self.__dict__ = self._shared_state
