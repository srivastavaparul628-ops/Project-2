import tkinter as tk
import math


# -----------------------------
# MAIN APP
# -----------------------------
class AdvancedCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Calculator")
        self.geometry("420x600")
        self.resizable(False, False)
        self.config(bg="#222")

        # Display Frame
        self.display = DisplayFrame(self)
        self.display.pack(fill="x", pady=10)

        # Frame that holds all buttons
        self.button_container = tk.Frame(self, bg="#222")
        self.button_container.pack(expand=True, fill="both")

        # Two modes
        self.basic = BasicMode(self.button_container, self)
        self.scientific = ScientificMode(self.button_container, self)

        # Show Basic by default
        self.basic.pack(fill="both", expand=True)

        # Toggle Button
        self.create_mode_button()

    def create_mode_button(self):
        tk.Button(
            self,
            text="Switch",
            bg="#444",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            command=self.toggle_mode
        ).pack(pady=5)

    def toggle_mode(self):
        if self.basic.winfo_ismapped():
            self.basic.pack_forget()
            self.scientific.pack(fill="both", expand=True)
        else:
            self.scientific.pack_forget()
            self.basic.pack(fill="both", expand=True)


# -----------------------------
# DISPLAY FRAME
# -----------------------------
class DisplayFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#222")

        self.var = tk.StringVar()
        self.entry = tk.Entry(
            self,
            textvariable=self.var,
            font=("Segoe UI", 28),
            bg="#111",
            fg="white",
            insertbackground="white",
            relief="flat",
            justify="right"
        )
        self.entry.pack(fill="x", ipady=20, padx=10)

    def add(self, char):
        self.var.set(self.var.get() + str(char))

    def delete(self):
        self.var.set(self.var.get()[:-1])

    def clear(self):
        self.var.set("")

    def evaluate(self):
        expression = self.var.get()
        try:
            expression = expression.replace("^", "**")
            result = str(eval(expression, {"__builtins__": None}, math.__dict__))
            self.var.set(result)
        except:
            self.var.set("Error")


# -----------------------------
# BASIC MODE BUTTONS
# -----------------------------
class BasicMode(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#222")
        self.app = app

        layout = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["AC", "DEL"]
        ]

        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                self.make_button(char).grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

        # Expand grid
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(len(layout)):
            self.grid_rowconfigure(i, weight=1)

    def make_button(self, char):
        return tk.Button(
            self,
            text=char,
            bg="#333",
            fg="white",
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            command=lambda c=char: self.process(c)
        )

    def process(self, char):
        disp = self.app.display

        if char == "=":
            disp.evaluate()
        elif char == "AC":
            disp.clear()
        elif char == "DEL":
            disp.delete()
        else:
            disp.add(char)


# -----------------------------
# SCIENTIFIC MODE BUTTONS
# -----------------------------
class ScientificMode(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#222")
        self.app = app

        scientific_buttons = [
            ["sin(", "cos(", "tan(", "log("],
            ["sqrt(", "pi", "e", "^"],
            ["(", ")", "AC", "DEL"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]

        for r, row in enumerate(scientific_buttons):
            for c, char in enumerate(row):
                self.make_button(char).grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

        # Expand grid
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(len(scientific_buttons)):
            self.grid_rowconfigure(i, weight=1)

    def make_button(self, char):
        return tk.Button(
            self,
            text=char,
            bg="#555" if char in ["sin(", "cos(", "tan(", "log(", "sqrt("] else "#333",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            relief="flat",
            command=lambda c=char: self.process(c)
        )

    def process(self, char):
        disp = self.app.display

        if char == "=":
            disp.evaluate()
        elif char == "AC":
            disp.clear()
        elif char == "DEL":
            disp.delete()
        elif char in ["pi", "e"]:
            disp.add(str(getattr(math, char)))
        else:
            disp.add(char)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app = AdvancedCalculatorApp()
    app.mainloop()