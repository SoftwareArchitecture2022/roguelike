from components.real_component import RealComponent
from system import System
from llist import dllist
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class InventorySystem(System):
    def __init__(self, entity_factory, entity_storage, event_exchanger):
        super(InventorySystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.inventory_components = dllist()
        self.map = {}

    def update(self):
        events = self.event_exchanger.pull_events()
        for i in range(len(events)):
            pass

        for node in self.inventory_components.iternodes():
            if False:  # TODO delete deleted component
                self.inventory_components.remove(node)
            self.check_collision(node.value)

    def check_collision(self, inventory_component):
        real_component = self.entity_storage.get_entity_component(
            inventory_component.entityId, RealComponent)
        point = (real_component.x, real_component.y)
        if point in self.map.keys():
            if self.insert_to_inventory(inventory_component, self.map[point].first):
                self.entity_storage.delete_entity(self.map[point].first.entityId)
                self.map[point].remove(self.map[point].first)
                if self.map[point].size() == 0:
                    del self.map[point]

    def insert_to_inventory(self, inventory_component, item):
        for i in range(len(inventory_component.inventory)):
            if inventory_component.inventory[i] is None:
                inventory_component.inventory[i] = item
                return True
        return False
