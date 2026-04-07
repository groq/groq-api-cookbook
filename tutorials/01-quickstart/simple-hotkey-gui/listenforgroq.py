"""
Step 1: Set Up Dependencies
"""

# Setup the virtual environment: python -m venv groq-assistant
# Install dependencies: pip install groq pynput
# Export your API key: export GROQ_API_KEY=yourkeyhere



"""
Step 2: Imports and Variables
"""

import tkinter as tk
from groq import Groq
import os
import threading
from pynput import keyboard

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
HOT_KEY={keyboard.Key.alt, keyboard.KeyCode.from_char('g')}

client = Groq(api_key=GROQ_API_KEY)
current_keys=set()



"""
Step 3: Query Groq
"""

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



"""
Step 4: Prepare the Window
"""

def update_output(output_widget, text):
    output_widget.config(state="normal")
    output_widget.delete("1.0", tk.END)
    output_widget.insert(tk.END, text)
    output_widget.config(state="disabled")

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


"""
Step 5: Keypressings and Listeners
"""

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


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Background listener for Groq chat active")
    listener.join()



"""
Step 6: Run Forest, Run!
"""

# Open your virtual environment if not already open:
# bash: source groq-assistant/bin/activate
#
# Run the following command:
# bash: python listenforgroq.py
#
# Press Alt+G anywhere and the GUI will open automatically
#
# Enjoy! 😀