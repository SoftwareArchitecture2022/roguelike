from src.components.real_component import RealComponent
from src.components.inventory_item_component import InventoryItemComponent
from src.systems.system import System
from llist import dllist
from src.events.event_exchanger import EventType, EventAction


class InventorySystem(System):
    def __init__(self, entity_factory, entity_storage, event_exchanger):
        super(InventorySystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.inventory_components = dllist()
        self.map = {}
        self.event_exchanger.subscribe(self, EventType.MAP_ITEM_COMPONENT)
        self.event_exchanger.subscribe(self, EventType.INVENTORY_COMPONENT_CHANGE)

    def update(self):
        events = self.event_exchanger.pull_events()
        deleted_components = set()
        for event in events:
            if event.event_type == EventType.INVENTORY_COMPONENT_CHANGE:
                if event.event_action == EventAction.ADD_COMPONENT:
                    self.inventory_components.insert(event.component)
                elif event.event_action == EventAction.DELETE_COMPONENT:
                    deleted_components.add(event.component)
            elif event.event_type == EventType.MAP_ITEM_COMPONENT:
                real_component = self.entity_storage.get_entity_component(
                    event.component.entity_id, RealComponent)
                point = (real_component.x, real_component.y)
                if event.event_action == EventAction.ADD_COMPONENT:
                    if point not in self.map.keys():
                        self.map[point] = dllist()
                    self.map[point].insert(event.component)
                elif event.event_action == EventAction.DELETE_COMPONENT:
                    # TODO
                    pass

        for node in self.inventory_components.iternodes():
            if node.value in deleted_components:
                self.inventory_components.remove(node)
                continue
            self.check_collision(node.value)

    def remove_map_item(self, point, node):
        self.map[point].remove(node)
        if self.map[point].size == 0:
            del self.map[point]

    def check_collision(self, inventory_component):
        real_component = self.entity_storage.get_entity_component(
            inventory_component.entity_id, RealComponent)
        point = (real_component.x, real_component.y)
        if point in self.map.keys():
            if inventory_component.load < inventory_component.capacity:
                # TODO add args from self.map[point].first
                entity_id = self.entity_factory.create_inventory_item()
                inventory_item_component = self.entity_storage.get_entity_component(
                    entity_id, InventoryItemComponent)
                self.insert_to_inventory(inventory_component, inventory_item_component)
                self.entity_storage.delete_entity(self.map[point].first.value.entity_id)
                self.remove_map_item(point, self.map[point].first)

    def insert_to_inventory(self, inventory_component, item):
        for i in range(len(inventory_component.inventory)):
            if inventory_component.inventory[i] is None:
                inventory_component.inventory[i] = item
                inventory_component.load += 1
                break
