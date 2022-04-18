import unittest
import unittest.mock
from src.systems.intention_system import IntentionSystem
from src.components.intention_component import IntentionComponent
from src.entity_env.entity_factory import EntityFactory
from src.events.event_exchanger import EventExchanger
from src.entity_env.entity_storage import EntityStorage
from src.systems.input_state import KEY_Q, KEY_W, KEY_A, KEY_S, KEY_D, KEY_X, KEY_E
from src.events.event_exchanger import EventType, EventAction, ComponentChangeEvent
from src.components.intention_component import ACTION_UP, ACTION_LEFT, ACTION_DOWN, ACTION_RIGHT, ACTION_INVENTORY_EQUIP, ACTION_INVENTORY_LEFT, ACTION_INVENTORY_RIGHT


class TestIntentionSystem(unittest.TestCase):
    def setUp(self):
        self.event_exchanger = EventExchanger()
        self.entity_storage = EntityStorage(self.event_exchanger)
        self.entity_factory = EntityFactory(self.entity_storage)
        self.event_exchanger.subscribe = unittest.mock.MagicMock()
        self.event_exchanger.pull_events = unittest.mock.MagicMock()

    def test_intention_system(self):
        class InputState:
            keys = {KEY_Q, KEY_W, KEY_A, KEY_S, KEY_D, KEY_X, KEY_E}

        intention_system = IntentionSystem(InputState(), self.entity_factory, self.entity_storage, self.event_exchanger)
        self.event_exchanger.subscribe.assert_called_once_with(intention_system, EventType.INTENTION_COMPONENT_CHANGE)

        component1 = IntentionComponent(0)
        component2 = IntentionComponent(1)
        answer = {ACTION_UP, ACTION_LEFT, ACTION_DOWN, ACTION_RIGHT, ACTION_INVENTORY_EQUIP, ACTION_INVENTORY_LEFT, ACTION_INVENTORY_RIGHT}
        self.event_exchanger.pull_events.return_value = [ComponentChangeEvent(EventType.INTENTION_COMPONENT_CHANGE, 0, EventAction.ADD_COMPONENT, component1), ComponentChangeEvent(EventType.INTENTION_COMPONENT_CHANGE, 0, EventAction.ADD_COMPONENT, component2)]
        intention_system.update()
        self.assertEqual(component1.actions, answer)
        self.assertEqual(component2.actions, answer)
        self.event_exchanger.pull_events.return_value = [ComponentChangeEvent(EventType.INTENTION_COMPONENT_CHANGE, 0, EventAction.DELETE_COMPONENT, component1), ComponentChangeEvent(EventType.INTENTION_COMPONENT_CHANGE, 0, EventAction.DELETE_COMPONENT, component2)]
        intention_system.update()
        self.assertEqual(self.event_exchanger.pull_events.call_count, 2)
