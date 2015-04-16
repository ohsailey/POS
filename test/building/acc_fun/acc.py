import kivykivy.require('1.8.0')from kivy.app import Appfrom kivy.uix.screenmanager import Screen from kivy.uix.gridlayout import GridLayoutfrom kivy.uix.boxlayout import BoxLayoutfrom kivy.uix.label import Labelfrom kivy.uix.textinput import TextInputfrom kivy.uix.button import Buttonfrom kivy.properties import ObjectPropertyclass AccScreen(Screen):    def __init__(self, **kwargs):        super(AccScreen, self).__init__(**kwargs)        layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)        layout.add_widget(Label(text='Phone Number'))        self.phone_input = TextInput(multiline=False, password=True)        layout.add_widget(self.phone_input)        self.submit_btn = Button(text="submit")        self.submit_btn.bind(on_press=self.vaildate)        self.previous_btn = Button(text="Return")        self.previous_btn.bind(on_press=self.previous)        self.msg = Label(text='')        layout.add_widget(self.submit_btn)        layout.add_widget(self.previous_btn)        layout.add_widget(self.msg)        self.add_widget(layout)    def vaildate(self, *args):        if self.phone_input.text == '0':            self.manager.current = 'download_screen'            self.phone_input.text = ''            self.msg.text = ''        else:            self.msg.text = 'wrong vaildation!!'    def previous(self, *args):        self.manager.current = 'topic_screen'        self.phone_input.text = ''        self.msg.text = ''