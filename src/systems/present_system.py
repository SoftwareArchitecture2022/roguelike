from system import System


class ConsoleWindow:
    """
    Интерфейс для консольного окна, в котором PresentSystem будет отрисовывать графику.
    Если будем пользоваться библиотекой curses, можно просто взять curses.initscr()
    """

    def addstr(self, i, j, string):
        pass

    def addch(self, i, j, char):
        pass

    def refresh(self):
        pass

    def clear(self):
        pass

    def getmaxyx(self):
        pass


class PresentSystem(System):
    """
    Определяет размеры вьюшек и их расположение на экране, рисует их
    """

    def set_window(self, window):
        self.window = window

    def set_image_buffer(self, image_buffer):
        self.image_buffer = image_buffer

    def _draw_image(self, y, x, image):
        self.window.addstr(y, x, image)

    def update(self):
        self.window.clear()
        vertical_shift = 0
        map_view = self.image_buffer.get_view('MapView')
        tile_size = 1
        # TODO возможно, расчет размера тайла исходя из размера окна, на котором рисуем
        for i, col in enumerate(map_view.data):
            for j, d in enumerate(col):
                if d is None:
                    continue
                self._draw_image(i * tile_size + vertical_shift, j * tile_size, d.get_image(tile_size))
        vertical_shift += tile_size * len(map_view.data)
        inventory_view = self.image_buffer.get_view('InventoryView')
        inventory_item_size = 1
        for i, d in enumerate(inventory_view.inventory_drawables):
            if d is None:
                continue
            self._draw_image(vertical_shift, inventory_item_size * i, d.get_image(inventory_item_size))
        self._draw_image(1 + vertical_shift, inventory_item_size * inventory_view.pointer_pos, '^')
        vertical_shift += 2
        stats_view = self.image_buffer.get_view('StatsView')
        for i, k in enumerate(stats_view.ch_stats):
            self._draw_image(i + vertical_shift, 0, k + ": " + str(stats_view.ch_stats[k]))
        self.window.refresh()
