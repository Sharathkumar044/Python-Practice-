import tkinter as tk
import math

# Global variables
dark_mode = False
history = []

# Colors
light_colors = {
    "bg": "#f8f9fa", "entry": "#ffffff", "text": "#000000",
    "buttons": "#e0e0e0", "operators": "#ffcc00", "special": "#ff6666",
    "equal": "#66cc66", "mode": "#6666ff"
}
dark_colors = {
    "bg": "#222831", "entry": "#393e46", "text": "#ffffff",
    "buttons": "#4e4e50", "operators": "#ffcc00", "special": "#ff4444",
    "equal": "#44c767", "mode": "#4444ff"
}

def on_click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(entry_var.get())
            history.append(f"{entry_var.get()} = {result}")
            entry_var.set(result)
            update_history()
        except Exception:
            entry_var.set("Error")
    elif text == "C":
        entry_var.set("")
    elif text == "DEL":
        entry_var.set(entry_var.get()[:-1])
    elif text == "Dark Mode":
        toggle_dark_mode()
    else:
        entry_var.set(entry_var.get() + text)

def scientific_operation(op):
    try:
        value = float(entry_var.get())
        if op == "sin":
            entry_var.set(math.sin(math.radians(value)))
        elif op == "cos":
            entry_var.set(math.cos(math.radians(value)))
        elif op == "tan":
            entry_var.set(math.tan(math.radians(value)))
        elif op == "log":
            entry_var.set(math.log10(value))
        elif op == "√":
            entry_var.set(math.sqrt(value))
        elif op == "x²":
            entry_var.set(value ** 2)
    except Exception:
        entry_var.set("Error")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    colors = dark_colors if dark_mode else light_colors
    root.config(bg=colors["bg"])
    entry.config(bg=colors["entry"], fg=colors["text"])
    history_text.config(bg=colors["entry"], fg=colors["text"])
    for btn, color in button_colors.items():
        button_dict[btn].config(bg=colors[color], fg="black")

def update_history():
    history_text.config(state="normal")
    history_text.delete("1.0", tk.END)
    history_text.insert(tk.END, "\n".join(history[-5:]))  # Show last 5 calculations
    history_text.config(state="disabled")

# Create main window
root = tk.Tk()
root.title("Modern Calculator")
root.geometry("400x600")
root.config(bg=light_colors["bg"])

# Entry widget
entry_var = tk.StringVar()
entry = tk.Entry(root, textvar=entry_var, font=("Arial", 22, "bold"), bd=10, relief="ridge",
                 justify="right", bg=light_colors["entry"], fg=light_colors["text"])
entry.pack(fill="both", ipadx=10, pady=10, padx=10)

# Button layout
buttons = [
    ["sin", "cos", "tan", "log"],
    ["√", "x²", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"],
    ["DEL", "Dark Mode"]
]

# Button colors mapping
button_colors = {"+": "operators", "-": "operators", "*": "operators", "/": "operators",
                 "sin": "operators", "cos": "operators", "tan": "operators", "log": "operators",
                 "√": "operators", "x²": "operators", "=": "equal", "C": "special", "DEL": "special",
                 "Dark Mode": "mode"}

button_dict = {}  # Store buttons for dynamic styling

# Creating buttons dynamically with modern UI
for row in buttons:
    frame = tk.Frame(root, bg=light_colors["bg"])
    frame.pack(expand=True, fill="both")
    for btn in row:
        btn_color = light_colors.get(button_colors.get(btn, "buttons"), "#e0e0e0")

        button = tk.Button(frame, text=btn, font=("Arial", 16, "bold"), relief="raised", height=2, width=5,
                           bg=btn_color, fg="black", bd=5, activebackground="#cccccc", cursor="hand2")
        button.pack(side="left", expand=True, fill="both", padx=2, pady=2)

        button_dict[btn] = button  # Store for dark mode updates

        if btn in ["sin", "cos", "tan", "log", "√", "x²"]:
            button.bind("<Button-1>", lambda e, op=btn: scientific_operation(op))
        else:
            button.bind("<Button-1>", on_click)

# History Panel
history_label = tk.Label(root, text="History", font=("Arial", 12, "bold"), bg=light_colors["bg"])
history_label.pack(pady=5)
history_text = tk.Text(root, height=5, state="disabled", font=("Arial", 10), bg=light_colors["entry"], fg=light_colors["text"])
history_text.pack(fill="both", padx=10, pady=5)

# Run the Tkinter event loop
root.mainloop()
