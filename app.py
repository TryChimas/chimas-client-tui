import urwid

PADDING_LEFT = 2
PADDING_RIGHT = 2
PADDING_TOP = 1
PADDING_BOTTOM = 1

f_top_text = urwid.Text('This is header')
f_header = urwid.Padding(f_top_text,left=2,right=2)
f_footer_text = urwid.Text('This is footer')
f_footer = urwid.Padding(f_footer_text,left=2,right=2)
f_text = urwid.Text('This is test! Okay')

mylist = [urwid.Divider()]
for c in range(1, 70):
    mylist.append(urwid.AttrMap(urwid.Button('Board {0}'.format(c)),None,focus_map='reversed'))
mylist.append(urwid.Divider())
f_list = urwid.ListBox(urwid.SimpleFocusListWalker(mylist))
content_padding = urwid.Padding(f_list, left=2, right=2)

content_filler = urwid.Filler(content_padding, top=2, bottom=2)

#content= urwid.BoxAdapter(content_padding,40)
w_main = urwid.Frame(content_padding, f_header, f_footer)

#mylist=urwid.SimpleFocusListWalker(['lolz','okay'])



urwid.MainLoop(w_main).run()
