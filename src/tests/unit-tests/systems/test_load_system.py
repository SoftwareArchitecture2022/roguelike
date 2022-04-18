import unittest
import unittest.mock
from src.systems.load_system import LoadSystem
from src.entity_env.entity_factory import EntityFactory
from src.events.event_exchanger import EventExchanger
from src.entity_env.entity_storage import EntityStorage


class TestLoadSystem(unittest.TestCase):
    def setUp(self):
        self.event_exchanger = EventExchanger()
        self.entity_storage = EntityStorage(self.event_exchanger)
        self.entity_factory = EntityFactory(self.entity_storage)
        self.entity_factory.create_player = unittest.mock.MagicMock()
        self.entity_factory.create_map_item = unittest.mock.MagicMock()

    def test_basic_gen(self):
        system = LoadSystem(self.entity_factory, self.entity_storage, self.event_exchanger, 40, 40)
        system.update()
        self.entity_factory.create_player.assert_called_once()
        self.assertEqual(self.entity_factory.create_map_item.call_count, 100)
