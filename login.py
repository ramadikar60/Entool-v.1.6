import customtkinter
import bcrypt
from tkinter import messagebox
from config.database import collection
from config.verification import verify_otp

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("350x400")
        self.title("Login")
        self.configure(fg_color="#66004d")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = Login(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

class Login(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.labelLogin = customtkinter.CTkLabel(self, text="LOGIN", font=("Times New Roman", 24))
        self.labelLogin.place(relx=0.5, rely=0.15, anchor="center")

        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Email", font=("Times New Roman", 14), text_color="black", width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.email_entry.place(relx=0.5, rely=0.35, anchor="center")

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", font=("Times New Roman", 14), text_color="black", show="*", width=230, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.password_entry.place(relx=0.5, rely=0.53, anchor="center")

        self.labelLogin = customtkinter.CTkLabel(self, text="Dont have an account?", font=("Times New Roman", 12))
        self.labelLogin.place(relx=0.4, rely=0.65, anchor="center")
        self.register_button = customtkinter.CTkButton(self, text="Register", font=("Times New Roman", 12), width=10, fg_color="transparent", hover=False, command=self.register)
        self.register_button.place(relx=0.67, rely=0.65, anchor="center")

        self.login_button = customtkinter.CTkButton(self, text="Login", font=("Times New Roman", 14), width=230, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.login)
        self.login_button.place(relx=0.5, rely=0.75, anchor="center")

        self.lupa_button = customtkinter.CTkButton(self, text="Forgot Password", font=("Times New Roman", 12), width=100, height=30, fg_color="transparent", hover_color="#e60073", corner_radius=50, command=self.forgot)
        self.lupa_button.place(relx=0.5, rely=0.87, anchor="center")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        result = collection.find_one({"email": email})

        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result['password']):
                if result["verified"]:
                    messagebox.showinfo("Login", "Login successful!")
                    self.master.destroy()
                    from view import menu
                    menu.main()
                else:
                    messagebox.showerror("Login", "Email not verified. Please enter the OTP.")

                    verify_otp(email)
            else:
                messagebox.showerror("Login", "Invalid email or password!")
                self.email_entry.delete(0, customtkinter.END)
                self.password_entry.delete(0, customtkinter.END)

        elif email == "" or password == "":
            messagebox.showerror("Login", "Form be required!")
        else:
            messagebox.showerror("Login", "Invalid email or password!")
            self.email_entry.delete(0, customtkinter.END)
            self.password_entry.delete(0, customtkinter.END)
    
    def forgot(self):
        import forgot_password
        forgot_password.main()

    def register(self):
        import register
        register.main()

app = App()
app.mainloop()