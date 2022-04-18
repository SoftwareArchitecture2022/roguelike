from src.systems.system import System
from pynput import keyboard
from src.systems.input_state import KEY_Q, KEY_E, KEY_X, KEY_W, KEY_A, KEY_S, KEY_D


class InputSystem(System):
    def __init__(self, input_state, entity_factory, entity_storage, event_exchanger):
        super(InputSystem, self).__init__(
            entity_factory, entity_storage, event_exchanger)
        self.input_state = input_state

    def update(self):
        with keyboard.Events() as events:
            for event in events:
                if event.key == keyboard.Key.q:
                    self.input_state.keys.insert(KEY_Q)
                elif event.key == keyboard.Key.e:
                    self.input_state.keys.insert(KEY_E)
                elif event.key == keyboard.Key.x:
                    self.input_state.keys.insert(KEY_X)
                elif event.key == keyboard.Key.w:
                    self.input_state.keys.insert(KEY_W)
                elif event.key == keyboard.Key.a:
                    self.input_state.keys.insert(KEY_A)
                elif event.key == keyboard.Key.s:
                    self.input_state.keys.insert(KEY_S)
                elif event.key == keyboard.Key.d:
                    self.input_state.keys.insert(KEY_D)
