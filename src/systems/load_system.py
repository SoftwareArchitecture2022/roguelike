from system import System
import random

class LoadSystem(System):
    def __init__(self, entityFactory, entityStorage, eventExchanger, worldWidth, worldHeight):
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight
        self.needUpdate = True
        super(LoadSystem, self).__init__(entityFactory, entityStorage, eventExchanger)

    def update(self):
        if self.needUpdate:
            self.needUpdate = False
            self.generate()

    # Temporary gen
    def generate(self):
        self.entityFactory.createPlayer(0, 0)
        for _ in range(100):
            self.entityFactory.createMapItem(random.randint(1, self.worldWidth - 1), random.randint(1, self.worldHeight - 1))
