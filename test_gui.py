import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gui_frontend import WebsiteFuzzerGUI

class TestWebsiteFuzzerGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = WebsiteFuzzerGUI(self.root)

    def test_start_fuzzing_with_valid_payload(self):
        # Set up input values
        self.app.url_entry.insert(tk.END, "http://example.com")
        self.app.payload_entry.insert(tk.END, "directory1,directory2")
        self.app.fuzz_position_entry.insert(tk.END, "http://example.com/FUZZ")
        self.app.num_threads_entry.insert(tk.END, "2")

        # Simulate clicking the start button with a valid payload
        with patch.object(tk.messagebox, 'showerror') as mock_showerror:
            with patch.object(tk.scrolledtext.ScrolledText, 'insert') as mock_insert:
                self.app.start_fuzzing()
                self.assertFalse(mock_showerror.called)
                self.assertTrue(mock_insert.called)

    def test_import_directories(self):
        # Mock file dialog askopenfilename
        with patch.object(tk.filedialog, 'askopenfilename') as mock_askopenfilename:
            # Set the return value of the file dialog
            mock_askopenfilename.return_value = "test.txt"

            # Simulate clicking the import button
            with patch.object(tk.messagebox, 'showinfo') as mock_showinfo:
                self.app.import_directories()
                mock_showinfo.assert_called_once_with("Import", "Directories imported successfully.")
                self.assertEqual(self.app.directories, ['robots.txt','assets','drive','account'])

    def test_export_as_text_with_no_data(self):
        # Simulate clicking export as text button with no data in the output text box
        with patch.object(tk.messagebox, 'showinfo') as mock_showinfo:
            self.app.export_as_text()
            mock_showinfo.assert_called_once_with("Export", "No data to export.")

    # Add similar tests for export_as_csv method

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
