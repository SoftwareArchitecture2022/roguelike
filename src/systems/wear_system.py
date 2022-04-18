from src.components.stats_component import StatsComponent
from src.components.inventory_component import InventoryComponent
import src.components.intention_component as intention
from src.systems.system import System
from llist import dllist
from src.events.event_exchanger import EventType, EventAction


class WearSystem(System):
    def __init__(self, entity_factory, entity_storage, event_exchanger):
        super(WearSystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.intention_components = dllist()
        self.event_exchanger.subscribe(self, EventType.INTENTION_COMPONENT_CHANGE)

    def update(self):
        events = self.event_exchanger.pullEvents()
        deleted_components = set()
        for event in events:
            if event.action == EventAction.ADD_COMPONENT:
                self.intention_components.insert(event.component)
            elif event.action == EventAction.DELETE_COMPONENT:
                deleted_components.add(event.component)
        for node in self.intention_components.iternodes():
            if node.value in deleted_components:
                self.intention_components.remove(node)
                continue
            self.do_wear(node.value)

    def do_wear(self, intention_component):
        inventory_component = self.entity_storage.get_entity_component(
            intention_component.entity_id, InventoryComponent)
        if intention.ACTION_INVENTORY_LEFT in intention_component.actions:
            if inventory_component.pointer > 0:
                inventory_component.pointer -= 1
        if intention.ACTION_INVENTORY_RIGHT in intention_component.actions:
            if inventory_component.pointer < inventory_component.capacity - 1:
                inventory_component.pointer += 1
        if intention.ACTION_INVENTORY_EQUIP in intention_component.actions:
            stats_component = self.entity_storage.get_entity_component(
                intention_component.entity_id, StatsComponent)
            item = inventory_component.inventory[inventory_component.pointer]
            if item.is_equipped:
                item.is_equipped = False
                stats_component.health -= item.health
                stats_component.attack -= item.attack
                stats_component.armor -= item.armor
            else:
                item.is_equipped = True
                stats_component.health += item.health
                stats_component.attack += item.attack
                stats_component.armor += item.armor
