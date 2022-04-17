from entity import Entity
from src.events.event_exchanger import component_type_to_event_type, EventAction


class EntityStorage:
    def __init__(self, event_exchanger):
        """
            initializes internal vars
        """
        self.event_exchanger = event_exchanger
        self.entity_to_components = {}

    def create_entity(self):
        """
            creates entity
        """
        entity = Entity()
        self.entity_to_components[entity.id] = {}
        return entity

    def get_entity_component(self, entity_id, component_type):
        """
            gets component by its type and entity id
        """
        return self.entity_to_components[entity_id][component_type]

    def add_entity_component(self, entity_id, component_type, *args, **kwargs):
        """
            adds component to the entity and emits corresponding event
        """
        component = component_type(entity_id, *args, **kwargs)
        type_to_component = {component_type: component}
        if entity_components := self.entity_to_components.get(entity_id):
            entity_components.update(type_to_component)
        else:
            self.entity_to_components[entity_id] = type_to_component

        self.event_exchanger.emit_event(
            component_type_to_event_type(component_type),
            EventAction.ADD_COMPONENT, component)

    def delete_entity_component(self, entity_id, component_type):
        """
            removes component from storage end emits corresponding event
        """
        if entity_components := self.entity_to_components.get(entity_id):
            if component := entity_components.get(component_type):
                self.emit_delete_component_event(component)
            entity_components.pop(component_type)

    def emit_delete_component_event(self, component):
        """
            emits delete component event
        """
        self.event_exchanger.emit_event(
            component_type_to_event_type(type(component)),
            EventAction.DELETE_COMPONENT, component)

    def delete_entity(self, entity_id):
        """
            removes entity with its components by entity id.
            emits delete events for components.
        """
        if entity_components := self.entity_to_components.get(entity_id):
            for component_type, component in entity_components.items():
                self.emit_delete_component_event(component)
        self.entity_to_components.pop(entity_id)
