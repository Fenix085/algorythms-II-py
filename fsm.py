#Finite State Machine class

class InitializationError(Exception):
    """Raised when the FSM is not initialized correctly."""
    pass

class FSM:
    def __init__(self) -> None:
        self.handlers = {}
        self.initState = None
        self.finalStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.finalStates.append(name)

    def set_start(self, name):
        self.initState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.initState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.finalStates:
            raise InitializationError("at least one state must be an end_state")
        
        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.finalStates:
                print("reached ", newState)
                break
            else:
                handler = self.handlers[newState.upper()]