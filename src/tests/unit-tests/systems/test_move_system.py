import unittest
import unittest.mock
from src.entity_env.entity_factory import EntityFactory
from src.events.event_exchanger import EventExchanger
from src.entity_env.entity_storage import EntityStorage
from src.systems.move_system import MoveSystem
from src.events.event_exchanger import EventType, EventAction, ComponentChangeEvent
from src.components.real_component import RealComponent
from src.components.intention_component import IntentionComponent
from src.components.intention_component import ACTION_UP, ACTION_LEFT, ACTION_DOWN, ACTION_RIGHT


class TestMoveSystem(unittest.TestCase):
    def setUp(self):
        self.event_exchanger = EventExchanger()
        self.entity_storage = EntityStorage(self.event_exchanger)
        self.entity_factory = EntityFactory(self.entity_storage)
        self.event_exchanger.subscribe = unittest.mock.MagicMock()
        self.event_exchanger.pull_events = unittest.mock.MagicMock()
        self.entity_storage.get_entity_component = unittest.mock.MagicMock()

    def test_move_system_simple(self):
        move_system = MoveSystem(self.entity_factory, self.entity_storage, self.event_exchanger, 100, 100)
        self.event_exchanger.subscribe.assert_called_once_with(move_system, EventType.INTENTION_COMPONENT_CHANGE)

        intention_component = IntentionComponent(0)
        intention_component.actions = {ACTION_UP}
        real_component = RealComponent(0, 20, 20)
        self.entity_storage.get_entity_component.return_value = real_component
        self.event_exchanger.pull_events.return_value = [ComponentChangeEvent(EventType.INTENTION_COMPONENT_CHANGE, 0, EventAction.ADD_COMPONENT, intention_component)]
        move_system.update()
        self.assertEqual(real_component.y, 21)
        self.assertEqual(self.event_exchanger.pull_events.call_count, 1)

    def test_move_system_both_directions(self):
        move_system = MoveSystem(self.entity_factory, self.entity_storage, self.event_exchanger, 100, 100)
        self.event_exchanger.subscribe.assert_called_once_with(move_system, EventType.INTENTION_COMPONENT_CHANGE)

        intention_component = IntentionComponent(0)
        intention_component.actions = {ACTION_UP, ACTION_LEFT, ACTION_DOWN, ACTION_RIGHT}
        real_component = RealComponent(0, 20, 20)
        self.entity_storage.get_entity_component.return_value = real_component
        self.event_exchanger.pull_events.return_value = [ComponentChangeEvent(EventType.INTENTION_COMPONENT_CHANGE, 0, EventAction.ADD_COMPONENT, intention_component)]
        move_system.update()
        self.assertEqual(real_component.y, 20)
        self.assertEqual(real_component.x, 20)
        self.assertEqual(self.event_exchanger.pull_events.call_count, 1)

    def test_move_system_border(self):
        move_system = MoveSystem(self.entity_factory, self.entity_storage, self.event_exchanger, 100, 100)
        self.event_exchanger.subscribe.assert_called_once_with(move_system, EventType.INTENTION_COMPONENT_CHANGE)

        intention_component = IntentionComponent(0)
        intention_component.actions = {ACTION_DOWN, ACTION_LEFT}
        real_component = RealComponent(0, 0, 0)
        self.entity_storage.get_entity_component.return_value = real_component
        self.event_exchanger.pull_events.return_value = [ComponentChangeEvent(EventType.INTENTION_COMPONENT_CHANGE, 0, EventAction.ADD_COMPONENT, intention_component)]
        move_system.update()
        self.assertEqual(real_component.y, 0)
        self.assertEqual(real_component.x, 0)
        self.assertEqual(self.event_exchanger.pull_events.call_count, 1)
