from src.components.real_component import RealComponent
from src.systems.system import System
from llist import dllist
from src.events.event_exchanger import EventType, EventAction


class InventorySystem(System):
    def __init__(self, entity_factory, entity_storage, event_exchanger):
        super(InventorySystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.inventory_components = dllist()
        self.map = {}
        self.event_exchanger.subscribe(self, EventType.INVENTORY_COMPONENT_CHANGE)

    def update(self):
        events = self.event_exchanger.pull_events()
        deleted_components = set()
        for event in events:
            if event.action == EventAction.ADD_COMPONENT:
                self.inventory_components.insert(event.component)
            elif event.action == EventAction.DELETE_COMPONENT:
                deleted_components.add(event.component)

        for node in self.inventory_components.iternodes():
            if node.value in deleted_components:
                self.inventory_components.remove(node)
                continue
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
