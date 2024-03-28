from kivy.config import Config
# Set the keyboard mode to use system keyboard only
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
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from datetime import datetime
from kivy.animation import Animation
from kivy.clock import Clock

import re

class ScheduleApp(App):
    def build(self):
        Window.size = (800, 600)
        self.main_layout = FloatLayout()

        # Set up the background image
        self.bg_image = Image(source='default.jpg', allow_stretch=True, keep_ratio=False)
        self.main_layout.add_widget(self.bg_image)

        # Add TextInput for user to enter their name
        self.user_name_input = TextInput(
                hint_text='Enter your name',
                multiline=False,  # Increased size
                size_hint=(0.21, 0.035),  # Adjusted size
                pos_hint={'right': 0.98, 'top': 0.99}  # Adjusted position
        )
        self.user_name_input.bind(text=self.update_greeting_on_input)
        self.main_layout.add_widget(self.user_name_input)
        






        # Greeting based on time
        self.greeting_label = Label(
            text="",  # Initial text
            font_size='24sp',  # Font size
            size_hint=(0.21, 0.035),  # Size hint
            size=(Window.width, 60),  # Size
            pos_hint={'center_x': 0.84, 'center_y': 0.94}  # Position hint
        )

        # Add the greeting label to the main layout
        self.main_layout.add_widget(self.greeting_label)

        self.update_greeting()

        Clock.schedule_once(self.start_marquee_animation)

        # Add TextInput for user to enter class names
        self.class_names_input = TextInput(hint_text='Enter the names of your classes, separated by commas (e.g., CMPM 15, CSE 16, MATH 21)',
                                           multiline=False, size_hint=(None, None), size=(Window.width * 0.8, 50),
                                           pos_hint={'center_x': 0.5, 'top': 0.95})
        self.main_layout.add_widget(self.class_names_input)

        self.done_button = Button(text='Done', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'top': 0.8})
        self.done_button.bind(on_press=lambda instance: self.display_entered_classes())

        self.main_layout.add_widget(self.done_button)


        # ScrollView for the class inputs and 'Add Another Class' button
        scroll_view = ScrollView(size_hint=(None, None), size=(Window.width * 0.8, Window.height * 0.5), 
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5}, do_scroll_x=False)

        # This BoxLayout contains the class inputs and 'Add Another Class' button
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # Add the initial class inputs
        for _ in range(3):
            self.add_class_input(content_layout)

        # Button to add more class inputs
        add_more_button = Button(text='+ Add Another Class', size_hint_y=None, height=50)
        add_more_button.bind(on_press=lambda instance: self.add_class_input(content_layout))

        content_layout.add_widget(add_more_button)
        scroll_view.add_widget(content_layout)
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
    
    def start_marquee_animation(self, dt):
        # Calculate the distance to move the label for one animation loop
        distance = Window.width + self.greeting_label.texture_size[0]

        # Create the animation to move the label from left to right and then back to left
        anim = Animation(x=distance, duration=10)
        anim += Animation(x=-self.greeting_label.texture_size[0], duration=10)

        # Make the animation loop indefinitely
        anim.repeat = True

        # Start the animation
        anim.start(self.greeting_label)
        
    def update_greeting(self):
        # Extract the name directly from the input
        value = self.user_name_input.text.strip()
        
        # Update greeting based on the time of day
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = "Good Morning"
        elif 12 <= current_hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        if value:
            self.greeting_label.text = f"{greeting}, {value}"
            # Set up for scrolling effect if the label is wider than the window
            if self.greeting_label.texture_size[0] > Window.width:
                self.greeting_label.x = -self.greeting_label.texture_size[-1]  # Start from the left
                # Calculate duration based on the width of the text and the window width
                duration = (self.greeting_label.texture_size[0] + Window.width) / 50
                anim = Animation(x=Window.width, duration=duration)  # Adjust duration as needed
                anim.start(self.greeting_label)
        else:
            # Default text if no name is entered
            self.greeting_label.text = greeting

    def update_greeting_on_input(self, instance, value):
        self.update_greeting()  # Call the main update function without parameters


    


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

        layout.add_widget(class_layout, len(layout.children) - 1)  # Insert above the 'Add Another Class' button

    def show_file_chooser(self, instance):
        chooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg'], size_hint=(1, 1))
        confirm_btn = Button(text='Set Background', size_hint_y=None, height=50)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(chooser)
        layout.add_widget(confirm_btn)
    
        self.popup = Popup(title='Choose a background image', content=layout, size_hint=(0.9, 0.9))

    # Bind the button's on_press to a new method that handles the file selection and popup dismissal
        confirm_btn.bind(on_press=lambda x: self.set_background(chooser.selection))

        self.popup.open()


    def set_background(self, selection):
        if selection:  # Check if the list is not empty
            self.bg_image.source = selection[0]  # Set the first selected file as background
            self.bg_image.reload()  # Reload the image to apply the new source
            self.popup.dismiss()  # Close the popup

    def reset_background(self, instance):
        # Reset the background image to the default
        self.bg_image.source = 'default.jpg'
        self.bg_image.reload()

    def display_entered_classes(self):
        # Clear existing inputs
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(self.add_more_button)  # Re-add the 'Add Another Class' button

        # Get class names entered by the user, split by commas
        entered_classes = self.class_names_input.text.split(',')

        # Create class input for each entered class name
        for class_name in entered_classes:
            # Clean up class name, remove leading/trailing whitespaces
            class_name = class_name.strip()

            # Check if the class name is not empty
            if class_name:
                # Add a new set of class input fields
                self.add_class_input(self.content_layout)
                # Retrieve the last class input added
                last_layout = self.content_layout.children[1]  # Retrieve the last class input added
                last_layout.children[3].text = class_name  # Fill in 'Class Name'
                # Fill other details as 'TBA' or leave them empty
                last_layout.children[2].text = 'TBA'  # Class Type
                last_layout.children[1].text = 'TBA'  # Class Time
                last_layout.children[0].text = 'TBA'  # Class Location


    def parse_schedule(self, schedule_text):
        # Clear existing inputs
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(self.add_more_button)  # Re-add the 'Add Another Class' button

        # Define the regular expression pattern to extract class information
        # Adjusted based on the format you've provided
        class_pattern = re.compile(
            r'(\w+ \d+) - ([\w\s]+)'            # Matches 'Class Code - Class Name'
            r'.*?'                              # Skips irrelevant info
            r'(Lecture|Discussion|Laboratory)'  # Matches 'Class Type'
            r'.*?'                              # Skips to time and location
            r'([MTuWThF]+) ([\d:APM]+ - [\d:APM]+)'  # Matches 'Class Days' and 'Class Times'
            r'.*?'                              # Skips to location
            r'([\w\s&]+)',                      # Matches 'Class Location'
            re.DOTALL)                          # Allows '.' to match across lines

        # Find all matches in the pasted text
        classes = class_pattern.findall(schedule_text)

        # Create class input for each found class
        for class_info in classes:
            class_code, class_name, class_type, class_days, class_times, class_location = class_info
            # Construct full class name
            full_class_name = f"{class_code} - {class_name}".strip()

            # Add a new set of class input fields
            self.add_class_input(self.content_layout)
            # Retrieve the last class input added
            last_layout = self.content_layout.children[1]  # Retrieve the last class input added
            last_layout.children[3].text = full_class_name  # Fill in 'Class Name'
            last_layout.children[2].text = class_type  # Fill in 'Class Type'
            last_layout.children[1].text = f'{class_days} {class_times}'  # Fill in 'Class Time'
            last_layout.children[0].text = class_location  # Fill in 'Class Location'
                


    def show_schedule_prompt(self, instance):
        layout = BoxLayout(orientation='vertical', spacing=10)
        self.schedule_text_input = TextInput(hint_text='Paste your full schedule here', size_hint_y=None, height=300, multiline=True)
        submit_schedule_button = Button(text='Submit Schedule', size_hint_y=None, height=50)
        submit_schedule_button.bind(on_press=self.process_pasted_schedule)

        layout.add_widget(self.schedule_text_input)
        layout.add_widget(submit_schedule_button)

        self.schedule_popup = Popup(title='Paste your schedule', content=layout, size_hint=(0.9, 0.9))
        self.schedule_popup.open()

  
    def process_pasted_schedule(self, instance):
    # Close the schedule popup
        self.schedule_popup.dismiss()

    # Process the schedule text entered by the user
        schedule_text = self.schedule_text_input.text
        self.parse_schedule(schedule_text)



if __name__ == '__main__':
    ScheduleApp().run()
