import unittest

from src.components.intention_component import IntentionComponent
from src.components.inventory_component import InventoryComponent
from src.entity_env.entity import Entity
from src.entity_env.entity_storage import EntityStorage
from src.events.event_exchanger import EventExchanger, EventType, EventAction


class TestEntityStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.event_exchanger = EventExchanger()
        self.entity_storage = EntityStorage(self.event_exchanger)
        self.entity = Entity()

    def test_add_entity_component(self):
        self.entity_storage.add_entity_component(self.entity.id,
                                                 IntentionComponent)
        self.assertTrue(
            self.entity_storage.entity_to_components[self.entity.id][
                IntentionComponent])

        event_type = EventType.INTENTION_COMPONENT_CHANGE
        action = EventAction.ADD_COMPONENT
        events = self.event_exchanger.emitted_events.get(event_type)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.event_type, event_type)
        self.assertEqual(event.subscribed_systems_left, 0)
        self.assertEqual(event.event_action, action)

    def test_get_entity_component(self):
        self.test_add_entity_component()
        component = self.entity_storage.get_entity_component(self.entity.id,
                                                             IntentionComponent)
        self.assertEqual(component,
                         self.entity_storage.entity_to_components[
                             self.entity.id][
                             IntentionComponent])

    def test_delete_entity_component(self):
        self.test_add_entity_component()
        self.entity_storage.delete_entity_component(self.entity.id,
                                                    IntentionComponent)
        component = self.entity_storage.get_entity_component(self.entity.id,
                                                             IntentionComponent)
        self.assertFalse(component)

        event_type = EventType.INTENTION_COMPONENT_CHANGE
        action = EventAction.DELETE_COMPONENT
        events = self.event_exchanger.emitted_events.get(event_type)
        self.assertEqual(len(events), 2)
        event = events[-1]
        self.assertEqual(event.event_type, event_type)
        self.assertEqual(event.subscribed_systems_left, 0)
        self.assertEqual(event.event_action, action)

    def test_delete_entity_no_component(self):
        self.test_add_entity_component()
        self.entity_storage.delete_entity_component(self.entity.id,
                                                    InventoryComponent)
        component = self.entity_storage.get_entity_component(self.entity.id,
                                                             InventoryComponent)
        self.assertFalse(component)

        event_type = EventType.INVENTORY_COMPONENT_CHANGE
        events = self.event_exchanger.emitted_events.get(event_type)
        self.assertEqual(len(events), 0)

    def test_delete_entity(self):
        entity = self.entity_storage.create_entity()
        self.entity_storage.add_entity_component(entity.id, IntentionComponent)
        self.assertFalse(self.entity_storage.delete_entity(entity.id))

        self.assertFalse(
            self.entity_storage.entity_to_components.get(entity.id))

        event_type = EventType.INTENTION_COMPONENT_CHANGE
        events = self.event_exchanger.emitted_events.get(event_type)
        self.assertEqual(len(events), 2)

    def test_delete_no_entity(self):
        fake_entity_id = 100500
        self.assertFalse(self.entity_storage.delete_entity(fake_entity_id))

        self.assertFalse(
            self.entity_storage.entity_to_components.get(fake_entity_id))
