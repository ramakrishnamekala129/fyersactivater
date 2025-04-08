# Fyers API Authentication GUI

A simple Tkinter-based GUI application that helps users generate authentication URLs for the Fyers API. This tool simplifies the process of obtaining authentication tokens for the Fyers trading platform.

## Features

- User-friendly interface with pre-filled default values
- Generates authentication URLs for Fyers API
- Option to open the URL directly in your browser
- Copy URL functionality for easy sharing
- Input validation to prevent errors
- Clear and reset functionality

## Requirements

The application requires the following Python packages:

- tkinter (comes with Python)
- pyotp
- pytz
- fyers-apiv3

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install pyotp pytz fyers-apiv3
```

## Usage

1. Run the application:

```bash
python fyers_auth_gui.py
```

2. Fill in your Fyers API credentials (default values are pre-filled)
3. Click "Generate Auth URL" to create the authentication URL
4. Use "Open in Browser" to directly open the URL in your default web browser
5. Alternatively, use "Copy URL" to copy the URL to your clipboard

## Input Fields

- **Client ID**: Your Fyers API client ID
- **Secret Key**: Your Fyers API secret key
- **Redirect URI**: The callback URL for the OAuth flow
- **Fyers ID**: Your Fyers trading account ID
- **PIN**: Your Fyers account PIN
- **TOTP Key**: The TOTP secret key for two-factor authentication
- **Response Type**: The OAuth response type (default: "code")
- **Grant Type**: The OAuth grant type (default: "authorization_code")
- **State**: A session identifier (default: "sample")

## Notes

- The application pre-fills the fields with default values for convenience
- All fields are validated before generating the URL
- The TOTP key is used for two-factor authentication
- The generated URL will open the Fyers login page in your browser