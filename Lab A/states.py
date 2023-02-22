class State:
    def __init__(self, transitions=None, final=False):
        self.transitions = transitions or []
        self.final = final
