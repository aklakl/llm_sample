import tkinter as tk
def create_main_window():
    window = tk.Tk()
    button = tk.Button(window, text="Click me!", command=lambda: handle_button_click())
    button.pack()
    window.mainloop()
def handle_button_click():
    print("Button clicked!")