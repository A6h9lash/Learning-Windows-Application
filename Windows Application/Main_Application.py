import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import openpyxl
from datetime import datetime
import os
import subprocess
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learning App Demo")
        self.root.state('zoomed')

        # Color Palette
        self.primary_color = "#004299"
        self.secondary_color = "#66B2FF"
        self.accent_color = "#FFC107"
        self.background_color = "#F8F8F8"
        self.text_color = "#333333"

        # Set root background color
        self.root.configure(bg=self.background_color)

        # Style configuration
        self.style = ttk.Style(root)
        self.style.configure('TButton',
                             padding=5,
                             relief="raised",
                             background=self.secondary_color,
                             foreground=self.text_color)
        self.style.configure('TLabel',
                             padding=5,
                             font=('Arial', 12),
                             background=self.background_color,
                             foreground=self.text_color)
        self.style.configure('Header.TLabel',
                             font=('Arial', 18, 'bold'),
                             background=self.background_color,
                             foreground=self.primary_color)

        # Load and resize the logo image
        self.logo_path = os.path.join("backend", "Logo.png")
        pil_image = Image.open(self.logo_path)
        pil_image = pil_image.resize((150, 75))  # Resize to 200x200
        self.logo_image = ImageTk.PhotoImage(pil_image)

        self.login_frame = None
        self.welcome_frame = None
        self.learning_frame = None
        self.current_path = "Data"
        self.login_screen()

    def login_screen(self):
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()

        self.login_frame = tk.Frame(self.root, bg=self.background_color)
        self.login_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Top frame for logo and other potential top elements
        top_frame = tk.Frame(self.login_frame, bg=self.background_color)
        top_frame.pack(fill="x")

        logo_label = tk.Label(top_frame, image=self.logo_image, bg=self.background_color)
        logo_label.image = self.logo_image  # Keep a reference to prevent garbage collection
        logo_label.pack(side="left", padx=10, pady=10)

        # Inner frame to hold login form
        inner_frame = tk.Frame(self.login_frame, bg="#ffffff")  # White background
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner_frame, text="Username:", background="#ffffff", foreground=self.text_color).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(inner_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(inner_frame, text="Password:", background="#ffffff", foreground=self.text_color).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(inner_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        login_button = ttk.Button(inner_frame, text="Login", command=self.check_credentials, style='TButton')
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)

        inner_frame.rowconfigure(0, weight=1)
        inner_frame.rowconfigure(1, weight=1)
        inner_frame.rowconfigure(2, weight=1)

    def welcome_screen(self):
        welcomeusername = self.username_entry.get()
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()

        self.welcome_frame = tk.Frame(self.root, bg=self.background_color)
        self.welcome_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Top frame for logo and logout button
        top_frame = tk.Frame(self.welcome_frame, bg=self.background_color)
        top_frame.pack(fill="x")

        logo_label = tk.Label(top_frame, image=self.logo_image, bg=self.background_color)
        logo_label.image = self.logo_image  # Keep a reference to prevent garbage collection
        logo_label.pack(side="left", padx=10, pady=10)

        ttk.Button(top_frame, text="Logout", command=self.login_screen, style='TButton').pack(side="right", padx=10, pady=10)

        # Middle frame for content
        middle_frame = tk.Frame(self.welcome_frame, bg="#ffffff")
        middle_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(middle_frame, text=f"Welcome {welcomeusername}!", style='Header.TLabel').pack(pady=20)
        ttk.Label(middle_frame, text="You are logged in successfully!", style='TLabel').pack(pady=10)
        ttk.Button(middle_frame, text="Continue to Learning App", command=self.learning_screen, style='TButton').pack(pady=20)

    def learning_screen(self):
        # Clear any existing frames
        for widget in self.root.winfo_children():
            widget.destroy()

        self.learning_frame = tk.Frame(self.root, bg=self.background_color)
        self.learning_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Top frame for logo, logout, path display, and back button
        top_frame = tk.Frame(self.learning_frame, bg=self.background_color)
        top_frame.pack(fill="x")

        logo_label = tk.Label(top_frame, image=self.logo_image, bg=self.background_color)
        logo_label.image = self.logo_image  # Keep a reference to prevent garbage collection
        logo_label.pack(side="left", padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="Back", command=self.go_back, state="disabled", style='TButton')
        self.back_button.pack(side="left", padx=10, pady=10)
        self.path_label = ttk.Label(top_frame, text=f"Current Path: {self.current_path}", style='TLabel')
        self.path_label.pack(side="left", padx=10, pady=10)

        ttk.Button(top_frame, text="Logout", command=self.login_screen, style='TButton').pack(side="right", padx=10, pady=10)

        # Middle frame for content
        middle_frame = tk.Frame(self.learning_frame, bg=self.background_color) # Changed background color here
        middle_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.middle_frame = middle_frame
        self.display_folder_contents()

    def display_folder_contents(self):
        # Clear any existing widgets in the middle frame
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        try:
            items = os.listdir(self.current_path)
            for item in items:
                item_path = os.path.join(self.current_path, item)
                if os.path.isfile(item_path):
                    button = ttk.Button(self.middle_frame, text=f"File: {item}", command=lambda path=item_path: self.open_file(path), style='TButton')
                    button.pack(pady=5)
                elif os.path.isdir(item_path):
                    button = ttk.Button(self.middle_frame, text=f"Folder: {item}", command=lambda path=item_path: self.navigate_to_folder(path), style='TButton')
                    button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying folder contents: {e}")

    def open_file(self, file_path):
        try:
            if os.name == 'nt':
                os.startfile(file_path)
            elif os.name == 'posix':
                subprocess.call(('open', file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {e}")

    def navigate_to_folder(self, folder_path):
        self.current_path = folder_path
        self.path_label['text'] = f"Current Path: {self.current_path}"
        if self.current_path != "Data":
            self.back_button['state'] = "normal"
        else:
            self.back_button['state'] = "disabled"
        self.display_folder_contents()

    def go_back(self):
        parent_path = os.path.dirname(self.current_path)
        self.current_path = parent_path
        self.path_label['text'] = f"Current Path: {self.current_path}"
        if self.current_path != "Data":
            self.back_button['state'] = "normal"
        else:
            self.back_button['state'] = "disabled"
        self.display_folder_contents()

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Read credentials from Excel file
        credentials = self.read_credentials_from_excel("Backend/Credentials.xlsx")

        # Validate credentials
        if username in credentials:
            stored_password, valid_till = credentials[username]
            if password == stored_password:
                if valid_till is None or datetime.now() <= valid_till:
                    self.welcome_screen()
                else:
                    messagebox.showerror("Login Failed", "Login credentials expired. Please contact support.")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def read_credentials_from_excel(self, filename):
        """Reads username/password/valid_till from an Excel file."""
        try:
            workbook = openpyxl.load_workbook(filename)
            sheet = workbook.active

            credentials = {}
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] is not None and row[1] is not None:
                    username, password, valid_till = row[0], row[1], row[2] if len(row) > 2 else None

                    if valid_till is not None and not isinstance(valid_till, datetime):
                        try:
                            valid_till = datetime.fromisoformat(valid_till)
                        except ValueError:
                            try:
                                valid_till = datetime.strptime(str(valid_till), "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                try:
                                    valid_till = workbook.epoch + (valid_till - 25569) * 86400
                                    valid_till = datetime.utcfromtimestamp(valid_till)
                                except:
                                  valid_till = None

                    credentials[username] = (password, valid_till)

            return credentials
        except FileNotFoundError:
            messagebox.showerror("Error", "Credentials file not found!")
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Error reading credentials: {e}")
            return {}

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
