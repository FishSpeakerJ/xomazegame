import logging

import cairo
import gobject
import gtk


logger = logging.getLogger('connect-activity.gridwidget')


class GridWidget(gtk.EventBox):
    "Gtk widget for discs in a grid."""

    __gsignals__ = {
            'insert-requested': (gobject.SIGNAL_RUN_FIRST, None, [int]),
            }

    def __init__(self):
        gtk.EventBox.__init__(self)

        self.output = gtk.DrawingArea()
        self.set_property('child', self.output)

        self.output.connect('expose-event', self.expose_cb)
        self.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.connect('button-release-event', self.__class__.button_release_cb)
        self.connect('motion-notify-event', self.__class__.motion_cb)

        self.columns = 7
        self.rows = 6
        self.grid = [[-1] * self.columns for i in xrange(self.rows)]
        self.colors = {0: (0.9, 0, 0, 1), 1: (0, 0, 0.9, 1)}
        self.selected_column = None
        self.selection_color = (0.1, 0.1, 0.7, 1)
        self.background_color = (0.7, 0.7, 0.7, 1)
        self.background_selection_color = (0.9, 0.9, 0.9, 1)
        self.highlighted_discs = []
        self.highlighted_color = (1, 0, 0, 1)

    def check_coord (self, i, j):
        return i >= 0 and i < self.rows and j >= 0 and j < self.columns

    def insert(self, column, value):
        """Return:
            None : no winner
            0, 1: player 0/1 wins the game
        """
        discs = [row[column] for row in self.grid]

        if -1 not in discs:
            raise ValueError('Column is full')

        row = self.rows - list(reversed(discs)).index(-1) - 1
        self.grid[row][column] = value

        return self.check_winner(row, column, value)

    def check_winner (self, row, column, player):
        # check column
        if row <= 2:
            discs = [self.grid[i][column] for i in range(row, row + 4)]
            if discs == [player] * 4:
                logger.debug("win column")
                self.highlighted_discs = [(i, column) for i in range(row, row + 4)]
                return player

        # check row
        discs = self.grid[row]
        count = 0
        for i in range(self.columns):
            if discs[i] == player:
                count += 1
                self.highlighted_discs.append((row, i))
                if count == 4:
                    break
            else:
                self.highlighted_discs = []
                count = 0

        if count == 4:
            logger.debug("win row")
            return player

        # check down left -> up right diagonal
        count = 1
        self.highlighted_discs = [(row, column)]

        i, j = row - 1, column + 1
        move_up = self.check_coord(i, j)
        while move_up:
            if self.grid[i][j] != player:
                break

            count += 1
            self.highlighted_discs.append((i,j))

            i, j = i - 1, j + 1
            move_up = self.check_coord(i, j)

        i, j = row + 1, column - 1
        move_down = self.check_coord(i, j)
        while move_down:
            if self.grid[i][j] != player:
                break

            count += 1
            self.highlighted_discs.append((i,j))

            i, j = i + 1, j - 1
            move_down = self.check_coord(i, j)

        if count >= 4:
            logger.debug("win down left -> up right diag")
            return player

       # check down right -> up left diagonal
        count = 1
        self.highlighted_discs = [(row, column)]

        i, j = row - 1, column - 1
        move_up = self.check_coord(i, j)
        while move_up:
            if self.grid[i][j] != player:
                break

            count += 1
            self.highlighted_discs.append((i,j))

            i, j = i - 1, j - 1
            move_up = self.check_coord(i, j)

        i, j = row + 1, column + 1
        move_down = self.check_coord(i, j)
        while move_down:
            if self.grid[i][j] != player:
                break

            count += 1
            self.highlighted_discs.append((i,j))

            i, j = i + 1, j + 1
            move_down = self.check_coord(i, j)

        if count >= 4:
            logger.debug("win down right -> up left diag")
            return player

        self.highlighted_discs = []
        return None

    def draw_background(self, rect, unit, ctx):
        ctx.set_source_rgba(*self.background_color)
        ctx.rectangle(0, 0, unit * self.columns, unit * self.rows)
        ctx.fill()

        if self.selected_column is not None:
            ctx.set_source_rgba(*self.background_selection_color)
            ctx.rectangle(self.selected_column * unit, 0, unit,
                self.rows * unit)
            ctx.fill()

    def draw_lines(self, rect, unit, ctx):
        ctx.set_line_width(unit / 128.0)
        ctx.set_source_rgba(0, 0, 0, 0.1)

        for i in xrange(self.rows + 1):
            ctx.move_to(0, i * unit)
            ctx.line_to(self.columns * unit, i * unit)

        for i in xrange(self.columns + 1):
            ctx.move_to(i * unit, 0)
            ctx.line_to(i * unit, self.rows * unit)

        ctx.stroke()

        if self.selected_column is not None:
            ctx.set_line_width(unit / 32.0)
            ctx.set_source_rgba(*self.selection_color)
            ctx.rectangle(self.selected_column * unit, 0, unit,
                self.rows * unit)
            ctx.stroke()

    def draw_disc(self, x, y, color, unit, ctx):
        ctx.set_source_rgba(*color)
        ctx.arc(x, y, 0.4 * unit, 0, -1e-10)
        ctx.fill_preserve()
        ctx.set_source_rgba(0, 0, 0, color[3])
        ctx.stroke()

    def draw_discs(self, rect, unit, ctx):
        for j in xrange(self.rows):
            for i in xrange(self.columns):
                if self.grid[j][i] in self.colors:
                    self.draw_disc((i + 0.5) * unit, (j + 0.5) * unit,
                        self.colors[self.grid[j][i]], unit, ctx)

                if (i, j) in self.highlighted_discs:
                    ctx.set_line_width(unit / 32.0)
                    ctx.set_source_rgba(*self.highlighted_color)
                    ctx.rectangle(j * unit, i * unit, unit,
                        unit)
                    ctx.stroke()

        if self.selected_column is not None:
            discs = [row[self.selected_column] for row in self.grid]

            if -1 not in discs:
                # column is full
                return

            row = self.rows - list(reversed(discs)).index(-1) - 1
            self.draw_disc(
                (self.selected_column + 0.5) * unit,
                (row + 0.5) * unit,
                (0, 0, 0, 0.3), unit, ctx)

    def get_mouse_event_col(self, event):
        unit, x0, y0 = self.get_coordinates(self.get_rect())
        col = (event.x - x0) / unit
        if col <= 0 or col >= self.columns:
            return None
        return int(col)

    def motion_cb(self, event):
        if self.selected_column is None:
            return
        col = self.get_mouse_event_col(event)
        if col is not None and col != self.selected_column:
            self.selected_column = col
            self.output.queue_draw()

    def button_release_cb(self, event):
        if self.selected_column is None:
            return

        self.motion_cb(event)

        col = self.get_mouse_event_col(event)
        self.emit('insert-requested', col)

    def queue_draw(self):
        self.output.queue_draw()

    def get_coordinates(self, rect):
        """Returns tuple (unit size, origin x, origin y) suitable for drawing
        a grid within @rect."""

        if rect.height / float(self.rows) < rect.width / float(self.columns):
            # wide
            unit = rect.height / float(self.rows)
            x0 = rect.x + (rect.width - self.columns * unit) / 2.0
            y0 = rect.y
        else:
            # narrow
            unit = rect.width / float(self.columns)
            x0 = rect.x
            y0 = rect.y + (rect.height - self.rows * unit) / 2.0

        return unit, x0, y0

    def draw(self, rect, ctx):
        """Draw a grid using the cairo context @ctx within the rectangle
        @rect."""

        ctx.save()
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        unit, x0, y0 = self.get_coordinates(rect)
        ctx.translate(x0, y0)
        self.draw_background(rect, unit, ctx)
        self.draw_discs(rect, unit, ctx)
        self.draw_lines(rect, unit, ctx)
        ctx.restore()

    def get_rect(self):
        """Return a subrectangle of the widget's allocation within which to
        draw the grid."""
        rect = self.get_allocation()
        padding = 10
        return gtk.gdk.Rectangle(
            padding, padding,
            rect.width - 2 *  padding, rect.height - 2 * padding)

    def expose_cb(self, widget, event):
        ctx = widget.window.cairo_create()
        rect = self.get_rect()
        # XXX: this clips off some of the outer edge of the grid
        #ctx.rectangle(rect.x, rect.y, rect.width, rect.height)
        #ctx.clip()
        self.draw(rect, ctx)
