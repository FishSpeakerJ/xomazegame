
import gtk

import gridwidget

def redraw(grid):
    """Utility function to force a redraw of a Gtk widget."""
    grid.window.invalidate_rect(grid.get_allocation(), False)

def key_press_cb(window, event, grid, player):
    if grid.selected_column is None:
        return

    if gtk.gdk.keyval_name(event.keyval) in ('Left',):
        if grid.selected_column > 0:
            grid.selected_column -= 1
            redraw(grid)
    elif gtk.gdk.keyval_name(event.keyval) in ('Right',):
        if grid.selected_column < 6:
            grid.selected_column += 1
            redraw(grid)
    elif gtk.gdk.keyval_name(event.keyval) in ('Down', 'space'):
        if grid.insert(grid.selected_column, player[0]) != -1:
            player[:] = [{1 : 2, 2: 1}[player[0]]]
            redraw(grid)
    elif gtk.gdk.keyval_name(event.keyval) in ('Escape', 'q'):
        gtk.main_quit()

def main():
    grid = gridwidget.GridWidget()
    grid.selected_column = 3

    window = gtk.Window()
    window.connect('destroy', gtk.main_quit)
    window.connect('key-press-event', key_press_cb, grid, [1])
    window.add(grid)
    window.show_all()

    try:
        gtk.main()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

