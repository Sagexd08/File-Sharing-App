import socket
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import json
import hashlib
from cryptography.fernet import Fernet
from tqdm import tqdm
import mimetypes
import logging
from datetime import datetime

class FileShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced File Sharing App")
        self.root.geometry("600x800")
        
        # Network settings
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 5000
        self.BUFFER_SIZE = 8192
        
        # Encryption setup
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
        # Transfer history
        self.transfer_history = []
        
        # Allowed file types (empty means all allowed)
        self.allowed_extensions = set()
        
        # Setup logging
        self.setup_logging()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start server thread
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()
    
    def setup_logging(self):
        log_dir = Path.home() / "FileShare" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_dir / f"fileshare_{datetime.now().strftime('%Y%m%d')}.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def create_widgets(self):
        # Main container
        main_container = ttk.Notebook(self.root)
        main_container.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Transfer tab
        transfer_frame = ttk.Frame(main_container)
        main_container.add(transfer_frame, text="Transfer")
        
        # Settings tab
        settings_frame = ttk.Frame(main_container)
        main_container.add(settings_frame, text="Settings")
        
        # History tab
        history_frame = ttk.Frame(main_container)
        main_container.add(history_frame, text="History")
        
        self.create_transfer_widgets(transfer_frame)
        self.create_settings_widgets(settings_frame)
        self.create_history_widgets(history_frame)

    def create_transfer_widgets(self, parent):
        # IP Address display
        ip_frame = ttk.LabelFrame(parent, text="Network Information")
        ip_frame.pack(pady=10, fill="x")
        ttk.Label(ip_frame, text=f"Your IP Address: {self.HOST}").pack(pady=5)
        
        # Send file section
        send_frame = ttk.LabelFrame(parent, text="Send File")
        send_frame.pack(pady=10, fill="x")
        
        ttk.Label(send_frame, text="Recipient IP:").pack(pady=5)
        self.recipient_ip = ttk.Entry(send_frame)
        self.recipient_ip.pack(pady=5, fill="x")
        
        self.selected_files_text = tk.Text(send_frame, height=3, width=40)
        self.selected_files_text.pack(pady=5, fill="x")
        
        btn_frame = ttk.Frame(send_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Choose Files", command=self.choose_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Send Files", command=self.send_files).pack(side=tk.LEFT, padx=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(parent, text="Transfer Progress")
        progress_frame.pack(pady=10, fill="x")
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill="x", pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        # Status section
        status_frame = ttk.LabelFrame(parent, text="Status Log")
        status_frame.pack(pady=10, fill="both", expand=True)
        
        self.status_text = tk.Text(status_frame, height=10, width=40)
        self.status_text.pack(pady=5, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)

    def create_settings_widgets(self, parent):
        # File type settings
        type_frame = ttk.LabelFrame(parent, text="Allowed File Types")
        type_frame.pack(pady=10, fill="x")
        
        self.file_type_var = tk.StringVar(value="all")
        ttk.Radiobutton(type_frame, text="Allow all files", 
                       variable=self.file_type_var, value="all",
                       command=self.update_file_types).pack(pady=5)
        ttk.Radiobutton(type_frame, text="Restrict file types", 
                       variable=self.file_type_var, value="restrict",
                       command=self.update_file_types).pack(pady=5)
        
        self.file_types_entry = ttk.Entry(type_frame)
        self.file_types_entry.pack(pady=5, fill="x")
        ttk.Label(type_frame, text="Enter extensions separated by comma (e.g., .pdf,.txt,.png)").pack()
        
        # Security settings
        security_frame = ttk.LabelFrame(parent, text="Security Settings")
        security_frame.pack(pady=10, fill="x")
        
        self.encryption_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="Enable encryption", 
                       variable=self.encryption_var).pack(pady=5)
        
        # Download location
        download_frame = ttk.LabelFrame(parent, text="Download Location")
        download_frame.pack(pady=10, fill="x")
        
        self.download_path = tk.StringVar(value=str(Path.home() / "FileShare" / "downloads"))
        ttk.Entry(download_frame, textvariable=self.download_path).pack(pady=5, fill="x")
        ttk.Button(download_frame, text="Browse", 
                  command=self.choose_download_location).pack(pady=5)

    def create_history_widgets(self, parent):
        self.history_tree = ttk.Treeview(parent, columns=("Date", "Type", "File", "Size", "Status"))
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("Type", text="Type")
        self.history_tree.heading("File", text="File")
        self.history_tree.heading("Size", text="Size")
        self.history_tree.heading("Status", text="Status")
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_file_types(self):
        if self.file_type_var.get() == "all":
            self.allowed_extensions = set()
        else:
            extensions = self.file_types_entry.get().strip()
            self.allowed_extensions = {ext.strip() for ext in extensions.split(",")}

    def choose_download_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_path.set(directory)

    def choose_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.selected_files_text.delete(1.0, tk.END)
            self.selected_files_text.insert(tk.END, "\n".join(files))

    def update_status(self, message):
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        logging.info(message)

    def update_progress(self, value, message=""):
        self.progress_var.set(value)
        if message:
            self.status_label.config(text=message)

    def add_to_history(self, transfer_type, filename, size, status):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_tree.insert("", 0, values=(date, transfer_type, filename, 
                                              f"{size/1024/1024:.1f} MB", status))
        
    def check_file_type(self, filename):
        if not self.allowed_extensions:
            return True
        return any(filename.lower().endswith(ext.lower()) for ext in self.allowed_extensions)

    def send_files(self):
        files = self.selected_files_text.get(1.0, tk.END).strip().split("\n")
        if not files or not files[0]:
            messagebox.showerror("Error", "Please select files to send")
            return

        recipient = self.recipient_ip.get().strip()
        if not recipient:
            messagebox.showerror("Error", "Please enter recipient's IP address")
            return

        for filename in files:
            if not self.check_file_type(filename):
                messagebox.showerror("Error", f"File type not allowed: {filename}")
                continue

            threading.Thread(target=self.send_single_file, 
                           args=(filename, recipient),
                           daemon=True).start()

    def send_single_file(self, filename, recipient):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((recipient, self.PORT))
                
                file_path = Path(filename)
                file_size = file_path.stat().st_size
                
                # Prepare metadata
                metadata = {
                    "filename": file_path.name,
                    "size": file_size,
                    "encrypted": self.encryption_var.get()
                }
                
                # Send metadata
                s.send(json.dumps(metadata).encode())
                if s.recv(1024).decode() != "OK":
                    raise Exception("Connection failed")
                
                # Send file content
                sent_bytes = 0
                with open(filename, 'rb') as f:
                    while True:
                        data = f.read(self.BUFFER_SIZE)
                        if not data:
                            break
                            
                        if self.encryption_var.get():
                            data = self.cipher_suite.encrypt(data)
                            
                        s.send(data)
                        sent_bytes += len(data)
                        progress = (sent_bytes / file_size) * 100
                        self.root.after(0, self.update_progress, progress,
                                      f"Sending {file_path.name}: {progress:.1f}%")
                
                self.root.after(0, self.update_status, f"File sent successfully: {file_path.name}")
                self.root.after(0, self.add_to_history, "Send", file_path.name, 
                              file_size, "Completed")
                
        except Exception as e:
            error_msg = f"Failed to send file: {str(e)}"
            self.root.after(0, self.update_status, error_msg)
            self.root.after(0, self.add_to_history, "Send", file_path.name, 
                          file_size, "Failed")
            logging.error(error_msg)

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            
            self.update_status("Server started, waiting for incoming files...")
            
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, 
                               args=(conn, addr),
                               daemon=True).start()

    def handle_client(self, conn, addr):
        try:
            # Receive metadata
            metadata = json.loads(conn.recv(1024).decode())
            filename = metadata["filename"]
            file_size = metadata["size"]
            encrypted = metadata.get("encrypted", False)
            
            # Send acknowledgment
            conn.send("OK".encode())
            
            if not self.check_file_type(filename):
                raise Exception("File type not allowed")
            
            # Create download directory if it doesn't exist
            download_dir = Path(self.download_path.get())
            download_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = download_dir / filename
            
            # Receive and save file
            received_bytes = 0
            with open(file_path, 'wb') as f:
                while received_bytes < file_size:
                    data = conn.recv(self.BUFFER_SIZE)
                    if not data:
                        break
                        
                    if encrypted:
                        data = self.cipher_suite.decrypt(data)
                        
                    f.write(data)
                    received_bytes += len(data)
                    progress = (received_bytes / file_size) * 100
                    self.root.after(0, self.update_progress, progress,
                                  f"Receiving {filename}: {progress:.1f}%")
            
            self.root.after(0, self.update_status, 
                          f"Received file from {addr[0]}: {filename}")
            self.root.after(0, self.add_to_history, "Receive", filename, 
                          file_size, "Completed")
            
        except Exception as e:
            error_msg = f"Error receiving file from {addr[0]}: {str(e)}"
            self.root.after(0, self.update_status, error_msg)
            self.root.after(0, self.add_to_history, "Receive", filename, 
                          file_size, "Failed")
            logging.error(error_msg)
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileShareApp(root)
    root.mainloop()