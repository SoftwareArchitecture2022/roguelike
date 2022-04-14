from system import System
from llist import dllist

KEY_W = 0
KEY_A = 1
KEY_S = 2
KEY_D = 3
ACTION_UP = 0
ACTION_LEFT = 1
ACTION_DOWN = 2
ACTION_RIGHT = 3

class IntentionSystem(System):
    def __init__(self, inputState, entityFactory, entityStorage, eventExchanger):
        super(IntentionSystem, self).__init__(entityFactory, entityStorage, eventExchanger)
        self.initMapping()
        self.components = dllist()
        self.inputState = inputState
        # TODO subscribe to events

    def update(self):
        self.reset()
        events = self.eventExchanger.pullEvents()
        for i in range(len(events)):
            pass

        for key in self.inputState.keys:
            self.actions.add(self.mapping[key])

        for node in self.components.iternodes():
            if False: # TODO delete deleted component
                self.components.remove(node)
            node.value.actions = self.actions

    def reset(self):
        self.actions = set()

    def initMapping(self):
        self.mapping = {
                KEY_W: ACTION_UP,
                KEY_A: ACTION_LEFT,
                KEY_S: ACTION_DOWN,
                KEY_D: ACTION_RIGHT,
                }

