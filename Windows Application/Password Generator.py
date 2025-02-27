from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.widget import Widget
import pandas as pd
import random
import string
from datetime import datetime, timedelta

class CredentialGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super(CredentialGenerator, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.app_title = "Password Generator for the learning app"

        # Main layout to hold title/logo and the rest of the content
        main_layout = BoxLayout(orientation='vertical')

        # Top layout for logo and title
        top_layout = self.create_top_layout()
        main_layout.add_widget(top_layout)

        # Username input field
        username_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        username_box.add_widget(Widget(size_hint_x=0.2))
        self.username_input = TextInput(hint_text='Enter your username', size_hint_x=0.6, multiline=False)
        username_box.add_widget(self.username_input)
        username_box.add_widget(Widget(size_hint_x=0.2))
        main_layout.add_widget(username_box)

        # Button to generate and save credentials
        button_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_box.add_widget(Widget(size_hint_x=0.2))
        generate_button = Button(text='Generate and Save Credentials', size_hint_x=0.6)
        generate_button.bind(on_press=self.generate_and_save_credentials)
        button_box.add_widget(generate_button)
        button_box.add_widget(Widget(size_hint_x=0.2))
        main_layout.add_widget(button_box)

        # Button to view credentials
        self.view_button = Button(text='Click here to view your credentials', size_hint_y=None, height=40)
        self.view_button.bind(on_press=self.view_credentials)

        # Button to download credentials as text file
        self.download_button = Button(text='Download Credentials as Text File', size_hint_y=None, height=40)
        self.download_button.bind(on_press=self.download_credentials)

        # Label to display generated password
        self.password_label = Label(text='', size_hint_y=None, height=40)
        main_layout.add_widget(self.password_label)

        # Label to display valid till date
        self.valid_till_label = Label(text='', size_hint_y=None, height=40)
        main_layout.add_widget(self.valid_till_label)

        main_layout.add_widget(Widget())  # Add a spacer to push content to the top
        self.add_widget(main_layout)

    def create_top_layout(self):
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=150)
        logo = Image(source='Backend/Logo.jpg', size_hint=(None, None), size=(150, 150))
        top_layout.add_widget(logo)

        # Title Label in the Middle
        title_label = Label(text=self.app_title, color=(51 / 255, 51 / 255, 51 / 255, 1), font_size=24,
                            halign='center', valign='middle', size_hint_x=0.6)
        top_layout.add_widget(title_label)

        # Spacer to push content to the right
        top_layout.add_widget(Widget())
        return top_layout

    def generate_random_code(self, length):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    def get_valid_till_date(self):
        return datetime.now() + timedelta(days=2)

    def generate_and_save_credentials(self, instance):
        username = self.username_input.text
        if not username:
            self.show_popup("Error", "Please enter a username.")
            return

        try:
            df_existing = pd.read_excel('Backend/Credentials.xlsx')
            if 'Valid Till' in df_existing.columns:
                df_existing = df_existing.rename(columns={'Valid Till': 'Valid till'})

            if username in df_existing['Username'].values:
                # User exists, check if the validity has expired
                user_data = df_existing[df_existing['Username'] == username]
                valid_till = user_data['Valid till'].iloc[0]

                # Check if valid_till is already a datetime object
                if isinstance(valid_till, datetime):
                    valid_till_datetime = valid_till
                else:
                    try:
                        valid_till_datetime = datetime.strptime(valid_till, '%d-%m-%Y %H:%M:%S')
                    except ValueError:
                        self.show_popup("Error", "Invalid date format in Excel file.")
                        return

                if valid_till_datetime <= datetime.now():
                    # Validity expired, show popup to extend
                    self.show_extend_popup(username, df_existing)
                else:
                    # Validity not expired, allow to view credentials
                    self.show_view_popup(username)
                return

        except FileNotFoundError:
            pass

        # Generate new credentials
        code_length = random.randint(8, 10)
        password = self.generate_random_code(code_length)
        valid_till = self.get_valid_till_date()
        valid_till_formatted = valid_till.strftime('%d-%m-%Y %H:%M:%S')

        # Update labels
        self.password_label.text = f"Generated Password: {password}"
        self.valid_till_label.text = f"Valid till: {valid_till_formatted}"

        # Create new user data
        new_user = {
            "Username": [username],
            "Password": [password],
            "Valid till": [valid_till_formatted]
        }

        # Convert the dictionary into DataFrame
        df_new_user = pd.DataFrame(new_user)

        try:
            # Load existing Excel file
            df_existing = pd.read_excel('Backend/Credentials.xlsx')
            if 'Valid Till' in df_existing.columns:
                df_existing = df_existing.rename(columns={'Valid Till': 'Valid till'})
            # Ensure date format consistency
            df_existing['Valid till'] = pd.to_datetime(df_existing['Valid till']).dt.strftime('%d-%m-%Y %H:%M:%S')

            # Append the new user to the existing DataFrame
            df_combined = pd.concat([df_existing, df_new_user], ignore_index=True)

            # Save the combined DataFrame back to the Excel file
            df_combined.to_excel('Backend/Credentials.xlsx', index=False)
            self.show_popup("Success", "Credentials saved successfully.")
        except FileNotFoundError:
            # If the file does not exist, create a new one
            df_new_user.to_excel('Backend/Credentials.xlsx', index=False)
            self.show_popup("Success", "File created and credentials saved successfully.")
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {e}")

    def show_extend_popup(self, username, df_existing):
        """Show popup to extend validity."""
        content = BoxLayout(orientation='vertical')

        extend_2_days_button = Button(text='Extend by 2 days')
        extend_4_days_button = Button(text='Extend by 4 days')

        content.add_widget(Label(text='Validity expired. Extend by:'))
        content.add_widget(extend_2_days_button)
        content.add_widget(extend_4_days_button)

        popup = Popup(title="Extend Validity", content=content, size_hint=(None, None), size=(400, 200))

        extend_2_days_button.bind(on_press=lambda x: self.extend_validity(username, df_existing, 2, popup))
        extend_4_days_button.bind(on_press=lambda x: self.extend_validity(username, df_existing, 4, popup))

        popup.open()

    def extend_validity(self, username, df_existing, days, popup):
        """Extend the validity and save to Excel."""
        try:
            # Calculate new valid_till date
            new_valid_till = datetime.now() + timedelta(days=days)
            new_valid_till_formatted = new_valid_till.strftime('%d-%m-%Y %H:%M:%S')

            # Update the DataFrame
            df_existing.loc[df_existing['Username'] == username, 'Valid till'] = new_valid_till_formatted

            # Save the updated DataFrame to Excel
            df_existing.to_excel('Backend/Credentials.xlsx', index=False)
            self.show_popup("Success", f"Validity extended by {days} days.")
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {e}")
        finally:
            popup.dismiss()

    def show_view_popup(self, username):
        """Show popup with credentials."""
        try:
            df_existing = pd.read_excel('Backend/Credentials.xlsx')
            if 'Valid Till' in df_existing.columns:
                df_existing = df_existing.rename(columns={'Valid Till': 'Valid till'})
            user_data = df_existing.loc[df_existing['Username'] == username]
            if user_data.empty:
                self.show_popup("Error", "User not found.")
                return
            credentials = f"Username: {user_data['Username'].values[0]}\nPassword: {user_data['Password'].values[0]}\nValid till: {user_data['Valid till'].values[0]}"
            self.show_popup("Credentials", credentials)
        except FileNotFoundError:
            self.show_popup("Error", "No credentials file found.")
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {e}")

    def view_credentials(self, instance):
        username = self.username_input.text
        if not username:
            self.show_popup("Error", "Please enter a username.")
            return

        try:
            df_existing = pd.read_excel('Backend/Credentials.xlsx')
            if 'Valid Till' in df_existing.columns:
                df_existing = df_existing.rename(columns={'Valid Till': 'Valid till'})
            user_data = df_existing.loc[df_existing['Username'] == username]
            if user_data.empty:
                self.show_popup("Error", "User not found.")
                return
            credentials = f"Username: {user_data['Username'].values[0]}\nPassword: {user_data['Password'].values[0]}\nValid till: {user_data['Valid till'].values[0]}"
            self.show_popup("Credentials", credentials)
        except FileNotFoundError:
            self.show_popup("Error", "No credentials file found.")
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {e}")

    def download_credentials(self, instance):
        username = self.username_input.text
        if not username:
            self.show_popup("Error", "Please enter a username.")
            return

        try:
            df_existing = pd.read_excel('Backend/Credentials.xlsx')
            if 'Valid Till' in df_existing.columns:
                df_existing = df_existing.rename(columns={'Valid Till': 'Valid till'})
            user_data = df_existing.loc[df_existing['Username'] == username]
            if user_data.empty:
                self.show_popup("Error", "User not found.")
                return
            credentials = f"Username: {user_data['Username'].values[0]}\nPassword: {user_data['Password'].values[0]}\nValid till: {user_data['Valid till'].values[0]}"
            with open(f"{username}_credentials.txt", 'w') as file:
                file.write(credentials)
            self.show_popup("Success", "Credentials saved as text file.")
        except FileNotFoundError:
            self.show_popup("Error", "No credentials file found.")
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {e}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 100))
        popup.open()

class CredentialApp(App):
    def build(self):
        return CredentialGenerator()

if __name__ == "__main__":
    CredentialApp().run()
