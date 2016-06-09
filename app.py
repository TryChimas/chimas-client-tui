import urwid
import requests
import json

from requests.auth import HTTPBasicAuth

host = "http://127.0.0.1:41345"
authdata = ("admin", "abc123")

PADDING_LEFT = 2
PADDING_RIGHT = 2
PADDING_TOP = 1
PADDING_BOTTOM = 1

palette = [
    (None, 'light gray', 'default'),
    ('unselected', 'white', 'default'),
    ('selected', 'black', 'dark green'),
]

class ListButton(urwid.Button):
    def __init__(self, label, on_press=None, user_data=None):
        super(ListButton, self).__init__("", on_press, user_data)
        self._w = urwid.AttrMap(urwid.SelectableIcon([u"\N{BULLET} ", label]), 'unselected', 'selected')

class BoardList(urwid.ListBox):
    def __init__(self, main_window):
        super(BoardList, self).__init__("")

        self.main_window = main_window

        self.load()

    def load(self):

        r = requests.get(host+'/boards', auth=authdata)
        obj = json.loads(r.text)

        mylist = [urwid.Divider()]
        for c in obj['_items']:
            mylist.append(ListButton('Topic {0}'.format(c['title']),on_press=self.main_window.boardlist_callback,user_data=c))

        mylist.append(urwid.Divider())
        self.body = urwid.SimpleFocusListWalker(mylist)

class BoardTopics(urwid.ListBox):
    def __init__(self, main_window, board_id):
        super(BoardTopics, self).__init__("")

        self.main_window = main_window
        #self.board_id = board_id

        import pprint
        pprint.pprint(board_id,width=1)
        self.load(board_id)

    def load(self, board_id):

        r = requests.get(host+'/posts?where={"board_id":"{0}","reply_to_id":"0"}'.format(board_id['title']), auth=authdata)
        obj = json.loads(r.text)

        mylist = [urwid.Divider()]
        for c in obj['_items']:
            mylist.append(ListButton('Topic {0}'.format(c['title']),self.main_window.boardlist_callback,c))
        mylist.append(urwid.Divider())
        self.body = urwid.SimpleFocusListWalker(mylist)

class WindowFrame(urwid.Frame):
    def __init__(self, body=None, header=None, footer=None, focus_part='body'):
        super(WindowFrame, self).__init__("")

        self.f_top_text = urwid.Text('This is header')
        self.header = urwid.Padding(self.f_top_text,left=2,right=2)

        self.f_footer_text = urwid.Text('This is footer')
        self.footer = urwid.Padding(self.f_footer_text,left=2,right=2)

        self.boardlist = BoardList(main_window=self)
        self.set_body(self.boardlist)

    def set_body(self, widget):
        self.body = urwid.Padding(widget, left=2, right=2)

    def boardlist_callback(self, button, user_data):

        self.boardtopics = BoardTopics(self, user_data)

        self.set_body(self.boardtopics)





#content_filler = urwid.Filler(content_padding, top=3, bottom=3)
#l_boards = BoardList()
#content_padding = urwid.Padding(l_boards, left=2, right=2)

#content= urwid.BoxAdapter(content_padding,40)
#w_main = urwid.Frame(content_padding, f_header, f_footer)

#mylist=urwid.SimpleFocusListWalker(['lolz','okay'])
w_main = WindowFrame()

loop=urwid.MainLoop(w_main, palette)

loop.run()
