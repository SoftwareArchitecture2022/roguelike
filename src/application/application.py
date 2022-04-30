import curses

from src.entity_env.entity_factory import EntityFactory
from src.entity_env.entity_storage import EntityStorage
from src.events.event_exchanger import EventExchanger

from src.systems.draw_system import DrawSystem
from src.systems.present_system import PresentSystem


class Application:
    def __init__(self):
        self.systems = []
        event_exchanger = EventExchanger()
        entity_storage = EntityStorage(event_exchanger)
        entity_factory = EntityFactory(entity_storage)
        world_width = 10
        world_height = 10
        # creating systems
        draw_system = DrawSystem(entity_factory, entity_storage, event_exchanger, world_width, world_height)
        self.systems.append(draw_system)
        present_system = PresentSystem(entity_factory, entity_storage, event_exchanger, draw_system.get_image_buffer())
        self.systems.append(present_system)
        # creating window with curses library
        screen = curses.initscr()
        present_system.set_window(screen)

    def run(self):
        while True:
            for system in self.systems:
                system.update()
            curses.napms(10)
        curses.endwin()
