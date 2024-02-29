import tkinter as tk
from tkinter import messagebox, Menu, filedialog
from tkinter import scrolledtext
from website_fuzzer import WebsiteFuzzer

class WebsiteFuzzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Fuzzer GUI")
        self.root.geometry("800x600")

        self.url_label = tk.Label(root, text="URL:")
        self.url_label.grid(row=0, column=0)
        self.url_entry = tk.Entry(root, width=50) 
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        self.payload_label = tk.Label(root, text="Payload (comma-separated):")
        self.payload_label.grid(row=1, column=0)
        self.payload_entry = tk.Entry(root, width=50)  
        self.payload_entry.grid(row=1, column=1, padx=10, pady=10)

        self.fuzz_position_label = tk.Label(root, text="Fuzz Position (FUZZ) :")
        self.fuzz_position_label.grid(row=2, column=0)
        self.fuzz_position_entry = tk.Entry(root, width=50) 
        self.fuzz_position_entry.grid(row=2, column=1, padx=10, pady=10)

        self.num_threads_label = tk.Label(root, text="Number of Threads:")
        self.num_threads_label.grid(row=3, column=0)
        self.num_threads_entry = tk.Entry(root, width=50) 
        self.num_threads_entry.grid(row=3, column=1, padx=10, pady=10)

        # Entry widgets for filtering criteria
        self.response_code_label = tk.Label(root, text="Response Code:")
        self.response_code_label.grid(row=4, column=0)
        self.response_code_entry = tk.Entry(root, width=50)
        self.response_code_entry.grid(row=4, column=1, padx=10, pady=10)

        self.word_count_label = tk.Label(root, text="Word Count:")
        self.word_count_label.grid(row=5, column=0)
        self.word_count_entry = tk.Entry(root, width=50)
        self.word_count_entry.grid(row=5, column=1, padx=10, pady=10)

        self.char_count_label = tk.Label(root, text="Character Count:")
        self.char_count_label.grid(row=6, column=0)
        self.char_count_entry = tk.Entry(root, width=50)
        self.char_count_entry.grid(row=6, column=1, padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Fuzzing", command=self.start_fuzzing)
        self.start_button.grid(row=7, column=0, columnspan=2, padx=200, pady=10)

        self.output_label = tk.Label(root, text="Fuzzing Output:")
        self.output_label.grid(row=8, column=0, columnspan=2, pady=10)

        self.output_text = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
        self.output_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        # Import file button
        self.import_button = tk.Button(root, text="Import Directories", command=self.import_directories)
        self.import_button.grid(row=1, column=2, columnspan=2, pady=10)

        self.menubar = Menu(root)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Export as Text", command=self.export_as_text)
        self.file_menu.add_command(label="Export as CSV", command=self.export_as_csv)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menubar)
    
        self.directories = []

    def start_fuzzing(self):
        self.clear_output_text()  # Clear output text box
        url = self.url_entry.get()
        payload = self.payload_entry.get().split(',')
        fuzz_position = self.fuzz_position_entry.get()
        num_threads = int(self.num_threads_entry.get())
        response_code_filter = self.response_code_entry.get()
        word_count_filter = self.word_count_entry.get()
        char_count_filter = self.char_count_entry.get()

        # Check if both payload field and imported directories are empty
        if not payload and not self.directories:
            messagebox.showerror("Error", "Please provide a payload or import directories.")
            return

        # Print domain name and fuzz position
        self.output_text.insert(tk.END, f"Domain: {url} | Fuzz Position: {fuzz_position}\n")

        fuzzer = WebsiteFuzzer(url, payload, fuzz_position)

        # Handle empty or non-numeric input for num_threads
        if num_threads:
            try:
                num_threads = int(num_threads)
            except ValueError:
                messagebox.showerror("Error", "Number of Threads must be a valid integer.")
                return
        else:
            messagebox.showerror("Error", "Please provide a value for Number of Threads.")
            return
        
        # Ensure payload is a list
        if payload=="":
            pass
        elif isinstance(payload, str):
            directories = payload.split(',')  # Split the payload string into a list of directories
        else:
            directories = payload  # Assume payload is already a list of directories

        if self.directories:
            directories.extend(self.directories)  # Extend the directories with the imported ones
        
        results = fuzzer.fuzz_multiple(directories, num_threads)

        results = fuzzer.fuzz_multiple(directories, num_threads)

        for result in results:
            parts = result.split()  # Split the result string by whitespace

            # Initialize variables to store values
            response_code = None
            word_count = None
            char_count = None

            # Extract key-value pairs from the parts
            for part in parts:
                key, value = part.split(':')
                if key == 'response':
                    response_code = int(value)
                elif key == 'word':
                    word_count = int(value)
                elif key == 'char':
                    char_count = int(value)

            # Apply filtering if filter is provided
            if ((response_code_filter and response_code != int(response_code_filter)) or
                (word_count_filter and word_count != int(word_count_filter)) or
                (char_count_filter and char_count != int(char_count_filter))):
                continue

            # Add the filtered result to the output text box
            self.output_text.insert(tk.END, result + "\n")



    def clear_output_text(self):
        self.output_text.delete('1.0', tk.END)

    def import_directories(self):
        # Prompt user to select a file containing directories
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    # Read directories from the file and store them in self.directories
                    self.directories = file.read().splitlines()
                messagebox.showinfo("Import", "Directories imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while importing: {str(e)}")

    def export_as_text(self):
        # Get text from the output text box
        text_data = self.output_text.get('1.0', tk.END).strip()

        if not text_data:
            messagebox.showinfo("Export", "No data to export.")
            return

        # Prompt user to choose a file location for text export
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(text_data)
                messagebox.showinfo("Export", f"Exported as text to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while exporting: {str(e)}")

    def export_as_csv(self):
        # Get text from the output text box
        text_data = self.output_text.get('1.0', tk.END).strip()

        if not text_data:
            messagebox.showinfo("Export", "No data to export.")
            return

        # Split the text data into lines and format each line as a CSV row
        csv_rows = []
        for line in text_data.split('\n'):
            parts = line.split()
            csv_row = ','.join(parts)
            csv_rows.append(csv_row)

        # Join the formatted CSV rows with newlines
        csv_data = '\n'.join(csv_rows)

        # Prompt user to choose a file location for CSV export
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(csv_data)
                messagebox.showinfo("Export", f"Exported as CSV to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while exporting: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteFuzzerGUI(root)
    root.mainloop()
