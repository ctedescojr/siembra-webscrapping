import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import sys
import queue
from datetime import datetime

# Import the refactored scripts
from nortel_refactor import run_nortel_scraper
from dimensional_refactor import run_dimensional_scraper


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class TextRedirector:
    def __init__(self, widget, log_file, q):
        self.widget = widget
        self.log_file = log_file
        self.q = q  # Queue for thread-safe updates
        self.stdout = sys.stdout  # Keep a reference to original stdout
        self.stderr = sys.stderr  # Keep a reference to original stderr

    def write(self, text):
        self.q.put(text)  # Put text into the queue
        if self.log_file:
            self.log_file.write(text)
            self.log_file.flush()  # Ensure immediate write to file
        self.widget.update_idletasks()  # Force GUI update

    def flush(self):
        # This method is required for file-like objects
        pass


class ScriptRunnerGUI:
    def __init__(self, master):
        self.master = master
        master.title("SIEMBRA - Webscrapping")

        self.master.iconbitmap(resource_path("resource/img/favicon.ico"))

        self.log_file_handle = None
        self.output_queue = queue.Queue()  # Initialize the queue

        self.create_widgets()
        self.master.after(100, self.process_queue)  # Start periodic queue processing

    def create_widgets(self):
        # Buttons frame
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        self.dimensional_button = tk.Button(
            button_frame,
            text="Dimensional",
            command=lambda: self.run_script("dimensional"),  # Pass module name
        )
        self.dimensional_button.pack(side=tk.LEFT, padx=5)

        self.nortel_button = tk.Button(
            button_frame,
            text="Nortel",
            command=lambda: self.run_script("nortel"),  # Pass module name
        )
        self.nortel_button.pack(side=tk.LEFT, padx=5)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            self.master, wrap=tk.WORD, width=80, height=25
        )
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)  # Make it read-only

    def run_script(self, script_module_name):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Running {script_module_name} scraper...\n")
        self.output_text.config(state=tk.DISABLED)

        # Generate log file name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{script_module_name}_log_{timestamp}.txt"
        log_filepath = os.path.join(os.getcwd(), log_filename)

        try:
            self.log_file_handle = open(log_filepath, "w")
            sys.stdout = TextRedirector(
                self.output_text, self.log_file_handle, self.output_queue
            )
            sys.stderr = TextRedirector(
                self.output_text, self.log_file_handle, self.output_queue
            )

            # Run script in a separate thread to keep GUI responsive
            thread = threading.Thread(
                target=self._execute_refactored_script,
                args=(script_module_name, log_filepath),
            )
            thread.daemon = True  # Allow the thread to exit with the main program
            thread.start()

        except Exception as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"Error setting up logging: {e}\n")
            self.output_text.config(state=tk.DISABLED)
            if self.log_file_handle:
                self.log_file_handle.close()
                self.log_file_handle = None
            self._reset_stdout_stderr()

    def _execute_refactored_script(self, script_module_name, log_filepath):
        try:
            # Set MEIPASS_PARENT for child processes if needed (though now it's same process)
            # This is technically not needed if we are importing directly, but good for consistency
            if hasattr(sys, "_MEIPASS"):
                os.environ["MEIPASS_PARENT"] = sys._MEIPASS

            if script_module_name == "dimensional":
                run_dimensional_scraper()
            elif script_module_name == "nortel":
                run_nortel_scraper()
            else:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(
                    tk.END, f"Error: Unknown script module '{script_module_name}'.\n"
                )
                self.output_text.config(state=tk.DISABLED)
                return

            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(
                tk.END,
                f"\n--- {script_module_name} scraper finished ---\n",
            )
            self.output_text.config(state=tk.DISABLED)

        except Exception as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(
                tk.END, f"An error occurred during script execution: {e}\n"
            )
            self.output_text.config(state=tk.DISABLED)
        finally:
            if self.log_file_handle:
                self.log_file_handle.close()
                self.log_file_handle = None
            self._reset_stdout_stderr()

    def process_queue(self):
        while not self.output_queue.empty():
            try:
                text = self.output_queue.get_nowait()
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, text)
                self.output_text.config(state=tk.DISABLED)
                self.output_text.see(tk.END)  # Scroll to end after inserting
            except queue.Empty:
                pass
        self.master.after(100, self.process_queue)  # Schedule next check

    def _reset_stdout_stderr(self):
        sys.stdout = (
            sys.stdout.stdout if isinstance(sys.stdout, TextRedirector) else sys.stdout
        )
        sys.stderr = (
            sys.stderr.stderr if isinstance(sys.stderr, TextRedirector) else sys.stderr
        )


def main():
    root = tk.Tk()
    root.app = ScriptRunnerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
