import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ssh_utils.ssh import SSHManager
from reports.report_generator import generate_report
from datetime import datetime


class SSHManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated SSH Manager")
        self.root.geometry("700x500")
        
        # Variables
        self.ssh_manager = None
        self.is_connected = False
        
        # Host
        ttk.Label(root, text="Host:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.host_entry = ttk.Entry(root, width=40)
        self.host_entry.grid(row=0, column=1, padx=10, pady=5)

        # Username
        ttk.Label(root, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = ttk.Entry(root, width=40)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password
        ttk.Label(root, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(root, width=40, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Key File
        ttk.Label(root, text="Key File:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.key_file_path = tk.StringVar()
        ttk.Entry(root, textvariable=self.key_file_path, width=30).grid(row=3, column=1, padx=10, pady=5, sticky="w")
        ttk.Button(root, text="Browse", command=self.browse_key_file).grid(row=3, column=2, padx=10, pady=5)

        # Command
        ttk.Label(root, text="Command:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.command_entry = ttk.Entry(root, width=40)
        self.command_entry.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        self.connect_button = ttk.Button(root, text="Connect", command=self.connect_ssh)
        self.connect_button.grid(row=5, column=0, padx=10, pady=10)

        self.execute_button = ttk.Button(root, text="Execute Command", command=self.execute_command, state="disabled")
        self.execute_button.grid(row=5, column=1, padx=10, pady=10)

        self.report_button = ttk.Button(root, text="Generate Report", command=self.generate_report, state="disabled")
        self.report_button.grid(row=5, column=2, padx=10, pady=10)

        # Output Area
        self.output_text = tk.Text(root, height=15, wrap="word", state="disabled", bg="#f9f9f9", font=("Consolas", 10))
        self.output_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def browse_key_file(self):
        file_path = filedialog.askopenfilename(title="Select Key File")
        if file_path:
            self.key_file_path.set(file_path)

    def connect_ssh(self):
        host = self.host_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        key_path = self.key_file_path.get()
        
        if not host or not username:
            self.log_output("Error: Host and Username are required.", error=True)
            return

        try:
            self.ssh_manager = SSHManager(host, username, password, key_path)
            self.log_output("SSH Manager initialized. Connection successful.")
            self.is_connected = True
            self.execute_button.configure(state="normal")
            self.report_button.configure(state="normal")
        except Exception as e:
            self.log_output(f"Connection failed: {e}", error=True)
            self.is_connected = False

    def execute_command(self):
        if not self.is_connected:
            self.log_output("Error: Connect to a server first.", error=True)
            return
        
        command = self.command_entry.get()
        if not command:
            self.log_output("Error: Command cannot be empty.", error=True)
            return

        try:
            output = self.ssh_manager.execute_command_fabric(command)
            self.log_output(f"Command executed successfully:\n{output}")
        except Exception as e:
            self.log_output(f"Command execution failed: {e}", error=True)

    def generate_report(self):
        output = self.get_output_text()
        if not output.strip():
            self.log_output("Error: No output available for report generation.", error=True)
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            try:
                generate_report(filename, output)
                messagebox.showinfo("Success", f"Report saved as {filename}")
            except Exception as e:
                self.log_output(f"Report generation failed: {e}", error=True)

    def log_output(self, message, error=False):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        formatted_message = f"{timestamp}{message}\n"
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", formatted_message, "error" if error else "info")
        self.output_text.configure(state="disabled")
        self.output_text.see("end")

    def get_output_text(self):
        return self.output_text.get("1.0", "end-1c")


if __name__ == "__main__":
    root = tk.Tk()
    app = SSHManagerGUI(root)
    root.mainloop()
