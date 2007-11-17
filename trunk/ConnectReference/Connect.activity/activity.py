import logging
from gettext import gettext as _

import dbus
import gtk
import hippo
import telepathy
import telepathy.client

from sugar.activity.activity import Activity, ActivityToolbox
from sugar.presence import presenceservice
import sugar.logger

import gridwidget
from game import ConnectGame, SERVICE
from sugar.presence.tubeconn import TubeConnection
from buddiespanel import BuddiesPanel
from infopanel import InfoPanel


logger = logging.getLogger('connect-activity')


class ConnectActivity(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        logger.debug('Starting Connect activity...')

        self.set_title(_('Connect Activity'))

        self.grid = gridwidget.GridWidget()

        self.buddies_panel = BuddiesPanel()

        self.info_panel = InfoPanel()

        vbox = hippo.CanvasBox(spacing=4,
            orientation=hippo.ORIENTATION_VERTICAL)

        hbox = hippo.CanvasBox(spacing=4,
            orientation=hippo.ORIENTATION_HORIZONTAL)

        hbox.append(self.buddies_panel)
        hbox.append(hippo.CanvasWidget(widget=self.grid), hippo.PACK_EXPAND)
        
        vbox.append(hbox, hippo.PACK_EXPAND)
        vbox.append(self.info_panel, hippo.PACK_END)

        canvas = hippo.Canvas()
        canvas.set_root(vbox)
        self.set_canvas(canvas)
        self.show_all()

        toolbox = ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        self.pservice = presenceservice.get_instance()
        owner = self.pservice.get_owner()
        self.owner = owner

        # This displays the buddies_panel even if we fail to connect:
        self.buddies_panel.add_watcher(owner)
        self.info_panel.show(_('To play, share or invite someone.'))

        try:
            name, path = self.pservice.get_preferred_connection()
            self.tp_conn_name = name
            self.tp_conn_path = path
            self.conn = telepathy.client.Connection(name, path)
        except TypeError:
            self.info_panel.show(_('Offline'))
        self.initiating = None

        self.game = None

        self.connect('shared', self._shared_cb)

        if self._shared_activity:
            # we are joining the activity
            self.buddies_panel.add_watcher(owner)
            self.connect('joined', self._joined_cb)
            self._shared_activity.connect('buddy-joined', self._buddy_joined_cb)
            self._shared_activity.connect('buddy-left', self._buddy_left_cb)
            if self.get_shared():
                # oh, OK, we've already joined
                self._joined_cb()
        else:
            # we are creating the activity
            self.buddies_panel.remove_watcher(owner)
            self.buddies_panel.add_player(owner)
            #self.buddies_panel.set_is_playing(owner)
            #self.buddies_panel.set_count(owner, 69)

        self.connect('key-press-event', self.key_press_cb)

    def _get_buddy(self, cs_handle):
        """Get a Buddy from a channel specific handle."""
        logger.debug('Trying to find owner of handle %u...', cs_handle)
        group = self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP]
        my_csh = group.GetSelfHandle()
        logger.debug('My handle in that group is %u', my_csh)
        if my_csh == cs_handle:
            handle = self.conn.GetSelfHandle()
            logger.debug('CS handle %u belongs to me, %u', cs_handle, handle)
        elif group.GetGroupFlags() & telepathy.CHANNEL_GROUP_FLAG_CHANNEL_SPECIFIC_HANDLES:
            handle = group.GetHandleOwners([cs_handle])[0]
            logger.debug('CS handle %u belongs to %u', cs_handle, handle)
        else:
            handle = cs_handle
            logger.debug('non-CS handle %u belongs to itself', handle)

            # XXX: deal with failure to get the handle owner
            assert handle != 0

        # XXX: we're assuming that we have Buddy objects for all contacts -
        # this might break when the server becomes scalable.
        return self.pservice.get_buddy_by_telepathy_handle(self.tp_conn_name,
                self.tp_conn_path, handle)

    def key_press_cb(self, widget, event):
        logger.debug('Keypress: %r, %r', widget, event)
        if event.keyval in (gtk.keysyms.Escape, gtk.keysyms.q):
            gtk.main_quit()

        if self.game is not None:
            self.game.key_press_event(widget, event)

    def _shared_cb(self, activity):
        logger.debug('My Connect activity was shared')
        self.initiating = True
        self._setup()

        for buddy in self._shared_activity.get_joined_buddies():
            self.buddies_panel.add_watcher(buddy)

        self._shared_activity.connect('buddy-joined', self._buddy_joined_cb)
        self._shared_activity.connect('buddy-left', self._buddy_left_cb)

        logger.debug('This is my activity: making a tube...')
        id = self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].OfferDBusTube(
            SERVICE, {})
        self.info_panel.show(_('Waiting for another player to join.'))

    # FIXME: presence service should be tubes-aware and give us more help
    # with this
    def _setup(self):
        if self._shared_activity is None:
            logger.error('Failed to share or join activity')
            return

        bus_name, conn_path, channel_paths = self._shared_activity.get_channels()

        # Work out what our room is called and whether we have Tubes already
        room = None
        tubes_chan = None
        text_chan = None
        for channel_path in channel_paths:
            channel = telepathy.client.Channel(bus_name, channel_path)
            htype, handle = channel.GetHandle()
            if htype == telepathy.HANDLE_TYPE_ROOM:
                logger.debug('Found our room: it has handle#%d "%s"',
                    handle, self.conn.InspectHandles(htype, [handle])[0])
                room = handle
                ctype = channel.GetChannelType()
                if ctype == telepathy.CHANNEL_TYPE_TUBES:
                    logger.debug('Found our Tubes channel at %s', channel_path)
                    tubes_chan = channel
                elif ctype == telepathy.CHANNEL_TYPE_TEXT:
                    logger.debug('Found our Text channel at %s', channel_path)
                    text_chan = channel

        if room is None:
            logger.error("Presence service didn't create a room")
            return
        if text_chan is None:
            logger.error("Presence service didn't create a text channel")
            return

        # Make sure we have a Tubes channel - PS doesn't yet provide one
        if tubes_chan is None:
            logger.debug("Didn't find our Tubes channel, requesting one...")
            tubes_chan = self.conn.request_channel(telepathy.CHANNEL_TYPE_TUBES,
                telepathy.HANDLE_TYPE_ROOM, room, True)

        self.tubes_chan = tubes_chan
        self.text_chan = text_chan

        tubes_chan[telepathy.CHANNEL_TYPE_TUBES].connect_to_signal('NewTube',
            self._new_tube_cb)

    def _list_tubes_reply_cb(self, tubes):
        for tube_info in tubes:
            self._new_tube_cb(*tube_info)

    def _list_tubes_error_cb(self, e):
        logger.error('ListTubes() failed: %s', e)

    def _joined_cb(self, activity):
        if self.game is not None:
            return

        if not self._shared_activity:
            return

        for buddy in self._shared_activity.get_joined_buddies():
            self.buddies_panel.add_watcher(buddy)

        logger.debug('Joined an existing Connect game')
        self.info_panel.show(_('Joined a game. Waiting for my turn...'))
        self.initiating = False
        self._setup()

        logger.debug('This is not my activity: waiting for a tube...')
        self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].ListTubes(
            reply_handler=self._list_tubes_reply_cb,
            error_handler=self._list_tubes_error_cb)

    def _new_tube_cb(self, id, initiator, type, service, params, state):
        logger.debug('New tube: ID=%d initator=%d type=%d service=%s '
                     'params=%r state=%d', id, initiator, type, service,
                     params, state)

        if (self.game is None and type == telepathy.TUBE_TYPE_DBUS and
            service == SERVICE):
            if state == telepathy.TUBE_STATE_LOCAL_PENDING:
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES].AcceptDBusTube(id)

            tube_conn = TubeConnection(self.conn,
                self.tubes_chan[telepathy.CHANNEL_TYPE_TUBES],
                id, group_iface=self.text_chan[telepathy.CHANNEL_INTERFACE_GROUP])
            self.game = ConnectGame(tube_conn, self.grid, self.initiating,
                self.buddies_panel, self.info_panel, self.owner,
                self._get_buddy, self)

    def _buddy_joined_cb (self, activity, buddy):
        logger.debug("buddy joined")
        self.buddies_panel.add_watcher(buddy)

    def _buddy_left_cb (self,  activity, buddy):
        logger.debug("buddy left")
        self.buddies_panel.remove_watcher(buddy)
