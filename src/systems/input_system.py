from system import System
from pynput import keyboard
from systems.input_state import KEY_Q, KEY_E, KEY_X, KEY_W, KEY_A, KEY_S, KEY_D


class InputSystem(System):
    def __init__(self, inputState, entityFactory, entityStorage, eventExchanger):
        super(InputSystem, self).__init__(
            entityFactory, entityStorage, eventExchanger)
        self.inputState = inputState

    def update(self):
        with keyboard.Events() as events:
            for event in events:
                if event.key == keyboard.Key.q:
                    self.inputState.keys.insert(KEY_Q)
                elif event.key == keyboard.Key.e:
                    self.inputState.keys.insert(KEY_E)
                elif event.key == keyboard.Key.x:
                    self.inputState.keys.insert(KEY_X)
                elif event.key == keyboard.Key.w:
                    self.inputState.keys.insert(KEY_W)
                elif event.key == keyboard.Key.a:
                    self.inputState.keys.insert(KEY_A)
                elif event.key == keyboard.Key.s:
                    self.inputState.keys.insert(KEY_S)
                elif event.key == keyboard.Key.d:
                    self.inputState.keys.insert(KEY_D)
