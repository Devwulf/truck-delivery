class Event:
    def __init__(self):
        self.listeners = []

    def addListener(self, listener):
        self.listeners.append(listener)
        return self

    def removeListener(self, listener):
        self.listeners.remove(listener)
        return self

    def fire(self, sender, eargs=None):
        for listener in self.listeners:
            listener(sender, eargs)

    def __len__(self):
        return len(self.listeners)

    __iadd__ = addListener
    __isub__ = removeListener
    __call__ = fire