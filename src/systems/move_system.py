from src.components.real_component import RealComponent
import src.components.intention_component as intention
from src.systems.system import System
from llist import dllist
from src.events.event_exchanger import EventType, EventAction


class MoveSystem(System):
    def __init__(self, entity_factory, entity_storage, event_exchanger,
                 world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        super(MoveSystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.components = dllist()
        self.event_exchanger.subscribe(self, EventType.INTENTION_COMPONENT_CHANGE)

    def update(self):
        events = self.event_exchanger.pull_events()
        deleted_components = set()
        for event in events:
            if event.event_action == EventAction.ADD_COMPONENT:
                self.components.insert(event.component)
            elif event.event_action == EventAction.DELETE_COMPONENT:
                deleted_components.add(event.component)

        for node in self.components.iternodes():
            if node.value in deleted_components:
                self.components.remove(node)
                continue
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
