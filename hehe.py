# Modify inject function to use file dialog for selecting rawaccel.exe
def inject():
    try:
        # Open file dialogs to select the LICENSE and rawaccel.exe files
        license_path = filedialog.askopenfilename(title="Select LICENSE file", filetypes=[("Text files", "*.txt")])
        rawaccel_path = filedialog.askopenfilename(title="Select rawaccel.exe", filetypes=[("Executable files", "*.exe")])

        if not license_path or not rawaccel_path:
            return

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

# Modify destruct function to use file dialog for selecting rawaccel.exe
def destruct():
    try:
        # Open file dialogs to select the LICENSE and rawaccel.exe files
        license_path = filedialog.askopenfilename(title="Select LICENSE file", filetypes=[("Text files", "*.txt")])
        rawaccel_path = filedialog.askopenfilename(title="Select rawaccel.exe", filetypes=[("Executable files", "*.exe")])

        if not license_path or not rawaccel_path:
            return

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
