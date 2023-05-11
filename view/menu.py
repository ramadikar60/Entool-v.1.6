import customtkinter as ctk
# from config.database import collection
import time
from view.encrypt_file import Form_Encrpyt_File
from view.decrypt_file import Form_Decrpyt_File
from view.encrypt_folder import Form_Encrpyt_Folder
from view.decrypt_folder import Form_Decrpyt_Folder
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("750x300")
        self.title("Entool")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=0)  # sidebar column
        self.grid_columnconfigure(1, weight=1)  # content column

        self.sidebar = Sidebar(master=self, width=150)  # Set sidebar width here
        self.sidebar.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.content_area = ctk.CTkFrame(self, fg_color="white", width=600)  # Set content area width here
        self.content_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # username = collection.find_one()
        # user = username['username']
        # self.welcome_label = ctk.CTkLabel(self.content_area, text="Welcome {}".format(user), text_color="black", font=("Arial", 24))
        # self.welcome_label.pack(pady=60)

        self.my_image = ctk.CTkImage(light_image=Image.open("img/entool.jpeg"),
                                  dark_image=Image.open("img/entool.jpeg"),
                                  size=(150, 150))
            

        self.welcome_label = ctk.CTkLabel(self.content_area, text="Welcome", text_color="black", font=("Arial", 24))
        self.welcome_label.pack(padx=0.5, pady=20, anchor="center")

        self.image = ctk.CTkLabel(self.content_area, text="", image=self.my_image)
        self.image.pack(padx=0.5, pady=10, anchor="center")

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg_color="#66004d")

        self.button1 = ctk.CTkButton(self, text="Encrypt File", fg_color=("#ff1a8c"), hover_color="#ff80aa", command=self.encrypt_file)
        self.button1.pack(fill=ctk.BOTH, padx=10, pady=8)

        self.button2 = ctk.CTkButton(self, text="Decrypt File", fg_color=("#ff1a8c"), hover_color="#ff80aa", command=self.decrypt_file)
        self.button2.pack(fill=ctk.BOTH, padx=10, pady=8)

        self.button3 = ctk.CTkButton(self, text="Encrypt Folder", fg_color=("#ff1a8c"), hover_color="#ff80aa", command=self.encrypt_folder)
        self.button3.pack(fill=ctk.BOTH, padx=10, pady=8)

        self.button3 = ctk.CTkButton(self, text="Decrpyt Folder", fg_color=("#ff1a8c"), hover_color="#ff80aa", command=self.decrypt_folder)
        self.button3.pack(fill=ctk.BOTH, padx=10, pady=8)

        self.label = ctk.CTkLabel(self, text="Powered By \n RAMA DIKA RAMADHAN", font=("Arial", 14), text_color="red")
        self.label.pack(fill=ctk.BOTH, padx=10, pady=8)

        self.clock_label = ctk.CTkLabel(self, font=("Arial", 9), text_color="white")
        self.clock_label.pack(fill=ctk.BOTH, padx=10, pady=10)

        self.update_clock()

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%d/%m/%Y')
        datetime_str = f"{current_time} {current_date}"
        self.clock_label.configure(text=datetime_str)
        self.clock_label.after(1000, self.update_clock)

    def encrypt_file(self):
        self.master.content_area.destroy()  # Clear existing content
        self.master.content_area = Form_Encrpyt_File(self.master)  # Create a new form
        self.master.content_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def decrypt_file(self):
        self.master.content_area.destroy()  # Clear existing content
        self.master.content_area = Form_Decrpyt_File(self.master)  # Create a new form
        self.master.content_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def encrypt_folder(self):
        self.master.content_area.destroy()  # Clear existing content
        self.master.content_area = Form_Encrpyt_Folder(self.master)  # Create a new form
        self.master.content_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def decrypt_folder(self):
        self.master.content_area.destroy()  # Clear existing content
        self.master.content_area = Form_Decrpyt_Folder(self.master)  # Create a new form
        self.master.content_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
def main():
    app = App()
    app.mainloop()