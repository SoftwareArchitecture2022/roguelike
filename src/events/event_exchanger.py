from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

from src.components.component import Component
from src.components.intention_component import IntentionComponent
from src.components.inventory_component import InventoryComponent
from src.components.real_component import RealComponent
from src.components.stats_component import StatsComponent


class EventType(Enum):
    INTENTION_COMPONENT_CHANGE = 1
    INVENTORY_COMPONENT_CHANGE = 2
    REAL_COMPONENT_CHANGE = 3
    STATS_COMPONENT_CHANGE = 4
    MAP_ITEM_COMPONENT = 5
    INVENTORY_ITEM_COMPONENT_CHANGE = 6
    DRAWABLE_COMPONENT_CHANGE = 7


class EventAction(Enum):
    ADD_COMPONENT = 1
    DELETE_COMPONENT = 2


@dataclass
class ComponentChangeEvent:
    event_type: EventType
    subscribed_systems_left: int
    event_action: EventAction
    component: Component


component_type_to_event_type = {
    type(IntentionComponent): EventType.INTENTION_COMPONENT_CHANGE,
    type(InventoryComponent): EventType.INVENTORY_COMPONENT_CHANGE,
    type(RealComponent): EventType.REAL_COMPONENT_CHANGE,
    type(StatsComponent): EventType.STATS_COMPONENT_CHANGE,
    # TODO: add components
}


def get_event_type(self, component_type):
    return component_type_to_event_type[component_type]


class EventExchanger:
    def __init__(self):
        self.system_to_event_types = {}
        self.count_event_sub = defaultdict(int)
        self.emitted_events = {event_type: [] for event_type in EventType}

    def subscribe(self, system, event_type):
        if events := self.system_to_event_types.get(system):
            if event_type in events:
                return
            events.add(event_type)
        else:
            self.system_to_event_types[system] = set(event_type)
        self.count_event_sub[event_type] += 1

    def emit_event(self, event_type, action, component):
        if action not in EventExchanger.components_actions:
            raise RuntimeError(f"action {action} is not supported")

        events = self.emitted_events.get(event_type)
        if events is None:
            raise RuntimeError(
                f"event type {event_type} is not in emitted_events dict")

        events.append(ComponentChangeEvent(
            event_type,
            self.count_event_sub[event_type],
            action,
            component,
        ))

    def pull_events(self, system):
        event_types = self.system_to_event_types[system]
        result = []
        for event_type in event_types:
            tmp = []
            for event in self.emitted_events[event_type]:
                event.subscribed_systems_left -= 1
                if event.subscribed_systems_left >= 0:
                    result.append(event)
                    tmp.append(event)
            self.emitted_events[event_type] = tmp

        return result

    components_actions = [EventAction.ADD_COMPONENT,
                          EventAction.DELETE_COMPONENT]
