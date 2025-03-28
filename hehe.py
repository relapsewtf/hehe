import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import string

# Function to read file as hex
def extract_hex(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return data.hex()

# Function to replace hex in a file
def replace_hex(file_path, old_hex, new_hex):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    old_bytes = bytes.fromhex(old_hex)
    new_bytes = bytes.fromhex(new_hex)
    
    if old_bytes not in data:
        messagebox.showerror("Error", "Old hex not found!")
        return
    
    data = data.replace(old_bytes, new_bytes)
    
    with open(file_path, 'wb') as f:
        f.write(data)

# Function to write a random paragraph to a file
def write_random_paragraph(file_path):
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit"]
    paragraph = ' '.join(random.choices(words, k=random.randint(20, 50)))
    with open(file_path, 'w') as f:
        f.write(paragraph)

# Function to perform the "inject" operation (replace rawaccel.exe with LICENSE hex)
def inject():
    try:
        # File paths
        license_path = r"G:\LICENSE"
        rawaccel_path = r"G:\RawAccel_v1.6.1\rawaccel.exe"

        # Extract hex from LICENSE
        new_hex = extract_hex(license_path)

        # Read current rawaccel.exe file as hex (for reverting later)
        with open(rawaccel_path, 'rb') as f:
            rawaccel_data = f.read()
        rawaccel_original_hex = rawaccel_data.hex()

        # Store the original hex of rawaccel.exe for later use (for destruct)
        with open("original_rawaccel_hex.txt", "w") as f:
            f.write(rawaccel_original_hex)

        # Replace rawaccel.exe with LICENSE hex
        replace_hex(rawaccel_path, rawaccel_original_hex, new_hex)
        
        messagebox.showinfo("Success", "Injection complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to perform the "destruct" operation (restore rawaccel.exe and replace LICENSE with random paragraph)
def destruct():
    try:
        # File paths
        license_path = r"G:\LICENSE"
        rawaccel_path = r"G:\RawAccel_v1.6.1\RawAccel\rawaccel.exe"

        # Retrieve original rawaccel.exe hex (from stored file)
        with open("original_rawaccel_hex.txt", "r") as f:
            original_rawaccel_hex = f.read().strip()

        # Replace rawaccel.exe with original hex
        replace_hex(rawaccel_path, extract_hex(rawaccel_path), original_rawaccel_hex)

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
