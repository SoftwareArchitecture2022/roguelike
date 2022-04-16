from component import Component

class InventoryComponent(Component):
    def __init__(self, entityId, capacity):
        self.inventory = [None for _ in range(len(capacity))]
        super(InventoryComponent, self).__init__(entityId)

    def insert(self, item):
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                self.inventory[i] = item
                return True
        return False

