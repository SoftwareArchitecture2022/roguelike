import unittest

from src.entity_env.entity_storage import EntityStorage
from src.events.event_exchanger import EventExchanger


class TestEntityStorage(unittest.TestCase):
    def setUp(self) -> None:
        event_exchanger = EventExchanger()
        self.entity_storage = EntityStorage(event_exchanger)


if __name__ == "__main__":
    unittest.main()
