from component import Component

# TODO: Enum this
ACTION_UP = 0
ACTION_LEFT = 1
ACTION_DOWN = 2
ACTION_RIGHT = 3
ACTION_INVENTORY_EQUIP = 4
ACTION_INVENTORY_LEFT = 5
ACTION_INVENTORY_RIGHT = 6


class IntentionComponent(Component):
    def __init__(self, entityId):
        super(IntentionComponent, self).__init__(entityId)
        self.actions = set()
