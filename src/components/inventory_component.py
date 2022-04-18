from src.components.component import Component


class InventoryComponent(Component):
    def __init__(self, entity_id, capacity):
        self.capacity = capacity
        self.inventory = [None for _ in range(capacity)]
        self.pointer = 0
        super(InventoryComponent, self).__init__(entity_id)
