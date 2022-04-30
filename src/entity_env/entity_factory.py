from src.components.intention_component import IntentionComponent
from src.components.inventory_component import InventoryComponent
from src.components.map_item_component import MapItemComponent
from src.components.real_component import RealComponent
from src.components.stats_component import StatsComponent
from src.components.drawable_component import DrawableComponent


class EntityFactory:
    def __init__(self, entity_storage):
        self.entity_storage = entity_storage

    def create_player(self, x, y, inventory_capacity):
        entity = self.entity_storage.create_entity()
        self.entity_storage.add_entity_component(entity.id, RealComponent, x, y)
        self.entity_storage.add_entity_component(entity.id, IntentionComponent)
        self.entity_storage.add_entity_component(entity.id, InventoryComponent,
                                                 inventory_capacity)
        self.entity_storage.add_entity_component(entity.id, StatsComponent)
        self.entity_storage.add_entity_component(entity.id, DrawableComponent, "assets/player/")
        return entity.id

    def create_map_item(self, x, y):
        entity = self.entity_storage.create_entity()
        self.entity_storage.add_entity_component(entity.id, RealComponent, x, y)
        self.entity_storage.add_entity_component(entity.id, MapItemComponent)
        self.entity_storage.add_entity_component(entity.id, DrawableComponent, "assets/map_item/")
        return entity.id
