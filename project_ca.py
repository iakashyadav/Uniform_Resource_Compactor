import tkinter as tk
from tkinter import messagebox
import pyshorteners
import pyperclip
import threading

class UniformResourceCompactor(tk.Tk):
    """
    An intermediary GUI that interfaces with a dedicated URL shortening
    service API to transform long, verbose links into concise,
    user-friendly identifiers.
    
    Technologies: Tkinter, pyshorteners
    """
    
    def __init__(self):
        super().__init__()
        
        # --- Configure the main window ---
        self.title("Uniform Resource Compactor")
        self.geometry("550x250")
        self.resizable(False, False)
        self.configure(bg='#f0f0f0')

        # --- Title Label ---
        title_label = tk.Label(self, 
                               text="Uniform Resource Compactor", 
                               font=("Arial", 16, "bold"), 
                               bg='#f0f0f0', 
                               pady=10)
        title_label.pack()

        # --- Input Frame ---
        frame_input = tk.Frame(self, bg='#f0f0f0', pady=10)
        frame_input.pack(fill='x', padx=20)

        lbl_long_url = tk.Label(frame_input, 
                                text="Enter Long URL:", 
                                font=("Arial", 10), 
                                bg='#f0f0f0', 
                                anchor='w')
        lbl_long_url.pack(fill='x')

        self.entry_long_url = tk.Entry(frame_input, 
                                        width=60, 
                                        font=("Arial", 10), 
                                        bd=2, 
                                        relief='groove')
        self.entry_long_url.pack(fill='x', pady=(5, 10))

        # --- Button ---
        self.btn_shorten = tk.Button(self, 
                                     text="Generate Short URL", 
                                     command=self.start_shorten_thread, 
                                     font=("Arial", 10, "bold"),
                                     bg='#0078D7', 
                                     fg='white', 
                                     relief='flat', 
                                     pady=5,
                                     cursor="hand2")
        self.btn_shorten.pack(pady=5)

        # --- Output Frame ---
        frame_output = tk.Frame(self, bg='#f0f0f0', pady=10)
        frame_output.pack(fill='x', padx=20)
        
        lbl_short_url = tk.Label(frame_output, 
                                 text="Shortened URL:", 
                                 font=("Arial", 10), 
                                 bg='#f0f0f0', 
                                 anchor='w')
        lbl_short_url.pack(fill='x')

        self.entry_short_url = tk.Entry(frame_output, 
                                        width=60, 
                                        font=("Arial", 10), 
                                        state='readonly', 
                                        readonlybackground='white', 
                                        fg='black', 
                                        bd=2, 
                                        relief='groove')
        self.entry_short_url.pack(fill='x', pady=5)
        
        self.btn_copy = tk.Button(frame_output, 
                                  text="Copy to Clipboard", 
                                  command=self.copy_to_clipboard, 
                                  font=("Arial", 9),
                                  bg='#5cb85c', 
                                  fg='white', 
                                  relief='flat',
                                  cursor="hand2")
        self.btn_copy.pack(pady=(5,0))

    def start_shorten_thread(self):
        """
        Use a thread to prevent the GUI from freezing during
        the network request to the shortening service.
        """
        self.btn_shorten.config(text="Shortening...", state="disabled")
        # Start the URL shortening in a separate thread
        thread = threading.Thread(target=self.shorten_url)
        thread.daemon = True # Allows program to exit even if thread is running
        thread.start()

    def shorten_url(self):
        """
        The core logic to interface with the pyshorteners service.
        """
        long_url = self.entry_long_url.get()
        if not long_url:
            messagebox.showwarning("Warning", "Please enter a URL to shorten.")
            self.reset_button()
            return

        try:
            # Initialize the shortener
            s = pyshorteners.Shortener()
            # Use the TinyURL service (simple, no API key required)
            short_url = s.tinyurl.short(long_url)

            # Update the GUI (must be done in the main thread)
            self.after(0, self.update_output_entry, short_url)

        except pyshorteners.exceptions.ShorteningErrorException:
            messagebox.showerror("Error", "Could not shorten the URL. Please check the link and your internet connection.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        
        # Always reset the button state, whether success or fail
        self.after(0, self.reset_button)

    def update_output_entry(self, short_url):
        """ Safely updates the GUI from the main thread. """
        self.entry_short_url.config(state='normal') # Enable to modify
        self.entry_short_url.delete(0, tk.END)
        self.entry_short_url.insert(0, short_url)
        self.entry_short_url.config(state='readonly') # Make read-only again

    def reset_button(self):
        """ Resets the button to its original state. """
        self.btn_shorten.config(text="Generate Short URL", state="normal")
        
    def copy_to_clipboard(self):
        """ Copies the content of the short URL entry to the clipboard. """
        short_url = self.entry_short_url.get()
        if short_url:
            pyperclip.copy(short_url)
            messagebox.showinfo("Copied!", "Short URL has been copied to your clipboard.")
        else:
            messagebox.showwarning("Warning", "Nothing to copy. Please generate a short URL first.")

# --- Run the Application ---
if __name__ == "__main__":
    app = UniformResourceCompactor()
    app.mainloop()