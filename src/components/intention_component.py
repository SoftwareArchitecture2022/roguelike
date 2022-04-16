from component import Component

KEY_W = 0
KEY_A = 1
KEY_S = 2
KEY_D = 3
ACTION_UP = 0
ACTION_LEFT = 1
ACTION_DOWN = 2
ACTION_RIGHT = 3

class IntentionComponent(Component):
    def __init__(self, entityId):
        super(IntentionComponent, self).__init__(entityId)
        self.actions = set()

