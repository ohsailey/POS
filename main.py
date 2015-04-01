from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from functools import partial
from pos import Pos
import os


#my_screenmanager = ScreenManager()

class TopicScreen(Screen):
    def __init__(self, **kwargs):
        super(TopicScreen, self).__init__(**kwargs)
        self.cols = 2
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Hello, this is my POS')
        layout.add_widget(self.label)
        self.topics = self.get_topics()
        for topic in self.topics:
            topic_btn = Button(text = topic.get_name())
            #topic_btn.bind(on_release=self.changer(topic.get_name()))
            topic_btn.bind(on_release=partial(self.changer, topic.get_name()))
            layout.add_widget(topic_btn)
        self.add_widget(layout)
	
    def changer(self, topic_name, *args):
        #self.manager.current = 'acc_screen'
        module_path = 'test.'+ topic_name + '.acc_fun.acc'
        print module_path
        pkg = __import__(module_path, fromlist=['AccScreen'])
        name = 'acc_screen'
        acc_view = pkg.AccScreen(name=name)
        MyApp().new_screen(acc_view, name)

        #start_accountability = pkg.start_accountability
        #vaildation = start_accountability()
        #if vaildation:		
            #self.manager.current = 'download_screen'
        #self.label.text = 'you have a wrong vaildation'
        #
        #self.cols = 2
        #self.row = 2
        #self.add_widget(Label(text='User Name'))
        #self.username = TextInput(multiline=False)
        #self.add_widget(self.username)
        #self.add_widget(Label(text='password'))
        #self.password = TextInput(password=True, multiline=False)
        #self.add_widget(self.password)
        #self.hello = Button(text="hello")
        #self.hello.bind(on_press=self.auth)
        #self.add_widget(self.hello)
		
    def get_topics(self):
        topic_folder = os.path.dirname(os.path.abspath(__file__)) + '/test/'
        test_pos = Pos(topic_folder)
        topics = test_pos.get_topics()
        return topics
		
'''class AccScreen(Screen):
    def __init__(self, **kwargs):
        super(AccScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        title = Label(text='Verify your identification')
        phone_label = Label(text='Phone Number')
        self.phone_input = TextInput(multiline=False)
        submit_btn = Button(text="Submit",size_hint_y=None, size_y=100)
        submit_btn.bind(on_press=self.vaildate)
        return_btn = Button(text="Return",size_hint_y=None, size_y=100)
        return_btn.bind(on_press=self.back)
        layout.add_widget(title)
        layout.add_widget(phone_label)
        layout.add_widget(self.phone_input)
        layout.add_widget(submit_btn)
        layout.add_widget(return_btn)
        self.add_widget(layout)

    def vaildate(self, *args):
        if self.phone_input.text == '0988252130':
            print True
        else:
            print False

    def back(self, *args):
        self.phone_input.text = ""
        self.manager.current = "topic_screen"'''

class DownloadScreen(Screen):

    def __init__(self,**kwargs):
        super (DownloadScreen,self).__init__(**kwargs)

        my_box1 = BoxLayout(orientation='vertical')
        my_label1 = Label(text="start downloading, use one of interface you like",font_size='24dp')
        my_button1 = Button(text="Bluetooth",size_hint_y=None, size_y=100)
        my_button1.bind(on_press=self.bluetooth)
        my_button2 = Button(text="Topic Page",size_hint_y=None, size_y=100)
        my_button2.bind(on_press=self.changer)
        my_box1.add_widget(my_label1)
        my_box1.add_widget(my_button1)
        my_box1.add_widget(my_button2)
        self.add_widget(my_box1)

    def changer(self,*args):
        self.manager.current = 'topic_screen'

    def bluetooth(self,*args):
        pass
        
class MyScreenManager(ScreenManager):
    def new_screen(self, view , name):
        #name = str(time.time())
        self.add_widget(view)
        self.current = name


#root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
'''MyScreenManager:
    TopicScreen:
    DownloadScreen:

<TopicScreen>:
    name: 'topic_screen'

<DownloadScreen>:
    name: 'download_screen'
)'''


my_screenmanager = ScreenManager()
topic_view = TopicScreen(name='topic_screen')
download_view = DownloadScreen(name='download_screen')
my_screenmanager.add_widget(topic_view)
my_screenmanager.add_widget(download_view)

class MyApp(App):
    def build(self):
        
        return my_screenmanager

    def new_screen(self, view , name):
        #name = str(time.time())
        my_screenmanager.add_widget(view)
        my_screenmanager.current = name

        #return root_widget


if __name__ == '__main__':
    MyApp().run()