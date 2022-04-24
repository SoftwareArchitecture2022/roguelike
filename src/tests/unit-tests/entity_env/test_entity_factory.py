import unittest

from src.entity_env.entity_factory import EntityFactory
from src.entity_env.entity_storage import EntityStorage
from src.events.event_exchanger import EventExchanger


class TestEntityFactory(unittest.TestCase):
    def setUp(self) -> None:
        event_exchanger = EventExchanger()
        entity_storage = EntityStorage(event_exchanger)
        self.entity_factory = EntityFactory(entity_storage)

    def test_create_player(self):
        player_id = self.entity_factory.create_player(4, 4, 5)
        self.assertNotEqual(player_id, None)

        components = self.entity_factory.entity_storage.entity_to_components[
            player_id]
        self.assertEqual(len(components), 4)

    def test_create_map_item(self):
        item_id = self.entity_factory.create_map_item(1, 1)
        self.assertNotEqual(item_id, None)

        components = self.entity_factory.entity_storage.entity_to_components[
            item_id]
        self.assertEqual(len(components), 2)
