import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")

        self.pdf_path = ""
        self.data = pd.DataFrame(columns=["Page(s)", "Name"])

        # Create GUI elements
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=5)

        # Upload PDF Button
        self.upload_button = tk.Button(self.buttons_frame, text="Select PDF", command=self.select_pdf)
        self.upload_button.grid(row=0, column=0, padx=5)

        # Split PDF Button
        self.split_button = tk.Button(self.buttons_frame, text="Split PDF", command=self.split_pdf)
        self.split_button.grid(row=0, column=1, padx=5)

        # Prefix Entry
        self.prefix_label = tk.Label(self.buttons_frame, text="Prefix:")
        self.prefix_label.grid(row=0, column=2, padx=5)
        self.prefix_entry = tk.Entry(self.buttons_frame)
        self.prefix_entry.grid(row=0, column=3, padx=5)

        # PDF Info Label
        self.pdf_info_label = tk.Label(self.root, text="")
        self.pdf_info_label.pack(pady=5)

        # Table
