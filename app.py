import urwid
import requests
import json

from requests.auth import HTTPBasicAuth

host = "http://127.0.0.1:41345"
authdata = ("admin","abc123")

class ListButton(urwid.Button):
    def __init__(self,label,on_press=None,user_data=None):
        super(ListButton, self).__init__("")
        #urwid.connect_signal(self, "click", callback)
#        self._w = urwid.AttrMap(urwid.SelectableIcon([u"\N{BULLET} ", label]), None, 'unselected')
        self._w = urwid.AttrMap(urwid.SelectableIcon([u"\N{BULLET} ", label]),'unselected', 'selected')

palette =[
(None, 'light gray', 'default'),
('unselected', 'white', 'default'),
('selected', 'black', 'dark green'),
]
PADDING_LEFT = 2
PADDING_RIGHT = 2
PADDING_TOP = 1
PADDING_BOTTOM = 1

f_top_text = urwid.Text('This is header')
f_header = urwid.Padding(f_top_text,left=2,right=2)
f_footer_text = urwid.Text('This is footer')
f_footer = urwid.Padding(f_footer_text,left=2,right=2)
f_text = urwid.Text('This is test! Okay')

r = requests.get(host+'/boards', auth=authdata)
obj = json.loads(r.text)

mylist = [urwid.Divider()]
for c in obj['_items']:
    #mylist.append(urwid.AttrMap(ListButton('Board {0}'.format(c)), 'selected', 'unselected'))
    #mylist.append(urwid.AttrMap(ListButton('Board {0}'.format(c)),None,focus_map='selected'))
    mylist.append(ListButton('Board {0}'.format(c['title'])))
mylist.append(urwid.Divider())
f_list = urwid.ListBox(urwid.SimpleFocusListWalker(mylist))
content_padding = urwid.Padding(f_list, left=2, right=2)

content_filler = urwid.Filler(content_padding, top=3, bottom=3)

#content= urwid.BoxAdapter(content_padding,40)
w_main = urwid.Frame(content_padding, f_header, f_footer)

#mylist=urwid.SimpleFocusListWalker(['lolz','okay'])



urwid.MainLoop(w_main, palette).run()
