from src.components.component import Component


class StatsComponent(Component):
    def __init__(self, entity_id):
        self.health = 100
        self.attack = 10
        self.armor = 0
        super(StatsComponent, self).__init__(entity_id)
