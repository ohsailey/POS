from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
#from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial
from pos import Pos
import os
import platform
import win32api
from usb import StorageDevice

topic_folder = os.path.dirname(os.path.abspath(__file__)) + '/test/'

class TopicScreen(Screen):
    def __init__(self, **kwargs):
        super(TopicScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Hello, this is my POS.\n'+
    'Please choose your desirable topic')
        layout.add_widget(self.label)
        self.topics = self.get_topics()
        for topic in self.topics:
            topic_btn = Button(text = topic.get_name())
            topic_btn.bind(on_release=partial(self.changer, topic))
            layout.add_widget(topic_btn)
        self.add_widget(layout)
	
    def changer(self, topic, *args):
        global choose_topic
        choose_topic = topic
        module_path = 'test.'+ topic.get_name() + '.acc_fun.acc'
        pkg = __import__(module_path, fromlist=['AccScreen'])
        name = 'acc_screen'
        acc_view = pkg.AccScreen(name=name)
        MyApp().new_screen(acc_view, name)

		
    def get_topics(self):
        topics = pos.get_topics()
        return topics
        
class DownloadScreen(Screen):

    def __init__(self,**kwargs):
        super (DownloadScreen,self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Pluggin your Storage Device And Start",
            font_size='30dp')
        plugin_dev_btn = Button(text="storage device")
        plugin_dev_btn.bind(on_press=self.transfer_data)
        return_btn = Button(text="Return Topic Page")
        return_btn.bind(on_press=self.press_topic_page)
        layout.add_widget(self.label)
        layout.add_widget(plugin_dev_btn)
        layout.add_widget(return_btn)

        self.add_widget(layout)

    def transfer_data(self,*args):
        if storage_device._is_detectable() == True :
            self.label.text = 'Start Downloading\n' + 'Do not remove your storage in the process.'
            global choose_topic
            storage_device.obtain_data(choose_topic.get_data_path())
            Clock.schedule_once(self.show_finish_message, 5)
        else:
            alert_popup = Popup(title='POS Alert',
                content=Label(text='Device is not detected.Inserted it rightly'),
                size_hint=(.5, .5), auto_dismiss=True)
            alert_popup.open()

    def press_topic_page(self, *args):
        self.label.text = 'Pluggin your Storage Device And Start'
        self.manager.current = 'topic_screen'

    def show_finish_message(self, *args):
        self.label.text = 'Download Complete\n'+'\
            Remember to Ejet your Device.\n'+'\
            Returning to Topic Page'
        Clock.schedule_once(self.press_topic_page, 3)

class MyApp(App):
    def build(self):
        return pos_screenmanager
    def new_screen(self, view , name):
        pos_screenmanager.add_widget(view)
        pos_screenmanager.current = name

def init_pos_gui():
    topic_view = TopicScreen(name='topic_screen')
    download_view = DownloadScreen(name='download_screen')
    pos_screenmanager.add_widget(topic_view)
    pos_screenmanager.add_widget(download_view)

if __name__ == '__main__':
    pos_screenmanager = ScreenManager()
    pos = Pos(topic_folder)
    storage_device = StorageDevice()
    init_pos_gui()
    MyApp().run()