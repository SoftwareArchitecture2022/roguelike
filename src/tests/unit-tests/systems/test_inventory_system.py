import unittest
import unittest.mock
from src.entity_env.entity_factory import EntityFactory
from src.events.event_exchanger import EventExchanger
from src.entity_env.entity_storage import EntityStorage
from src.systems.inventory_system import InventorySystem
from src.events.event_exchanger import EventType, EventAction, ComponentChangeEvent
from src.components.real_component import RealComponent
from src.components.map_item_component import MapItemComponent
from src.components.inventory_component import InventoryComponent


class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        self.event_exchanger = EventExchanger()
        self.entity_storage = EntityStorage(self.event_exchanger)
        self.entity_factory = EntityFactory(self.entity_storage)
        self.event_exchanger.subscribe = unittest.mock.MagicMock()
        self.event_exchanger.pull_events = unittest.mock.MagicMock()
        self.entity_storage.get_entity_component = unittest.mock.MagicMock()
        self.entity_factory.create_inventory_item = unittest.mock.MagicMock()
        self.entity_storage.delete_entity = unittest.mock.MagicMock()

    def test_basic(self):
        inventory_system = InventorySystem(self.entity_factory, self.entity_storage, self.event_exchanger)
        self.event_exchanger.subscribe.assert_any_call(inventory_system, EventType.INVENTORY_COMPONENT_CHANGE)
        self.event_exchanger.subscribe.assert_any_call(inventory_system, EventType.MAP_ITEM_COMPONENT)

        inventory_component = InventoryComponent(0, 4)
        real_component = RealComponent(0, 10, 10)
        self.entity_storage.get_entity_component.return_value = real_component
        map_item_component1 = MapItemComponent(1)
        map_item_component2 = MapItemComponent(2)
        self.event_exchanger.pull_events.return_value = [ComponentChangeEvent(EventType.MAP_ITEM_COMPONENT, 0, EventAction.ADD_COMPONENT, map_item_component1), ComponentChangeEvent(EventType.MAP_ITEM_COMPONENT, 0, EventAction.ADD_COMPONENT, map_item_component2), ComponentChangeEvent(EventType.INVENTORY_COMPONENT_CHANGE, 0, EventAction.ADD_COMPONENT, inventory_component)]
        inventory_system.update()
        self.event_exchanger.pull_events.return_value = []

        self.assertEqual(self.entity_factory.create_inventory_item.call_count, 1)
        self.assertEqual(self.entity_storage.delete_entity.call_count, 1)
        inventory_system.update()
        self.assertEqual(self.entity_factory.create_inventory_item.call_count, 2)
        self.assertEqual(self.entity_storage.delete_entity.call_count, 2)
        inventory_system.update()
        self.assertEqual(self.entity_factory.create_inventory_item.call_count, 2)
        self.assertEqual(self.entity_storage.delete_entity.call_count, 2)
