from components.real_component import RealComponent
from system import System
from llist import dllist
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class InventorySystem(System):
    def __init__(self, entityFactory, entityStorage, eventExchanger):
        super(InventorySystem, self).__init__(
            entityFactory, entityStorage, eventExchanger)
        self.inventoryComponents = dllist()
        self.map = {}

    def update(self):
        events = self.eventExchanger.pullEvents()
        for i in range(len(events)):
            pass

        for node in self.inventoryComponents.iternodes():
            if False:  # TODO delete deleted component
                self.inventoryComponents.remove(node)
            self.checkCollision(node.value)

    def checkCollision(self, inventoryComponent):
        realComponent = self.entityStorage.getEntityComponent(
            inventoryComponent.entityId, RealComponent)
        point = (realComponent.x, realComponent.y)
        if point in self.map.keys():
            if self.insertToInventory(inventoryComponent, self.map[point].first):
                self.entityStorage.deleteEntity(self.map[point].first.entityId)
                self.map[point].remove(self.map[point].first)
                if self.map[point].size() == 0:
                    del self.map[point]

    def insertToInventory(self, inventoryComponent, item):
        for i in range(len(inventoryComponent.inventory)):
            if inventoryComponent.inventory[i] is None:
                inventoryComponent.inventory[i] = item
                return True
        return False
