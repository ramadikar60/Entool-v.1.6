import customtkinter
import bcrypt
from tkinter import messagebox, Toplevel, Label, Entry, Button
from config.database import collection
from config.otp import generate_otp, send_otp_email
from config.verification import verify_otp

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("350x390")
        self.title("Register")
        self.configure(fg_color="#66004d")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = Register(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

class Register(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.register_label = customtkinter.CTkLabel(self, text="REGISTER", font=("Times New Roman", 24))
        self.register_label.place(relx=0.5, rely=0.15, anchor="center")

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username", text_color="black", font=("Times New Roman", 14), width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")

        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Email", text_color="black", font=("Times New Roman", 14), width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.email_entry.place(relx=0.5, rely=0.5, anchor="center")

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show="*", text_color="black", font=("Times New Roman", 14), width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.password_entry.place(relx=0.5, rely=0.65, anchor="center")

        self.button = customtkinter.CTkButton(self, text="Register", font=("Times New Roman", 14), width=230, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.register)
        self.button.place(relx=0.5, rely=0.8, anchor="center")

    def register(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if email already exists in the database
        existing_user = collection.find_one({"email": email})
        if existing_user:
            messagebox.showerror("Register", "Email already registered.")
            return

        # Generate OTP
        otp = generate_otp()

        # Send OTP to the user's email
        send_otp_email(email, otp)

        # Store user data in the database
        user_data = {
            "email": email,
            "username": username,
            "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
            # "password": password,
            "otp": otp,
            "verified": False,
        }
        collection.insert_one(user_data)

        messagebox.showinfo("Register", "Registration successful! Please check your email for the OTP verification.")
        self.username_entry.delete(0, customtkinter.END)
        self.email_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        self.master.destroy()
        verify_otp(email)

def main():
    app = App()
    app.mainloop()