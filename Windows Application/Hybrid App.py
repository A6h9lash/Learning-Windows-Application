import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.clock import mainthread
from datetime import datetime
import os
import subprocess
import openpyxl

kivy.require('2.0.0')

class LoginApp(App):
    current_path = StringProperty("Data")
    username = StringProperty("")
    password = StringProperty("")
    welcome_username = StringProperty("")

    def build(self):
        Window.clearcolor = (248/255, 248/255, 248/255, 1) #background color
        return self.login_screen()

    def login_screen(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        logo = Image(source='backend/Logo.png', size_hint_x=0.3)
        top_layout.add_widget(logo)
        layout.add_widget(top_layout)

        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        form_layout.add_widget(Label(text="Username:", color=(51/255, 51/255, 51/255, 1)))
        username_input = TextInput(multiline=False, on_text=lambda instance, value: setattr(self, 'username', value))
        form_layout.add_widget(username_input)

        form_layout.add_widget(Label(text="Password:", color=(51/255, 51/255, 51/255, 1)))
        password_input = TextInput(multiline=False, password=True, on_text=lambda instance, value: setattr(self, 'password', value))
        form_layout.add_widget(password_input)

        layout.add_widget(form_layout)

        login_button = Button(text="Login", on_press=self.check_credentials, size_hint_y=None, height=40, background_color=(102/255, 178/255, 1, 1))
        layout.add_widget(login_button)

        return layout

    def welcome_screen(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        logo = Image(source='backend/Logo.png', size_hint_x=0.3)
        top_layout.add_widget(logo)
        logout_button = Button(text="Logout", on_press=lambda x: setattr(self, 'root', self.login_screen()), size_hint_x=0.2, background_color=(102/255, 178/255, 1, 1))
        top_layout.add_widget(logout_button)
        layout.add_widget(top_layout)

        content_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        content_layout.add_widget(Label(text=f"Welcome {self.username}!", font_size='24sp', color=(0, 66/255, 153/255, 1)))
        content_layout.add_widget(Label(text="You are logged in successfully!", color=(51/255, 51/255, 51/255, 1)))
        continue_button = Button(text="Continue to Learning App", on_press=lambda x: setattr(self, 'root', self.learning_screen()), size_hint_y=None, height=40, background_color=(102/255, 178/255, 1, 1))
        content_layout.add_widget(continue_button)
        layout.add_widget(content_layout)

        return layout

    def learning_screen(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        logo = Image(source='backend/Logo.png', size_hint_x=0.3)
        top_layout.add_widget(logo)
        back_button = Button(text="Back", on_press=self.go_back, size_hint_x=0.1, background_color=(102/255, 178/255, 1, 1))
        self.back_button = back_button
        top_layout.add_widget(back_button)
        path_label = Label(text=f"Current Path: {self.current_path}", size_hint_x=0.4)
        self.path_label = path_label
        top_layout.add_widget(path_label)
        logout_button = Button(text="Logout", on_press=lambda x: setattr(self, 'root', self.login_screen()), size_hint_x=0.2, background_color=(102/255, 178/255, 1, 1))
        top_layout.add_widget(logout_button)
        layout.add_widget(top_layout)

        scroll_view = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        scroll_view.add_widget(self.content_layout)
        layout.add_widget(scroll_view)
        self.display_folder_contents()
        return layout

    def display_folder_contents(self):
        self.content_layout.clear_widgets()
        try:
            items = os.listdir(self.current_path)
            for item in items:
                item_path = os.path.join(self.current_path, item)
                if os.path.isfile(item_path):
                    button = Button(text=f"File: {item}", on_press=lambda instance, path=item_path: self.open_file(path), size_hint_y=None, height=40, background_color=(102/255, 178/255, 1, 1))
                    self.content_layout.add_widget(button)
                elif os.path.isdir(item_path):
                    button = Button(text=f"Folder: {item}", on_press=lambda instance, path=item_path: self.navigate_to_folder(path), size_hint_y=None, height=40, background_color=(102/255, 178/255, 1, 1))
                    self.content_layout.add_widget(button)
        except Exception as e:
            self.show_popup("Error", f"Error displaying folder contents: {e}")

    def open_file(self, file_path):
        try:
            if platform == 'win':
                os.startfile(file_path)
            elif platform == 'linux' or platform == 'macosx':
                subprocess.call(('open', file_path))
            elif platform == 'android':
                subprocess.call(('xdg-open', file_path)) #try this or find android specific method.
        except Exception as e:
            self.show_popup("Error", f"Error opening file: {e}")

    def navigate_to_folder(self, folder_path):
        self.current_path = folder_path
        self.path_label.text = f"Current Path: {self.current_path}"
        self.back_button.disabled = (self.current_path == "Data")
        self.display_folder_contents()

    def go_back(self, instance):
        parent_path
