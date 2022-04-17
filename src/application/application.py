
class Application:
    def __init__(self):
        self.systems = []

    def run(self):
        while True:
            for system in self.systems:
                system.update()
