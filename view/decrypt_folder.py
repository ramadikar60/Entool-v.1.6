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

class Form_Decrpyt_Folder(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.decrypt_folder_label = ctk.CTkLabel(self, text="DECRYPT FOLDER", font=("Times New Roman", 24))
        self.decrypt_folder_label.place(relx=0.5, rely=0.15, anchor="center")

        self.decrypt_folder_entry1 = ctk.CTkEntry(self, placeholder_text="Decrypt Your Folder Here", font=("Times New Roman", 14), text_color="black", width=350, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.decrypt_folder_entry1.place(relx=0.43, rely=0.35, anchor="center")

        self.decrypt_folder_browse1 = ctk.CTkButton(self, text="Browse", font=("Times New Roman", 14), width=30, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.browse_folder)
        self.decrypt_folder_browse1.place(relx=0.88, rely=0.35, anchor="center")

        self.decrypt_folder_entry2 = ctk.CTkEntry(self, placeholder_text="Password Your Decrypt", font=("Times New Roman", 14), text_color="black", show="*", width=350, height=35, fg_color="white", placeholder_text_color="black", border_color="white", corner_radius=15)
        self.decrypt_folder_entry2.place(relx=0.43, rely=0.50, anchor="center")

        self.submit_button = ctk.CTkButton(self, text="Submit", font=("Times New Roman", 14), width=80, height=30, fg_color="#e60073", hover_color="#ff3399", corner_radius=50, command=self.process)
        self.submit_button.place(relx=0.7, rely=0.65, anchor="center")
    
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
        
        fs = GridFS(db)

        def load_key(keyfile):
            """Load a key from the given file."""
            with open(keyfile, 'rb') as f:
                return f.read()
            
        def load_key_mongodb(keyfile):
            """Load a key from the given file."""
            # Cari file keyfile berdasarkan nama
            file_obj = fs.find_one({'filename': keyfile})

            if file_obj:
                # Baca data keyfile dari GridFS
                key_data = file_obj.read()

                # Simpan keyfile ke dalam file lokal
                # keyfile_path = r'C:\Users\user\Entool\\' + keyfile # Ganti r'C:\Users\user\entool\\ atau hapus saja
                keyfile_path = keyfile # Ganti r'C:\Users\user\entool\\ atau hapus saja
                with open(keyfile_path, 'wb') as f:
                    f.write(key_data)

                # Load key dari file lokal
                key = load_key(keyfile_path)

                # Hapus keyfile lokal setelah di-load
                os.remove(keyfile_path)

                # Hapus file keyfile dari MongoDB
                fs.delete(file_obj._id)

                return key
            else:
                # messagebox.showerror("Error", "File keyfile tidak ditemukan di MongoDB GridFS")
                messagebox.showerror("Error", "Key dekripsi tidak sama dengan key enkripsi. File gagal didekripsi.")

        def decrypt_file(filename, key):
            """Decrypt the given file using the given key."""
            f = Fernet(key)
            with open(filename, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)
            with open(filename[:-5], 'wb') as file:
                file.write(decrypted_data)
            os.remove(filename)

        def decrypt_dir(path, key):
            """Decrypt all files in the given directory and its subdirectories using the given key."""
            for root, dirs, files in os.walk(path):
                for filename in files:
                    try:
                        filepath = os.path.join(root, filename)
                        decrypt_file(filepath, key)
                    except:
                        messagebox.showerror("Error", "Key dekripsi tidak sama dengan key enkripsi. File gagal didekripsi.")
                        return False
            return True
        try:
            # Input dari user
            path = self.decrypt_folder_entry1.get()
            keyfile = self.decrypt_folder_entry2.get()

            # Generate atau load key
            if pathlib.Path(keyfile).is_file():
                key = load_key(keyfile)
            else:
                key = load_key_mongodb(keyfile)

            # Dekripsi file/folder
            if os.path.isdir(path):
                if decrypt_dir(path, key):
                    logging.info("Berhasil mendekripsi folder.")
                    messagebox.showinfo("Berhasil", "Folder berhasil didekripsi.")
                    self.decrypt_folder_entry1.delete(0, ctk.END)
                    self.decrypt_folder_entry2.delete(0, ctk.END)
                else:
                    logging.error("File gagal didekripsi.")
                    messagebox.showerror("Error", "Folder gagal didekripsi.")
            else:
                logging.error("File atau direktori tidak ditemukan.")
                messagebox.showinfo("Error", "Folder gagal didekripsi.")
        except:
            logging.error("File gagal didekripsi")
            # messagebox.showerror("Error", "Terjadi kesalahan saat menjalankan program.")
            messagebox.showerror("Error", "File gagal didekripsi.")
            return True

    def browse_folder(self):
        foldername = filedialog.askdirectory(
            title='Select a folder',
            initialdir='/'
        )

        if foldername:
            self.decrypt_folder_entry1.delete(0, ctk.END)
            self.decrypt_folder_entry1.insert(0, foldername)