from component import Component

class InventoryComponent(Component):
    def __init__(self, entityId, capacity):
        self.capacity = capacity
        self.inventory = [None for _ in range(len(capacity))]
        self.pointer = 0
        super(InventoryComponent, self).__init__(entityId)
