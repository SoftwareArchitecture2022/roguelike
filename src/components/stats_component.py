from component import Component


class StatsComponent(Component):
    def __init__(self, entityId):
        self.health = 100
        self.attack = 10
        self.armor = 0
        super(StatsComponent, self).__init__(entityId)
