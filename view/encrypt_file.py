import customtkinter as ctk
from tkinter import filedialog, messagebox
from config.database import db
from gridfs import GridFS
from cryptography.fernet import Fernet
import pathlib
import os
import logging
import logging.handlers
import datetime

class Form_Encrpyt_File(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.encrypt_file_label = ctk.CTkLabel(self, text="ENCRYPT FILE", font=("Times New Roman", 24))
        self.encrypt_file_label.place(relx=0.5, rely=0.15, anchor="center")

        self.encrypt_file_entry1 = ctk.CTkEntry(self, placeholder_text="Encrypt Your File Here", font=("Times New Roman", 14), text_color="black", width=350, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.encrypt_file_entry1.place(relx=0.43, rely=0.35, anchor="center")

        self.encrypt_file_browse1 = ctk.CTkButton(self, text="Browse", font=("Times New Roman", 14), width=30, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.browse_file)
        self.encrypt_file_browse1.place(relx=0.88, rely=0.35, anchor="center")

        self.encrypt_file_entry2 = ctk.CTkEntry(self, placeholder_text="Password Your Encrypt", font=("Times New Roman", 14), text_color="black", show="*", width=350, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.encrypt_file_entry2.place(relx=0.43, rely=0.50, anchor="center")

        self.encrypt_file_entry3 = ctk.CTkEntry(self, placeholder_text="Path For Save Your Password", font=("Times New Roman", 14), text_color="black", width=350, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.encrypt_file_entry3.place(relx=0.43, rely=0.65, anchor="center")

        self.encrypt_file_browse2 = ctk.CTkButton(self, text="Browse", font=("Times New Roman", 14), width=30, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.browse_folder)
        self.encrypt_file_browse2.place(relx=0.88, rely=0.65, anchor="center")

        self.submit_button = ctk.CTkButton(self, text="Submit", font=("Times New Roman", 14), width=80, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.process)
        self.submit_button.place(relx=0.7, rely=0.80, anchor="center")


    def process(self, event = None):
        folder_path = 'logs'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Membuat TimedRotatingFileHandler
        log_filename = datetime.datetime.now().strftime('entool_%Y-%m-%d.log')
        log_path = os.path.join(folder_path, log_filename)

        # Cek apakah handler sudah ada
        logger = logging.getLogger('')
        if not logger.handlers:
            # Membuat TimedRotatingFileHandler
            handler = logging.handlers.TimedRotatingFileHandler(
                log_path, when='midnight', interval=1, backupCount=0
            )

            # Konfigurasi logger
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # # Membuat folder jika belum ada
        # folder_path = 'logs'
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)

        # # Membuat TimedRotatingFileHandler
        # log_filename = datetime.datetime.now().strftime('entool_%Y-%m-%d.log')
        # log_path = os.path.join(folder_path, log_filename)

        # # Membuat TimedRotatingFileHandler
        # handler = logging.handlers.TimedRotatingFileHandler(
        #     log_path, when='midnight', interval=1
        # )

        # # Konfigurasi logger
        # logger = logging.getLogger('')
        # logger.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        # handler.close()
        
        fs = GridFS(db)

        def generate_key(keyfile):
            """Generate a new key and save it to a file."""
            key = Fernet.generate_key()

            with fs.new_file(filename=keyfile, content_type='application/octet-stream') as fp:
                fp.write(key)

            return key

        def load_key(keyfile):
            """Load a key from the given file."""
            with open(keyfile, 'rb') as f:
                return f.read()

        def encrypt_file(filename, key):
            """Encrypt the given file using the given key."""
            f = Fernet(key)

            with open(filename, 'rb') as file:
                file_data = file.read()
            encrypted_data = f.encrypt(file_data)

            with open(filename + '.rama', 'wb') as file:
                file.write(encrypted_data)
            os.remove(filename)

        try:
            # Input dari user
            path = self.encrypt_file_entry1.get()
            keyfile = self.encrypt_file_entry2.get()
            key_dir = self.encrypt_file_entry3.get()

            # Generate atau load key
            if pathlib.Path(keyfile).is_file():
                key = load_key(keyfile)
            else:
                key = generate_key(keyfile)
                key_filename = os.path.basename(keyfile)

                with open(os.path.join(key_dir, key_filename + '.txt'), 'wb') as f:
                    f.write(key)
                
            # Enkripsi file/folder
            if os.path.isfile(path):
                encrypt_file(path, key)
                logging.info("Berhasil mengenkripsi file.")
                messagebox.showinfo("Berhasil", "File berhasil dienkripsi.")
                self.encrypt_file_entry1.delete(0, ctk.END)
                self.encrypt_file_entry2.delete(0, ctk.END)
                self.encrypt_file_entry3.delete(0, ctk.END)
            else:
                logging.error("File atau direktori tidak ditemukan.")
                messagebox.showerror("Error", "File gagal dienkripsi.")
            return True

        except:
            logging.error("Terjadi kesalahan")
            # messagebox.showerror("Error", "Terjadi kesalahan saat menjalankan program.")
            messagebox.showerror("Error", "File gagal didekripsi.")
            return True

    def browse_file(self):
        filetypes = (
            ('all files', '*.*'),
            ('text files', '*.txt'),
            ('Python files', '*.py'),
            ('Image files', '*.jpg;*.png'),
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        if filename:
            self.encrypt_file_entry1.delete(0, ctk.END)
            self.encrypt_file_entry1.insert(0, filename)

    def browse_folder(self):
        foldername = filedialog.askdirectory(
            title='Select a folder',
            initialdir='/'
        )

        if foldername:
            self.encrypt_file_entry3.delete(0, ctk.END)
            self.encrypt_file_entry3.insert(0, foldername)