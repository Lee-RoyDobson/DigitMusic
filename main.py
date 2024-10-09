import tkinter as tk
import ExtractNotes as en
from tkinter import filedialog
from tkinter import messagebox
import webbrowser  # Import the webbrowser module

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        file_path_var.set(file_path)

def on_okay():
    file_path = file_path_var.get()
    if file_path:
        notes = en.extract_notes(file_path, en.note_scale, en.note_pattern)
        en.save_to_html(notes, "index.html", 4)
        #messagebox.showinfo("Success", "File has been processed and saved to index.html")
        webbrowser.open("index.html")  # Open index.html with the default browser
    else:
        messagebox.showwarning("Warning", "No file selected")


if __name__ == "__main__":
    # Initialize the main application window
    root = tk.Tk()
    root.title("Note Extractor")

    # Set minimum window size
    root.minsize(150, 100)

    file_path_var = tk.StringVar()

    # Frame for the select file button
    select_frame = tk.Frame(root)
    select_frame.pack(expand=True, fill='x')

    # Button to select file, packed inside the frame
    select_button = tk.Button(select_frame, text="Select File", command=select_file)
    select_button.pack(expand=True)

    # Frame for the okay button
    okay_frame = tk.Frame(root)
    okay_frame.pack(expand=True, fill='x')

    # Okay button to process the selected file, packed inside the frame
    okay_button = tk.Button(okay_frame, text="Convert", command=on_okay)
    okay_button.pack(expand=True)

    # Run the application
    root.mainloop()

