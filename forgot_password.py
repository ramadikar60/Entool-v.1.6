import customtkinter
import bcrypt
from tkinter import *
from tkinter import messagebox
from config.database import collection
from config.otp import generate_otp, send_otp_email

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("350x250")
        self.title("Forgot Password")
        self.configure(fg_color="#66004d")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = Forgot_Password(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

class Forgot_Password(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.labelLogin = customtkinter.CTkLabel(self, text="LUPA PASSWORD", font=("Times New Roman", 24))
        self.labelLogin.place(relx=0.5, rely=0.15, anchor="center")

        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Email", font=("Times New Roman", 14), text_color="black", width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.email_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.login_button = customtkinter.CTkButton(self, text="Request OTP", font=("Times New Roman", 14), width=230, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.request_otp)
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")

    def request_otp(self):
        email = self.email_entry.get()

        # Generate new OTP
        new_otp = generate_otp()        

        # Update OTP in the database
        result = collection.update_one({"email": email}, {"$set": {"otp": new_otp}})
        if result.modified_count == 0:
            messagebox.showerror("Request OTP", "Email not found.")
            return

        # Send OTP to the user's email
        send_otp_email(email, new_otp)

        messagebox.showinfo("Request OTP", "New OTP has been sent to your email.")

        # Clear existing widgets
        # self.email_entry.destroy()
        self.login_button.destroy()

        # Create new widgets for OTP and password
        self.otp_entry = customtkinter.CTkEntry(self, placeholder_text="OTP", font=("Times New Roman", 14), text_color="black", width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.otp_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="New Password", font=("Times New Roman", 14), text_color="black", width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15, show="*")
        self.password_entry.place(relx=0.5, rely=0.6, anchor="center")

        self.reset_button = customtkinter.CTkButton(self, text="Reset Password", font=("Times New Roman", 14), width=230, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.reset_password)
        self.reset_button.place(relx=0.5, rely=0.8, anchor="center")

    def reset_password(self):
        email = self.email_entry.get()
        otp = self.otp_entry.get()
        password = self.password_entry.get()

        # Verify OTP
        result = collection.find_one({"email": email, "otp": otp})
        if not result:
            messagebox.showerror("Reset Password", "Invalid OTP.")
            return

        # Generate new OTP
        new_otp = generate_otp()



        # Update OTP and password in the database
        collection.update_one({"email": email}, {"$set": {"otp": new_otp, "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())}})

        # Send new OTP to the user's email
        send_otp_email(email, new_otp)

        messagebox.showinfo("Reset Password", "Password has been reset successfully!")

        # Clear the OTP and password entry fields
        self.otp_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)

        # Destroy the OTP and password entry fields
        self.otp_entry.destroy()
        self.password_entry.destroy()
        self.reset_button.destroy()

        # Recreate the email entry and login button
        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Email", font=("Times New Roman", 14), text_color="black", width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.email_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.login_button = customtkinter.CTkButton(self, text="Request OTP", font=("Times New Roman", 14), width=230, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.request_otp)
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")

def main():
    app = App()
    app.mainloop()