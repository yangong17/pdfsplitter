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

        # Table Frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=5)

        self.table_label = tk.Label(self.table_frame, text="Page(s)   |   Name")
        self.table_label.pack()

        self.table_text = tk.Text(self.table_frame, height=10, width=50)
        self.table_text.pack()

        # Page Name Input
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)

        self.page_label = tk.Label(self.input_frame, text="Page")
        self.page_label.grid(row=0, column=0, padx=5)

        self.page_entry = tk.Entry(self.input_frame, width=10)
        self.page_entry.grid(row=0, column=1, padx=5)

        self.name_label = tk.Label(self.input_frame, text="Name")
        self.name_label.grid(row=0, column=2, padx=5)

        self.name_entry = tk.Entry(self.input_frame, width=20)
        self.name_entry.grid(row=0, column=3, padx=5)

        self.add_button = tk.Button(self.input_frame, text="Add", command=self.add_to_table)
        self.add_button.grid(row=0, column=4, padx=5)

    def create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        
        options_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Import Settings", command=self.import_settings)
        options_menu.add_command(label="Export Settings", command=self.export_settings)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            messagebox.showinfo("Selected PDF", f"Selected PDF: {self.pdf_path}")

    def add_to_table(self):
        page = self.page_entry.get()
        name = self.name_entry.get()
        if page and name:
            self.table_text.insert(tk.END, f"{page}   {name}\n")
            self.page_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)

    def split_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning("No PDF Selected", "Please select a PDF file first.")
            return

        try:
            self.data = self.get_table_data()
            pdf_reader = PdfReader(self.pdf_path)
            prefix = self.prefix_entry.get()
            output_dir = filedialog.askdirectory()
            if not output_dir:
                return
            for index, row in self.data.iterrows():
                pages = row['Page(s)']
                name = row['Name']
                self.create_pdf(pdf_reader, pages, name, prefix, output_dir)
            messagebox.showinfo("Success", "PDF split successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_table_data(self):
        data = []
        lines = self.table_text.get("1.0", tk.END).strip().split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                data.append({'Page(s)': parts[0], 'Name': ' '.join(parts[1:])})
        return pd.DataFrame(data)

    def create_pdf(self, pdf_reader, pages, name, prefix, output_dir):
        pdf_writer = PdfWriter()
        page_numbers = self.parse_pages(pages)
        for page_num in page_numbers:
            pdf_writer.add_page(pdf_reader.pages[page_num - 1])
        output_path = f"{output_dir}/{prefix}_{name}.pdf" if prefix else f"{output_dir}/{name}.pdf"
        with open(output_path, 'wb') as out_file:
            pdf_writer.write(out_file)

    def parse_pages(self, pages):
        page_numbers = []
        parts = pages.split(',')
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                page_numbers.extend(range(start, end + 1))
            else:
                page_numbers.append(int(part))
        return page_numbers

    def import_settings(self):
        settings_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if settings_path:
            with open(settings_path, 'r') as file:
                settings = file.read()
                self.table_text.delete("1.0", tk.END)
                self.table_text.insert(tk.END, settings)
            messagebox.showinfo("Import Settings", "Settings imported successfully.")

    def export_settings(self):
        settings_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if settings_path:
            with open(settings_path, 'w') as file:
                file.write(self.table_text.get("1.0", tk.END))
            messagebox.showinfo("Export Settings", "Settings exported successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
