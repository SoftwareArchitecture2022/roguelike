from src.systems.system import System
import random


class LoadSystem(System):
    def __init__(self, entity_factory, entity_storage, event_exchanger,
                 world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.need_update = True
        super(LoadSystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)

    def update(self):
        if self.need_update:
            self.need_update = False
            self.generate()

    # Temporary gen
    def generate(self):
        self.entity_factory.create_player(0, 0, 10)
        for _ in range(5):
            self.entity_factory.create_map_item(random.randint(
                1, self.world_width - 1), random.randint(1, self.world_height - 1))
