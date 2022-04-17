from components.real_component import RealComponent
import components.intention_component as intention
from system import System
from llist import dllist
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class MoveSystem(System):
    def __init__(self, entity_factory, entity_storage, event_exchanger,
                 world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        super(MoveSystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.components = dllist()

    def update(self):
        events = self.event_exchanger.pullEvents()
        for i in range(len(events)):
            pass

        for node in self.components.iternodes():
            if False:  # TODO delete deleted component
                self.components.remove(node)
            self.do_move(node.value)

    def do_move(self, intention_component):
        real_component = self.entity_storage.get_entity_component(
            intention_component.entity_id, RealComponent)
        if real_component.y < self.world_height - 1 and intention.ACTION_UP in intention_component.actions:
            real_component.y += 1
        if real_component.y > 0 and intention.ACTION_DOWN in intention_component.actions:
            real_component.y -= 1
        if real_component.x < self.world_width - 1 and intention.ACTION_RIGHT in intention_component.actions:
            real_component.x += 1
        if real_component.x > 0 and intention.ACTION_LEFT in intention_component.actions:
            real_component.x -= 1
