import curses

from src.entity_env.entity_factory import EntityFactory
from src.entity_env.entity_storage import EntityStorage
from src.events.event_exchanger import EventExchanger

from src.systems.draw_system import DrawSystem
from src.systems.input_state import InputState
from src.systems.input_system import InputSystem
from src.systems.intention_system import IntentionSystem
from src.systems.inventory_system import InventorySystem
from src.systems.load_system import LoadSystem
from src.systems.present_system import PresentSystem
from src.systems.wear_system import WearSystem


class Application:
    def __init__(self):
        """
        inits application
        """
        event_exchanger = EventExchanger()
        entity_storage = EntityStorage(event_exchanger)
        entity_factory = EntityFactory(entity_storage)
        self.systems = []
        self.init_systems(event_exchanger, entity_storage, entity_factory)

    def init_systems(self, event_exchanger, entity_storage, entity_factory):
        """
        initializes all systems
        """
        world_width = 10
        world_height = 10
        # creating systems

        load_system = LoadSystem(
            entity_factory,
            entity_storage,
            event_exchanger,
            world_width,
            world_height,
        )
        self.systems.append(load_system)

        input_state = InputState()
        input_system = InputSystem(
            input_state,
            entity_factory,
            entity_storage,
            event_exchanger,
        )
        self.systems.append(input_system)

        intention_system = IntentionSystem(
            input_state,
            entity_factory,
            entity_storage,
            event_exchanger,
        )
        self.systems.append(intention_system)

        inventory_system = InventorySystem(
            entity_factory,
            entity_storage,
            event_exchanger,
        )
        self.systems.append(inventory_system)

        wear_system = WearSystem(
            entity_factory,
            entity_storage,
            event_exchanger,
        )
        self.systems.append(wear_system)

        draw_system = DrawSystem(
            entity_factory,
            entity_storage,
            event_exchanger,
            world_width,
            world_height,
        )
        self.systems.append(draw_system)
        present_system = PresentSystem(
            entity_factory,
            entity_storage,
            event_exchanger,
            draw_system.get_image_buffer(),
        )
        self.systems.append(present_system)
        # creating window with curses library
        screen = curses.initscr()
        present_system.set_window(screen)

    def run(self):
        try:
            while True:
                for system in self.systems:
                    system.update()
                curses.napms(10)
        except KeyboardInterrupt:
            curses.endwin()
