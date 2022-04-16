from system import System
from llist import dllist
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from components.intention_component import *
from components.inventory_component import *
from components.stats_component import *

class WearSystem(System):
    def __init__(self, entityFactory, entityStorage, eventExchanger):
        super(WearSystem, self).__init__(entityFactory, entityStorage, eventExchanger)
        self.intentionComponents = dllist()


    def update(self):
        events = self.eventExchanger.pullEvents()
        for i in range(len(events)):
            pass

        for node in self.intentionComponents.iternodes():
            if False: # TODO delete deleted component
                self.components.remove(node)
            self.doWear(node.value)


    def doWear(self, intentionComponent):
        inventoryComponent = self.entityStorage.getEntityComponent(intentionComponent.entityId, InventoryComponent)
        if ACTION_INVENTORY_LEFT in intentionComponent.actions:
            if inventoryComponent.pointer > 0:
                inventoryComponent.pointer -= 1
        if ACTION_INVENTORY_RIGHT in intentionComponent.actions:
            if inventoryComponent.pointer < inventoryComponent.capacity - 1:
                inventoryComponent.pointer += 1
        if ACTION_INVENTORY_EQUIP in intentionComponent.actions:
            statsComponent = self.entityStorage.getEntityComponent(intentionComponent.entityId, StatsComponent)
            item = inventoryComponent.inventory[inventoryComponent.pointer]
            if item.isEquipped:
                item.isEquipped = False
                statsComponent.health -= item.health
                statsComponent.attack -= item.attack
                statsComponent.armor -= item.armor
            else:
                item.isEquipped = True
                statsComponent.health += item.health
                statsComponent.attack += item.attack
                statsComponent.armor += item.armor
