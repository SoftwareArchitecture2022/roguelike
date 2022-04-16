from component import Component

class RealComponent(Component):
    def __init__(self, entityId, x, y):
        super(RealComponent, self).__init__(entityId)
        self.x = x
        self.y = y

