import tkinter as tk
from tkinter import filedialog, messagebox
import pefile
import os
import random
import string

def read_hex_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip().split(',')

def write_random_paragraph(file_path):
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit"]
    paragraph = ' '.join(random.choices(words, k=random.randint(20, 50)))
    with open(file_path, 'w') as f:
        f.write(paragraph)

def extract_hex(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return data.hex()

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

def inject():
    file_path = filedialog.askopenfilename()
    hex_file = filedialog.askopenfilename(title="Select hex data file")
    if not file_path or not hex_file:
        return
    
    try:
        old_hex, new_hex = read_hex_from_file(hex_file)
        replace_hex(file_path, old_hex, new_hex)
        pe = pefile.PE(file_path)
        pe.write(file_path)
        messagebox.showinfo("Success", "Injection complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def destruct():
    file_path = filedialog.askopenfilename()
    hex_file = filedialog.askopenfilename(title="Select hex data file")
    if not file_path or not hex_file:
        return
    
    try:
        old_hex, new_hex = read_hex_from_file(hex_file)
        replace_hex(file_path, new_hex, old_hex)
        write_random_paragraph(hex_file)
        messagebox.showinfo("Success", "Destruction complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Hex Injector")
app.geometry("300x200")

tk.Button(app, text="Inject", command=inject).pack(pady=10)
tk.Button(app, text="Destruct", command=destruct).pack(pady=10)

app.mainloop()
