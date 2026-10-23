# Keyboard Logger

A Python keyboard listener that prints keyboard events, appends keystrokes to
`keystrokes.log`, and emails the log through Gmail when the listener stops.
Use only on systems and with users whose permission you have to record keyboard input.

## Setup

Requires Python 3.9+ and an interactive desktop session. Run these commands from
the project directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Make a `.env` with the following variables:

```dotenv
SENDER_EMAIL=sender@gmail.com
RECEIVER_EMAIL=recipient@example.com
EMAIL_PASSWORD=your-gmail-app-password
```

The sender must be able to authenticate to Gmail's SMTP service with an app
password. Keep `.env` and `keystrokes.log` private: they contain credentials and
captured input, respectively. Existing environment variables take precedence over
values loaded from `.env`.

## Run

```powershell
.\.venv\Scripts\python.exe -m logger
```

Run from the project directory. The listener captures keyboard events across
applications, not just this terminal. It prints key presses and releases and
appends pressed keys to `keystrokes.log` in the current working directory.
Spaces, Enter, and Tab become whitespace; other special keys are recorded in
brackets, such as `[backspace]`. Backspace does not remove previously logged text.

Press **Esc** to stop the listener. During cleanup, the program closes the log and
attempts to email the entire file as an attachment using `smtp.gmail.com` on port
465 with TLS. Previous sessions remain in the file and are included in subsequent
emails. Cleanup also attempts delivery if the listener exits with an error.

Email delivery requires network access and valid credentials. Configuration and
SMTP errors are not handled by the application and can end the process with a
traceback. There is currently no option to disable email delivery.

This version runs directly from the source directory and has no package build
configuration. Install dependencies with `pip install -r requirements.txt` as
shown above. These setup and run commands do not create `build/`, `dist/`, or
`.egg-info/` directories in the repository. Python may create `__pycache__/`
directories during normal execution.

## Repository layout

- `logger/`: keyboard capture and email delivery implementation.
- `requirements.txt`: pinned direct runtime dependencies.
- `.env`: local email configuration (create this yourself; ignored by Git).

There are currently no automated tests. The application requires an interactive
desktop for keyboard capture and valid credentials and network access for email.
