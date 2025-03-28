import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import string

# Function to extract the hex bytes from a file
def extract_hex_bytes(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        return data  # Returning bytes directly
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        messagebox.showerror("Error", f"Could not read file: {file_path}")
        return None

# Function to replace hex bytes in a file
def replace_hex_bytes(file_path, old_bytes, new_bytes):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Ensure the old bytes exist in the file data
        if old_bytes not in data:
            messagebox.showerror("Error", "Old hex not found!")
            return
        
        # Replace the old bytes with new bytes
        data = data.replace(old_bytes, new_bytes)
        
        with open(file_path, 'wb') as f:
            f.write(data)
        print(f"Successfully replaced hex bytes in {file_path}")
    except Exception as e:
        print(f"Error replacing hex bytes in {file_path}: {e}")
        messagebox.showerror("Error", f"Could not replace hex in file: {file_path}")

# Function to write a random paragraph to a file (for destruct)
def write_random_paragraph(file_path):
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit"]
    paragraph = ' '.join(random.choices(words, k=random.randint(20, 50)))
    with open(file_path, 'w') as f:
        f.write(paragraph)
    print(f"Replaced {file_path} with a random paragraph")

# Function to perform the "inject" operation (replace rawaccel.exe with LICENSE hex)
def inject():
    try:
        # Open file dialogs to select the LICENSE and rawaccel.exe files
        license_path = filedialog.askopenfilename(title="Select LICENSE file", filetypes=[("Text files", "*.txt")])
        rawaccel_path = filedialog.askopenfilename(title="Select rawaccel.exe", filetypes=[("Executable files", "*.exe")])

        print(f"LICENSE file selected: {license_path}")
        print(f"rawaccel.exe file selected: {rawaccel_path}")

        if not license_path or not rawaccel_path:
            return

        # Extract bytes from LICENSE file
        new_bytes = extract_hex_bytes(license_path)
        if new_bytes is None:
            return

        # Read current rawaccel.exe file as bytes (for reverting later)
        rawaccel_original_bytes = extract_hex_bytes(rawaccel_path)
        if rawaccel_original_bytes is None:
            return

        # Store the original bytes of rawaccel.exe for later use (for destruct)
        with open("original_rawaccel_bytes.bin", "wb") as f:
            f.write(rawaccel_original_bytes)

        # Replace rawaccel.exe with LICENSE bytes
        replace_hex_bytes(rawaccel_path, rawaccel_original_bytes, new_bytes)
        
        messagebox.showinfo("Success", "Injection complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to perform the "destruct" operation (restore rawaccel.exe and replace LICENSE with random paragraph)
def destruct():
    try:
        # Open file dialogs to select the LICENSE and rawaccel.exe files
        license_path = filedialog.askopenfilename(title="Select LICENSE file", filetypes=[("Text files", "*.txt")])
        rawaccel_path = filedialog.askopenfilename(title="Select rawaccel.exe", filetypes=[("Executable files", "*.exe")])

        print(f"LICENSE file selected: {license_path}")
        print(f"rawaccel.exe file selected: {rawaccel_path}")

        if not license_path or not rawaccel_path:
            return

        # Retrieve original rawaccel.exe bytes (from stored file)
        with open("original_rawaccel_bytes.bin", "rb") as f:
            original_rawaccel_bytes = f.read()

        # Replace rawaccel.exe with original bytes
        replace_hex_bytes(rawaccel_path, extract_hex_bytes(rawaccel_path), original_rawaccel_bytes)

        # Replace LICENSE file with random paragraph
        write_random_paragraph(license_path)
        
        messagebox.showinfo("Success", "Destruction complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create GUI
app = tk.Tk()
app.title("Hex Injector")
app.geometry("300x200")

# Buttons for Inject and Destruct operations
tk.Button(app, text="Inject", command=inject).pack(pady=10)
tk.Button(app, text="Destruct", command=destruct).pack(pady=10)

# Run the app
app.mainloop()
