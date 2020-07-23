class Event:
    def __init__(self):
        self.listeners = []

    def addListener(self, listener):
        """
        Subscribes a listener to this event.

        :param listener: The listener that will subscribe to this event.
        :return: self
        """
        self.listeners.append(listener)
        return self

    def removeListener(self, listener):
        """
        Unsubscribes a listener from this event.

        :param listener: The listener to unsubscribe from this event.
        :return: self
        """
        self.listeners.remove(listener)
        return self

    def fire(self, sender, eargs=None):
        """
        Handles the listeners subscribed to this event, passing the
        object that fired the event and any other event arguments
        passed.

        :param sender: The object that fired this event.
        :param eargs: Optional - The arguments to be passed to the listeners when fired.
        :return: N/A
        """
        for listener in self.listeners:
            listener(sender, eargs)

    def __len__(self):
        """
        :return: The amount of listeners subscribed to this event.
        """
        return len(self.listeners)

    __iadd__ = addListener
    __isub__ = removeListener
    __call__ = fire