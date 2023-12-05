import os
import shutil
import tarfile
import schedule
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from ttkthemes import ThemedTk

class BackupApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Backup Application")

        frame = tk.Frame(self.master, padx=10, pady=10)
        frame.pack()

        self.source_label = tk.Label(frame, text="Source Directory:")
        self.source_label.grid(row=0, column=0, sticky="w")

        self.source_entry = tk.Entry(frame)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_source_button = tk.Button(frame, text="Browse", command=self.browse_source)
        self.browse_source_button.grid(row=0, column=2, padx=5, pady=5)

        self.backup_label = tk.Label(frame, text="Backup Directory:")
        self.backup_label.grid(row=1, column=0, sticky="w")

        self.backup_entry = tk.Entry(frame)
        self.backup_entry.grid(row=1, column=1, padx=5, pady=5)

        self.browse_backup_button = tk.Button(frame, text="Browse", command=self.browse_backup)
        self.browse_backup_button.grid(row=1, column=2, padx=5, pady=5)

        self.log_label = tk.Label(frame, text="Log File:")
        self.log_label.grid(row=2, column=0, sticky="w")

        self.log_entry = tk.Entry(frame)
        self.log_entry.grid(row=2, column=1, padx=5, pady=5)

        self.browse_log_button = tk.Button(frame, text="Browse", command=self.browse_log)
        self.browse_log_button.grid(row=2, column=2, padx=5, pady=5)

        self.backup_interval_label = tk.Label(frame, text="Backup Interval (hours):")
        self.backup_interval_label.grid(row=3, column=0, sticky="w")

        self.backup_interval_entry = tk.Entry(frame)
        self.backup_interval_entry.grid(row=3, column=1, padx=5, pady=5)

        self.start_button = tk.Button(frame, text="Start Backup", command=self.start_backup)
        self.start_button.grid(row=4, column=1, pady=10)

    def browse_source(self):
        source_dir = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, source_dir)

    def browse_backup(self):
        backup_dir = filedialog.askdirectory()
        self.backup_entry.delete(0, tk.END)
        self.backup_entry.insert(0, backup_dir)

    def browse_log(self):
        log_file = filedialog.askopenfilename()
        self.log_entry.delete(0, tk.END)
        self.log_entry.insert(0, log_file)

    def start_backup(self):
        source_directory = self.source_entry.get()
        backup_directory = self.backup_entry.get()
        log_file = self.log_entry.get()
        backup_interval_hours = int(self.backup_interval_entry.get())

        # ... (rest of the backup script)

        def backup():
            try:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                backup_folder = os.path.join(backup_directory, f"backup_{timestamp}")

                os.makedirs(backup_folder)

                shutil.copytree(source_directory, os.path.join(backup_folder, "data"))

                with tarfile.open(f"{backup_folder}.tar.gz", "w:gz") as tar:
                    tar.add(backup_folder, arcname=os.path.basename(backup_folder))

                shutil.rmtree(backup_folder)

                log_entry = f"{timestamp}: Backup successful\n"
                with open(log_file, "a") as log:
                    log.write(log_entry)

                print(log_entry)

            except Exception as e:
                error_entry = f"{timestamp}: Backup failed - {str(e)}\n"
                with open(log_file, "a") as log:
                    log.write(error_entry)

                print(error_entry)

        schedule.every(backup_interval_hours).hours.do(backup)

        while True:
            schedule.run_pending()
            time.sleep(1)

# Create the main window
root = ThemedTk(theme="arc")
app = BackupApp(root)
root.mainloop()
