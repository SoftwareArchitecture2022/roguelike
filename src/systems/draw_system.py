from src.systems.system import System
from src.events.event_exchanger import EventType, EventAction
from src.components.real_component import RealComponent
from src.components.drawable_component import DrawableComponent


class ImageBuffer:
    view_types = ['MapView', 'InventoryView', 'StatsView']

    def __init__(self):
        self.views = {}

    def add_view(self, view, view_type):
        assert view_type in self.view_types
        self.views[view_type] = view

    def get_view(self, view_type):
        return self.views.get(view_type)

    def clear(self):
        self.views.clear()


class MapView:
    """
    Содержит данные для отрисовки карты с предметами и персонажем
    """

    def __init__(self, world_width, world_height):
        self.data = [[None] * world_width for _ in range(world_height)]

    def add_drawable(self, drawable, i, j):
        assert 0 <= i < len(self.data) and 0 <= j < len(self.data[0])
        assert self.data[i][j] is None
        self.data[i][j] = drawable


class InventoryView:
    """
    Содержит данные для отрисовки инвентаря: список из drawable-компонентов предметов, какой предмет выбран
    """

    def __init__(self, inventory_capacity):
        self.inventory_drawables = [None for _ in range(inventory_capacity)]

    def add_inventory_drawable(self, drawable, place):
        self.inventory_drawables[place] = drawable

    def set_pointer(self, pointer_pos):
        self.pointer_pos = pointer_pos


class StatsView:
    """
    Содержит данные о характеристиках персонажа
    """
    stat_names = ['health', 'attack', 'armor']

    def __init__(self):
        self.ch_stats = {}

    def add_stat(self, stat_name, value):
        assert stat_name in self.stat_names
        self.ch_stats[stat_name] = value


class DrawSystem(System):
    """
    Отвечает за логическое наполнение буфера изображений: какая информация будет отображаться,
    не заботится в каком масштабе или в каком порядке будут рисоваться вьюшки
    """

    def __init__(self, entity_factory, entity_storage, event_exchanger, world_width, world_height):
        super().__init__(entity_factory, entity_storage, event_exchanger)
        self.world_width = world_width
        self.world_height = world_height
        self.drawables = []
        self.ch_inventory_component = None
        self.ch_stats_component = None
        self.image_buffer = ImageBuffer()
        # подписываемся на события создания компонент drawable, а также inventory и stats персонажа
        self.event_exchanger.subscribe(self, EventType.DRAWABLE_COMPONENT_CHANGE)
        self.event_exchanger.subscribe(self, EventType.INVENTORY_COMPONENT_CHANGE)
        self.event_exchanger.subscribe(self, EventType.STATS_COMPONENT_CHANGE)

    def update(self):
        self.image_buffer.clear()
        # обработка новых событий из event_exchanger
        for event in self.event_exchanger.pull_events(self):
            if event.event_type == EventType.DRAWABLE_COMPONENT_CHANGE:
                if event.event_action == EventAction.ADD_COMPONENT:
                    self.drawables.append(event.component)
                if event.event_action == EventAction.DELETE_COMPONENT:
                    self.drawables.remove(event.component)
            elif event.event_type == EventType.INVENTORY_COMPONENT_CHANGE:
                self.ch_inventory_component = event.component
            elif event.event_type == EventType.STATS_COMPONENT_CHANGE:
                self.ch_stats_component = event.component
        map_view = MapView(self.world_width, self.world_height)
        for d in self.drawables:
            # получение координат i, j из компоненты real соответствующей данной drawable
            real_component = self.entity_storage.get_entity_component(d.entity_id, RealComponent)
            i, j = real_component.x, real_component.y
            map_view.add_drawable(d, i, j)
        self.image_buffer.add_view(map_view, 'MapView')
        if self.ch_inventory_component is not None:
            inventory_view = InventoryView(self.ch_inventory_component.capacity)
            for p, i in enumerate(self.ch_inventory_component.inventory):
                # получение drawable для компонента inventory_item
                d = self.entity_storage.get_entity_component(i.entity_id, DrawableComponent)
                inventory_view.add_inventory_drawable(d, p)
            inventory_view.set_pointer(self.ch_inventory_component.pointer)
            self.image_buffer.add_view(inventory_view, 'InventoryView')
        if self.ch_stats_component is not None:
            stats_view = StatsView()
            stats_view.add_stat('health', self.ch_stats_component.health)
            stats_view.add_stat('attack', self.ch_stats_component.attack)
            stats_view.add_stat('armor', self.ch_stats_component.armor)
            self.image_buffer.add_view(stats_view, 'StatsView')

    def get_image_buffer(self):
        return self.image_buffer
