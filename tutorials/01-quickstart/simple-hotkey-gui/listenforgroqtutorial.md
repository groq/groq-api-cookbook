# Build a System-Wide AI Assistant with Groq and Python

In this tutorial we will be building a simple `tkinter` GUI for interacting with a Groq API.
**Note**: This tutorial assumes a macOS/Linux system. If you are on Windows: replace `source groq-assistant/bin/activate` with `source groq-assistant\Scripts\activate`. Otherwise everything should work.
  
Requirements:
- `pynput` install via: `pip install pynput`. `pynput` is how we get input from the keyboard.
- You will need a Groq API key. You can generate one for free [here](https://console.groq.com/keys).
- I recommend setting this up in a virtual environment: `python -m venv groq-assistant` then `source groq-assistant/bin/activate`. This is where you will run all your commands, so do this before anything else. To stop this virtual environment you can just type `deactivate` in the terminal you are running this in.
- You will also need to set an environment variable with your API key: `export GROQ_API_KEY=yourkeyhere`.

## Features

**GUI Interface**: Provides a simple, non-terminal, interface for interacting with Groq models.

**Keyboard Shortcut**: Simple background listener for keyboard shortcut to open GUI.

## Usage

You will need to start the program in your virtual environment: `source groq-assistant/bin/activate && python listenforgroq.py`. Once it is running, just press Alt+G and the GUI will open up automatically. The top rectangle is for entering your prompt, the response will appear below.

## Guide to Programming `listenforgroq.py`

### Step 1: Set up dependencies

First we need to start a virtual environment and install dependencies. Open your terminal and type the following: `python -m venv groq-assistant`

Enter that environment: `source groq-assistant/bin/activate`

Now install the requirements: `pip install groq pynput`

**Note**: You can exit the virtual environment at any time by simply typing `deactivate`

Now export your [Groq API](console.groq.com/keys) key as an environment variable: `export GROQ_API_KEY=yourkeyhere`

**You do not need to close this terminal while we do the following steps.** If you do you will need to restart it: `source groq-assistant/bin/activate` and re-export your API key: `export GROQ_API_KEY=yourkeyhere`.

### Step 2: Imports and Variables

Open a new file in your favorite editing platform or IDE and paste/type the following at the top of the file:

```python
import tkinter as tk
from groq import Groq
import os
import threading
from pynput import keyboard

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
HOT_KEY={keyboard.Key.alt, keyboard.KeyCode.from_char('g')}

client = Groq(api_key=GROQ_API_KEY)
current_keys=set()
```

This initializes our client for our Groq API key. I chose to have you export your API key as an environment variable to avoid having a bunch of copies of your API keys floating around in other program files. However you can replace `os.environ.get("GROQ_API_KEY")` with your actual key if you prefer.

### Step 3: Query Groq

Now we need a method for sending our prompt to Groq:

```python
def query_groq(prompt, output_widget, root):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt} # This one
            ],
        )
        response = completion.choices[0].message.content
        root.after(0, lambda: update_output(output_widget, response))
    
    except Exception as e:
        root.after(0, lambda: update_output(output_widget, f"Error: {e}"))
```
You can use whatever model you want by replacing the value of `model` with your desired model. You can also add a system prompt by adding: `{"role": "system", "content": "Your system prompt"}` before line marked `# This one`.

### Step 4: Prepare the Window

This is the method we will use to update the displayed output in our GUI:

```python
def update_output(output_widget, text):
    output_widget.config(state="normal")
    output_widget.delete("1.0", tk.END)
    output_widget.insert(tk.END, text)
    output_widget.config(state="disabled")
```

Initialize the GUI itself:

```python
def launch_window():
    root = tk.Tk()
    root.title("Ask Groq")
    root.attributes("-topmost", True)
    root.geometry("400x300+600+400")

    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(padx=20, pady=(5, 20), fill="x")

    output = tk.Text(root, font=("Arial", 14), wrap="word", state="disabled")
    output.pack(padx=20, pady=(5, 20), fill="both", expand=True)

    def on_submission(event=None):
        prompt = entry.get()
        if prompt:
            update_output(output, "Thinking...")
            threading.Thread(target=query_groq, args=(prompt, output, root), daemon=True).start()

    entry.bind("<Return>", on_submission)
    entry.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()
```

If you want a detailed breakdown of what all this code does, finish this tutorial, run it, and paste this section of code into the input space and ask the Groq about it.

### Step 5: Keypressings and Listeners

Now to get keyboard input for our `HOT_KEY`:

```python
def on_press(key):
    if key in HOT_KEY:
        current_keys.add(key)
        if all(k in current_keys for k in HOT_KEY):
            threading.Thread(target=launch_window, daemon=True).start()

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass
```

You can customize the `on_release(key)` method to handle `KeyError` exceptions if you want to print a custom error to the user. Now we start listening for the `HOT_KEY`:

```python
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Background listener for Groq chat active")
    listener.join()
```

### Step 6: Run Forest, Run!

Now for the fun part:
- Save your file as `listenforgroq.py` or any other fun name you want to give it.
- Go back to your terminal with your virtual environment open.
- Type: `python listenforgroq.py` and press enter.
- Press Alt+G.
If everything works as it should, you will see a GUI open up and you can enter your prompt. After pressing the enter (return) key, you will be greeted with that near instantaneous response that we all know and love Groq for.

Congrats! Now, you can set this to your startup and you will be able to talk to Groq in a simple format whenever you want.