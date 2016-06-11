import urwid
import requests
import json

from requests.auth import HTTPBasicAuth

host = "http://127.0.0.1:41345"
authdata = ("admin", "abc123")

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

class TopicList(urwid.ListBox):
    def __init__(self, main_window, user_data):
        super(TopicList, self).__init__("")

        self.main_window = main_window
        self.user_data = user_data

        self.load()

    def load(self):

        r = requests.get(host+'/posts?where={"board_id":"' + self.user_data['title'] + '", "reply_to_id":"0"}', auth=authdata)
        obj = json.loads(r.text)

        mylist = [urwid.Divider()]
        for c in obj['_items']:
            mylist.append(
                ListButton('Topic {0}'.format(c['title']), self.main_window.topiclist_callback, c)
            )
        mylist.append(urwid.Divider())
        self.body = urwid.SimpleFocusListWalker(mylist)

class ThreadPosts(urwid.Pile):
    def __init__(self, main_window, user_data, widget_list=[], focus_item=None):

        #super(ThreadPosts, self).__init__(widget_list)
        super(ThreadPosts, self).__init__(widget_list)

        self.main_window = main_window
        self.user_data = user_data

        self.load()

        #super(ThreadPosts, self).__init__(widget_list, focus_item)


    def load(self):

        r = requests.get(host+'/posts?where={"topic_id":"' + self.user_data['id'].__str__() + '"}', auth=authdata)
        obj = json.loads(r.text)

        #mylist = [urwid.Divider()]
        mylist = []
        for c in obj['_items']:
            #mylist.append(
            mawids = urwid.Text(c['title'])
            self.contents.append(
                #('pack', urwid.Text(c['title']))
                #(mawids, ('pack'))
                (mawids, ('pack',None))
                #urwid.Text(c['title'])

                #ListButton('Post: {0}'.format(c['title']), self.main_window.topiclist_callback, c)
                #urwid.LineBox( [
                    #urwid.Text(c['title']),
                    #urwid.Divider(),
                    #urwid.Text(c['post_text'])#]
                #])
            )
        #mylist.append(urwid.Divider())
        #self.body = urwid.SimpleFocusListWalker(mylist)
        #self.widget_list = mylist
        #self.contents.append(mylist)

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

        self.topiclist = TopicList(self, user_data)

        self.set_body(self.topiclist)

    def topiclist_callback(self, button, user_data):

        self.threadposts = ThreadPosts(self, user_data=user_data)

        self.set_body(self.threadposts)
        #myPile = urwid.Pile([('pack'), urwid.Text("oi"), urwid.Text("ei"), urwid.Text("hello buddy")])
        #self.set_body(myPile)

w_main = WindowFrame()
loop = urwid.MainLoop(w_main, palette)
loop.run()
