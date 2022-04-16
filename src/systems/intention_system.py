from systems.input_state import KEY_Q, KEY_W, KEY_A, KEY_S, KEY_D, KEY_X, KEY_E
from components.intention_component import ACTION_UP, ACTION_LEFT, ACTION_DOWN, ACTION_RIGHT, ACTION_INVENTORY_EQUIP, ACTION_INVENTORY_LEFT, ACTION_INVENTORY_RIGHT
from system import System
from llist import dllist
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class IntentionSystem(System):
    def __init__(self, inputState, entityFactory, entityStorage, eventExchanger):
        super(IntentionSystem, self).__init__(
            entityFactory, entityStorage, eventExchanger)
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
            if False:  # TODO delete deleted component
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
            KEY_X: ACTION_INVENTORY_EQUIP,
            KEY_Q: ACTION_INVENTORY_LEFT,
            KEY_E: ACTION_INVENTORY_RIGHT,
        }
