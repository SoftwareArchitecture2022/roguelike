from src.components.component import Component


class RealComponent(Component):
    def __init__(self, entity_id, x, y):
        super(RealComponent, self).__init__(entity_id)
        self.x = x
        self.y = y
