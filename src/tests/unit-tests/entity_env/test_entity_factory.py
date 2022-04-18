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
        id = self.entity_factory.create_player(4, 4, 5)
        self.assertEqual(id, 0)


if __name__ == "__main__":
  unittest.main()