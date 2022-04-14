from component import Component

class IntentionComponent(Component):
    def __init__(self, entityId):
        super(Component, self).__init__(entityId)
        self.actions = set()

