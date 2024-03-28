from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import re
from kivy.uix.filechooser import FileChooserListView


class ScheduleApp(App):
    def build(self):
        Window.size = (800, 600)
        self.main_layout = FloatLayout()

        # Set up the background image
        self.bg_image = Image(source='default.jpg', allow_stretch=True, keep_ratio=False)
        self.main_layout.add_widget(self.bg_image)

        # Add TextInput for user to enter class names
        self.class_names_input = TextInput(hint_text='Enter the names of your classes, separated by commas (e.g., CMPM 15, CSE 16, MATH 21)',
                                           multiline=False, size_hint=(None, None), size=(Window.width * 0.8, 50),
                                           pos_hint={'center_x': 0.5, 'top': 0.95})
        self.main_layout.add_widget(self.class_names_input)

        # Done button for user to submit their manually entered classes
        self.done_button = Button(text='Done', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'top': 0.7})
        self.done_button.bind(on_press=self.display_entered_classes)
        self.main_layout.add_widget(self.done_button)

        # ScrollView for the class inputs
        scroll_view = ScrollView(size_hint=(None, None), size=(Window.width * 0.8, Window.height * 0.5), 
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        # Button to add more class inputs dynamically
        self.add_more_button = Button(text='+ Add Another Class', size_hint_y=None, height=50)
        self.add_more_button.bind(on_press=lambda instance: self.add_class_input(self.content_layout))

        self.content_layout.add_widget(self.add_more_button)
        scroll_view.add_widget(self.content_layout)
        self.main_layout.add_widget(scroll_view)

        # Set background button
        set_bg_button = Button(text='Set Background', size_hint=(None, None), size=(150, 50), pos_hint={'x': 0, 'y': 0})
        set_bg_button.bind(on_press=self.show_file_chooser)
        self.main_layout.add_widget(set_bg_button)

        # Reset background button
        reset_bg_button = Button(text='Reset Background', size_hint=(None, None), size=(150, 50), pos_hint={'right': 1, 'y': 0})
        reset_bg_button.bind(on_press=self.reset_background)
        self.main_layout.add_widget(reset_bg_button)

        return self.main_layout

    def add_class_input(self, layout, instance=None):
        class_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        class_name_input = TextInput(hint_text='Class Name', size_hint_x=None, width=180)
        class_type_input = TextInput(hint_text='Class Type', size_hint_x=None, width=180)
        class_time_input = TextInput(hint_text='Class Time', size_hint_x=None, width=180)
        class_location_input = TextInput(hint_text='Class Location', size_hint_x=None, width=180)

        class_layout.add_widget(class_name_input)
        class_layout.add_widget(class_type_input)
        class_layout.add_widget(class_time_input)
        class_layout.add_widget(class_location_input)

        layout.add_widget(class_layout, len(layout.children))  # Insert at the end

    def display_entered_classes(self, *args):
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(self.add_more_button)  # Re-add the 'Add Another Class' button

        entered_classes = self.class_names_input.text.split(',')
        for class_name in entered_classes:
            class_name = class_name.strip()
            if class_name:
                self.add_class_input(self.content_layout)
                last_layout = self.content_layout.children[-2]  # Retrieve the second last class input added (first is the add button)
                last_layout.children[3].text = class_name
                last_layout.children[2].text = 'TBA'  # Class Type
                last_layout.children[1].text = 'TBA'  # Class Time
                last_layout.children[0].text = 'TBA'  # Class Location

    def show_file_chooser(self, instance):
        layout = BoxLayout(orientation='vertical', spacing=10)
        # Create a FileChooserListView widget
        filechooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg'], size_hint_y=None, height=400)
        # Button to confirm the background selection
        select_button = Button(text='Select Background', size_hint_y=None, height=50)
        select_button.bind(on_press=lambda x: self.set_background(filechooser.selection))

        # Add the filechooser and button to the layout
        layout.add_widget(filechooser)
        layout.add_widget(select_button)

        # Create a popup with the layout
        self.filechooser_popup = Popup(title='Choose a new background', content=layout, size_hint=(0.9, 0.9))
        self.filechooser_popup.open()

    def set_background(self, selection):
        # Check if any file is selected
        if selection:  # selection is a list of selected files
            new_background = selection[0]  # Take the first selected file
            self.bg_image.source = new_background  # Set new background image
            self.bg_image.reload()  # Reload the image
            self.filechooser_popup.dismiss()  # Close the popup






if __name__ == '__main__':
    ScheduleApp().run()
