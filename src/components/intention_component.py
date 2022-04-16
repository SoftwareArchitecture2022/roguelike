from component import Component

# TODO: Enum this
KEY_W = 0
KEY_A = 1
KEY_S = 2
KEY_D = 3
KEY_X = 4
KEY_Q = 5
KEY_E = 6
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

