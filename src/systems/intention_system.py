from src.systems.input_state import KEY_Q, KEY_W, KEY_A, KEY_S, KEY_D, KEY_X, \
    KEY_E
from src.components.intention_component import ACTION_UP, ACTION_LEFT, \
    ACTION_DOWN, ACTION_RIGHT, ACTION_INVENTORY_EQUIP, ACTION_INVENTORY_LEFT, \
    ACTION_INVENTORY_RIGHT
from src.systems.system import System
from llist import dllist
from src.events.event_exchanger import EventType, EventAction


class IntentionSystem(System):
    def __init__(self, input_state, entity_factory, entity_storage,
                 event_exchanger):
        super(IntentionSystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.init_mapping()
        self.components = dllist()
        self.input_state = input_state
        self.event_exchanger.subscribe(self,
                                       EventType.INTENTION_COMPONENT_CHANGE)

    def update(self):
        self.reset()
        events = self.event_exchanger.pull_events(self)
        deleted_components = set()
        for event in events:
            if event.event_action == EventAction.ADD_COMPONENT:
                self.components.insert(event.component)
            elif event.event_action == EventAction.DELETE_COMPONENT:
                deleted_components.add(event.component)

        for key in self.input_state.keys:
            self.actions.add(self.mapping[key])

        for node in self.components.iternodes():
            if node.value in deleted_components:
                self.components.remove(node)
                continue
            node.value.actions = self.actions

    def reset(self):
        self.actions = set()

    def init_mapping(self):
        self.mapping = {
            KEY_W: ACTION_UP,
            KEY_A: ACTION_LEFT,
            KEY_S: ACTION_DOWN,
            KEY_D: ACTION_RIGHT,
            KEY_X: ACTION_INVENTORY_EQUIP,
            KEY_Q: ACTION_INVENTORY_LEFT,
            KEY_E: ACTION_INVENTORY_RIGHT,
        }
