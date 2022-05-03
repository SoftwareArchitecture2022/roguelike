from src.systems.system import System
from pynput import keyboard
from src.systems.input_state import KEY_Q, KEY_E, KEY_X, KEY_W, KEY_A, KEY_S, KEY_D
import queue


class InputSystem(System):
    def __init__(self, input_state, entity_factory, entity_storage, event_exchanger):
        super(InputSystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.input_state = input_state
        self.events = queue.Queue()
        listener = keyboard.Listener(
            on_press=self.on_press)
        listener.start()

    def on_press(self, key):
        try:
            self.events.put(key.char)
        except AttributeError:
            pass

    def update(self):
        while not self.events.empty():
            key = str(self.events.get())
            if key == "q":
                self.input_state.keys.add(KEY_Q)
            elif key == 'e':
                self.input_state.keys.add(KEY_E)
            elif key == 'x':
                self.input_state.keys.add(KEY_X)
            elif key == 'w':
                self.input_state.keys.add(KEY_W)
            elif key == 'a':
                self.input_state.keys.add(KEY_A)
            elif key == 's':
                self.input_state.keys.add(KEY_S)
            elif key == 'd':
                self.input_state.keys.add(KEY_D)
