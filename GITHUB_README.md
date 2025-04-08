# Fyers API Authentication GUI

A simple GUI application that helps users generate authentication URLs for the Fyers API. This tool simplifies the process of obtaining authentication tokens for the Fyers trading platform.

![Fyers Auth GUI](https://github.com/user/fyersactivater/raw/main/screenshots/app_screenshot.png)

## Download

You can download the executable directly from this repository:

- [Download FyersAuthGUI.exe](https://github.com/user/fyersactivater/raw/main/dist/FyersAuthGUI.exe)

## Features

- User-friendly interface with pre-filled default values
- Generates authentication URLs for Fyers API
- Option to open the URL directly in your browser
- Copy URL functionality for easy sharing
- Input validation to prevent errors
- Clear and reset functionality

## Usage

1. Download the executable file from the link above
2. Run the application by double-clicking on FyersAuthGUI.exe
3. Fill in your Fyers API credentials
4. Click "Generate Auth URL" to create the authentication URL
5. Use "Open in Browser" to directly open the URL in your default web browser
6. Alternatively, use "Copy URL" to copy the URL to your clipboard

## Input Fields

- **Client ID**: Your Fyers API client ID
- **Secret Key**: Your Fyers API secret key
- **Redirect URI**: The callback URL for the OAuth flow
- **Fyers ID**: Your Fyers trading account ID
- **PIN**: Your Fyers account PIN
- **TOTP Key**: The TOTP secret key for two-factor authentication

## Building from Source

If you prefer to build the application from source:

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the build script:

```bash
build_exe.bat
```

4. Find the executable in the `dist` folder

## Security Note

This application is designed to run locally on your machine. Your credentials are never sent to any server other than the official Fyers API servers during the authentication process.