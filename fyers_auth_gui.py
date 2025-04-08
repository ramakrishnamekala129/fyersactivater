import tkinter as tk
from tkinter import ttk, messagebox
import pyotp
import webbrowser
import pytz
import os
import time
import datetime
from urllib.parse import parse_qs, urlparse

try:
    from fyers_apiv3 import fyersModel
    FYERS_AVAILABLE = True
except ImportError:
    FYERS_AVAILABLE = False
    messagebox.showerror("Import Error", "fyers_apiv3 module not found. Please install it using 'pip install fyers-apiv3'")

class FyersAuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fyers API Authentication")
        self.geometry("600x650")
        self.configure(bg="#f0f0f0")
        self.resizable(True, True)
        
        # Set app icon and style
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("TEntry", font=("Arial", 10))
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Fyers API Authentication", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Authentication Details", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Set constant values (hidden from UI)
        self.response_type_var = tk.StringVar(value="code")
        self.grant_type_var = tk.StringVar(value="authorization_code")
        self.state_var = tk.StringVar(value="sample")
        
        # Client ID
        ttk.Label(input_frame, text="Client ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.client_id_var = tk.StringVar(value="")
        ttk.Entry(input_frame, textvariable=self.client_id_var, width=40).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Secret Key
        ttk.Label(input_frame, text="Secret Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.secret_key_var = tk.StringVar(value="")
        ttk.Entry(input_frame, textvariable=self.secret_key_var, width=40).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Redirect URI
        ttk.Label(input_frame, text="Redirect URI:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.redirect_uri_var = tk.StringVar(value="")
        ttk.Entry(input_frame, textvariable=self.redirect_uri_var, width=40).grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Fyers ID
        ttk.Label(input_frame, text="Fyers ID:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.fyers_id_var = tk.StringVar(value="")
        ttk.Entry(input_frame, textvariable=self.fyers_id_var, width=40).grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # PIN
        ttk.Label(input_frame, text="PIN:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.pin_var = tk.StringVar(value="")
        ttk.Entry(input_frame, textvariable=self.pin_var, width=40, show="*").grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        # TOTP Key
        ttk.Label(input_frame, text="TOTP Key:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.totp_key_var = tk.StringVar(value="")
        ttk.Entry(input_frame, textvariable=self.totp_key_var, width=40).grid(row=5, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Generate URL Button
        self.generate_button = ttk.Button(button_frame, text="Generate Auth URL", command=self.generate_auth_url)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        # Open in Browser Button
        self.open_browser_button = ttk.Button(button_frame, text="Open in Browser", command=self.open_in_browser, state=tk.DISABLED)
        self.open_browser_button.pack(side=tk.LEFT, padx=5)
        
        # Copy URL Button
        self.copy_button = ttk.Button(button_frame, text="Copy URL", command=self.copy_url, state=tk.DISABLED)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # URL Display
        url_frame = ttk.LabelFrame(main_frame, text="Generated URL", padding="10")
        url_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.url_text = tk.Text(url_frame, wrap=tk.WORD, height=5, width=60, font=("Arial", 9))
        self.url_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set initial status
        self.status_var.set("Ready")
    
    def validate_inputs(self):
        """Validate all input fields"""
        required_fields = {
            "Client ID": self.client_id_var.get(),
            "Secret Key": self.secret_key_var.get(),
            "Redirect URI": self.redirect_uri_var.get(),
            "Fyers ID": self.fyers_id_var.get(),
            "PIN": self.pin_var.get(),
            "TOTP Key": self.totp_key_var.get()
            # Hidden constant fields are not included in validation
            # as they always have default values
        }
        
        # Check for empty fields
        empty_fields = [field for field, value in required_fields.items() if not value.strip()]
        if empty_fields:
            messagebox.showerror("Validation Error", f"The following fields cannot be empty: {', '.join(empty_fields)}")
            return False
        
        # Validate TOTP key format (basic check)
        if not self.totp_key_var.get().isalnum():
            messagebox.showerror("Validation Error", "TOTP Key should only contain alphanumeric characters")
            return False
            
        return True
    
    def generate_auth_url(self):
        """Generate the authentication URL"""
        if not FYERS_AVAILABLE:
            messagebox.showerror("Error", "fyers_apiv3 module is not available. Please install it first.")
            return
            
        if not self.validate_inputs():
            return
            
        try:
            self.status_var.set("Generating authentication URL...")
            self.update_idletasks()
            
            client_id = self.client_id_var.get()
            secret_key = self.secret_key_var.get()
            redirect_uri = self.redirect_uri_var.get()
            response_type = self.response_type_var.get()
            state = self.state_var.get()
            grant_type = self.grant_type_var.get()
            
            # Create session model
            app_session = fyersModel.SessionModel(
                client_id=client_id,
                secret_key=secret_key,
                redirect_uri=redirect_uri,
                response_type=response_type,
                state=state,
                grant_type=grant_type
            )
            
            # Generate token URL
            token_url = app_session.generate_authcode()
            
            # Display the URL
            self.url_text.delete(1.0, tk.END)
            self.url_text.insert(tk.END, token_url)
            
            # Enable buttons
            self.open_browser_button.config(state=tk.NORMAL)
            self.copy_button.config(state=tk.NORMAL)
            
            self.status_var.set("Authentication URL generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate authentication URL: {str(e)}")
            self.status_var.set("Error generating authentication URL")
    
    def open_in_browser(self):
        """Open the generated URL in the default web browser"""
        url = self.url_text.get(1.0, tk.END).strip()
        if url:
            try:
                webbrowser.open(url)
                self.status_var.set("URL opened in browser")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open URL in browser: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No URL to open. Generate an authentication URL first.")
    
    def copy_url(self):
        """Copy the generated URL to clipboard"""
        url = self.url_text.get(1.0, tk.END).strip()
        if url:
            self.clipboard_clear()
            self.clipboard_append(url)
            self.status_var.set("URL copied to clipboard")
        else:
            messagebox.showwarning("Warning", "No URL to copy. Generate an authentication URL first.")
    
    def clear_fields(self):
        """Clear all input fields and reset the UI"""
        # Clear user input fields (set to blank)
        self.client_id_var.set("")
        self.secret_key_var.set("")
        self.redirect_uri_var.set("")
        self.fyers_id_var.set("")
        self.pin_var.set("")
        self.totp_key_var.set("")
        
        # Constant fields remain unchanged
        # self.response_type_var.set("code")
        # self.grant_type_var.set("authorization_code")
        # self.state_var.set("sample")
        
        # Clear URL display
        self.url_text.delete(1.0, tk.END)
        
        # Disable buttons
        self.open_browser_button.config(state=tk.DISABLED)
        self.copy_button.config(state=tk.DISABLED)
        
        self.status_var.set("Fields cleared")

if __name__ == "__main__":
    app = FyersAuthApp()
    app.mainloop()