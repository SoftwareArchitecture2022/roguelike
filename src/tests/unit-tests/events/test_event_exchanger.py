import unittest

from src.components.intention_component import IntentionComponent
from src.entity_env.entity import Entity
from src.entity_env.entity_factory import EntityFactory
from src.entity_env.entity_storage import EntityStorage
from src.events.event_exchanger import EventExchanger, EventType, EventAction
from src.systems.system import System


class TestEventExchanger(unittest.TestCase):
    def setUp(self) -> None:
        self.event_exchanger = EventExchanger()
        entity_storage = EntityStorage(self.event_exchanger)
        entity_factory = EntityFactory(entity_storage)
        self.system = System(entity_factory, entity_storage,
                             self.event_exchanger)

    def test_subscribe(self):
        event_type = EventType.INTENTION_COMPONENT_CHANGE
        self.event_exchanger.subscribe(self.system, event_type)
        self.assertEqual(self.event_exchanger.count_event_sub[event_type], 1)
        self.assertEqual(
            self.event_exchanger.system_to_event_types[self.system],
            {event_type})

    def test_emit_event(self):
        self.test_subscribe()

        event_type = EventType.INTENTION_COMPONENT_CHANGE
        action = EventAction.ADD_COMPONENT
        entity = Entity()
        component = IntentionComponent(entity.id)
        self.event_exchanger.emit_event(event_type, action, component)

        events = self.event_exchanger.emitted_events.get(event_type)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.event_type, event_type)
        self.assertEqual(event.subscribed_systems_left, 1)
        self.assertEqual(event.event_action, action)
        self.assertEqual(event.component, component)
