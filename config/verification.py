import customtkinter
from tkinter import messagebox
# from database import collection
from config.database import collection

def verify_otp(email):
    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.geometry("350x250")
            self.title("Verification OTP")
            self.configure(fg_color="#66004d")
            self.resizable(False, False)
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.my_frame = Verification(master=self)
            self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    class Verification(customtkinter.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.labelLogin = customtkinter.CTkLabel(self, text="Verification OTP", font=("Times New Roman", 24))
            self.labelLogin.place(relx=0.5, rely=0.2, anchor="center")

            self.otp_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Your OTP", font=("Times New Roman", 14), width=230, height=35, fg_color="white", text_color="black", placeholder_text_color="black", border_color="white", corner_radius=15)
            self.otp_entry.place(relx=0.5, rely=0.5, anchor="center")

            self.button = customtkinter.CTkButton(self, text="Verify", font=("Times New Roman", 14), width=230, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.verify)
            self.button.place(relx=0.5, rely=0.75, anchor="center")

        def verify(self):
            otp = self.otp_entry.get()
            result = collection.find_one({"email": email, "otp": otp})

            if result:
                collection.update_one({"email": email}, {"$set": {"verified": True}})
                messagebox.showinfo("OTP Verification", "OTP verification successful!")
            else:
                messagebox.showerror("OTP Verification", "Invalid")

            self.master.destroy()
    app = App()
    app.mainloop()