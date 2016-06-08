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
    def __init__(self,label,on_press=None,user_data=None):
        super(ListButton, self).__init__("")
        self._w = urwid.AttrMap(urwid.SelectableIcon([u"\N{BULLET} ", label]), 'unselected', 'selected')

class BoardList(urwid.ListBox):
    def __init__(self):
        super(BoardList, self).__init__("")
        self.load()

    def load(self):

        r = requests.get(host+'/boards', auth=authdata)
        obj = json.loads(r.text)

        mylist = [urwid.Divider()]
        for c in obj['_items']:
            mylist.append(ListButton('Board {0}'.format(c['title'])))
        mylist.append(urwid.Divider())
        self.body = urwid.SimpleFocusListWalker(mylist)

class WindowFrame(urwid.Frame):
    def __init__(self, body=None, header=None, footer=None, focus_part='body'):
        super(WindowFrame, self).__init__("")

        self.f_top_text = urwid.Text('This is header')
        self.header = urwid.Padding(self.f_top_text,left=2,right=2)

        self.f_footer_text = urwid.Text('This is footer')
        self.footer = urwid.Padding(self.f_footer_text,left=2,right=2)

        self.set_body(BoardList())

    def set_body(self, widget):
        self.body = urwid.Padding(widget, left=2, right=2)




#content_filler = urwid.Filler(content_padding, top=3, bottom=3)
l_boards = BoardList()
#content_padding = urwid.Padding(l_boards, left=2, right=2)

#content= urwid.BoxAdapter(content_padding,40)
#w_main = urwid.Frame(content_padding, f_header, f_footer)

#mylist=urwid.SimpleFocusListWalker(['lolz','okay'])
w_main = WindowFrame()

loop=urwid.MainLoop(w_main, palette)

loop.run()
