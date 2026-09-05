import tkinter as tk
from tkinter import ttk
import math


class LuminaEngine:

    def __init__(self):
        self.memory = 0.0
        self.history = []

    def evaluate(self, expression: str) -> str:
        try:
            # Replace visual symbols with Python mathematical equivalents
            formatted_expr = (
                expression.replace("×", "*")
                .replace("÷", "/")
                .replace("^", "**")
                .replace("π", "math.pi")
                .replace("e", "math.e")
            )

            # Define safe scope for evaluation
            safe_dict = {
                "math": math,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "factorial": math.factorial,
                "pi": math.pi,
                "e": math.e,
            }

            result = eval(formatted_expr, {"__builtins__": None}, safe_dict)

            # Format integer vs floating results
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)

            self.history.append(f"{expression} = {result}")
            return str(result)
        except ZeroDivisionError:
            return "Error: Division by Zero"
        except Exception:
            return "Error: Invalid Expression"


class LuminaMath(tk.Tk):

    def __init__(self):
        super().__init__()
        self.engine = LuminaEngine()

        self.title("SimpleCalc")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg="#1E1E2E")

        self.expression = ""
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Color Palette
        self.colors = {
            "bg": "#1E1E2E",
            "display_bg": "#181825",
            "text": "#CDD6F4",
            "num_bg": "#313244",
            "op_bg": "#89B4FA",
            "op_fg": "#11111B",
            "fn_bg": "#45475A",
            "action_bg": "#F38BA8",
            "action_fg": "#11111B",
        }

    def _build_ui(self):
        # Display Area
        display_frame = tk.Frame(self, bg=self.colors["display_bg"])
        display_frame.pack(fill="x", padx=15, pady=15)

        self.history_label = tk.Label(
            display_frame,
            text="",
            anchor="e",
            bg=self.colors["display_bg"],
            fg="#A6ADC8",
            font=("Consolas", 11),
        )
        self.history_label.pack(fill="x", padx=10, pady=(10, 0))

        self.main_display = tk.Label(
            display_frame,
            text="0",
            anchor="e",
            bg=self.colors["display_bg"],
            fg=self.colors["text"],
            font=("Consolas", 26, "bold"),
        )
        self.main_display.pack(fill="x", padx=10, pady=(0, 10))

        # Button Grid Layout
        button_frame = tk.Frame(self, bg=self.colors["bg"])
        button_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Config layout matrix
        buttons = [
            ("MC", "MR", "M+", "C", "DEL"),
            ("sin", "cos", "tan", "√", "^"),
            ("log", "ln", "(", ")", "÷"),
            ("7", "8", "9", "×", "%"),
            ("4", "5", "6", "-", "π"),
            ("1", "2", "3", "+", "e"),
            ("0", ".", "±", "=", "x!"),
        ]

        for r_idx, row in enumerate(buttons):
            button_frame.rowconfigure(r_idx, weight=1)
            for c_idx, symbol in enumerate(row):
                button_frame.columnconfigure(c_idx, weight=1)
                self._create_button(button_frame, symbol, r_idx, c_idx)

        # Keyboard Bindings
        self.bind("<Return>", lambda e: self._on_action("="))
        self.bind("<BackSpace>", lambda e: self._on_action("DEL"))
        self.bind("<Escape>", lambda e: self._on_action("C"))
        self.bind("<Key>", self._on_key_press)

    def _create_button(self, parent, text, row, col):
        bg_color, fg_color = self._get_button_colors(text)

        btn = tk.Button(
            parent,
            text=text,
            bg=bg_color,
            fg=fg_color,
            activebackground=self.colors["text"],
            activeforeground=self.colors["bg"],
            font=("Consolas", 12, "bold"),
            relief="flat",
            bd=0,
            command=lambda: self._on_action(text),
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

    def _get_button_colors(self, text):
        if text in ["=", "C"]:
            return self.colors["action_bg"], self.colors["action_fg"]
        elif text in ["+", "-", "×", "÷", "^"]:
            return self.colors["op_bg"], self.colors["op_fg"]
        elif text.isdigit() or text == ".":
            return self.colors["num_bg"], self.colors["text"]
        else:
            return self.colors["fn_bg"], self.colors["text"]

    def _on_action(self, char):
        if char == "C":
            self.expression = ""
            self.main_display.config(text="0")
            self.history_label.config(text="")
        elif char == "DEL":
            self.expression = self.expression[:-1]
            self.main_display.config(
                text=self.expression if self.expression else "0"
            )
        elif char == "=":
            if self.expression:
                result = self.engine.evaluate(self.expression)
                self.history_label.config(text=f"{self.expression} =")
                self.main_display.config(text=result)
                self.expression = str(result) if "Error" not in result else ""
        elif char in ["sin", "cos", "tan", "log", "ln"]:
            self.expression += f"{char}("
            self.main_display.config(text=self.expression)
        elif char == "√":
            self.expression += "sqrt("
            self.main_display.config(text=self.expression)
        elif char == "x!":
            self.expression += "factorial("
            self.main_display.config(text=self.expression)
        elif char == "±":
            if self.expression and self.expression[0] == "-":
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.main_display.config(text=self.expression)
        elif char == "M+":
            try:
                val = float(self.main_display.cget("text"))
                self.engine.memory += val
            except ValueError:
                pass
        elif char == "MR":
            self.expression += str(self.engine.memory)
            self.main_display.config(text=self.expression)
        elif char == "MC":
            self.engine.memory = 0.0
        else:
            self.expression += char
            self.main_display.config(text=self.expression)

    def _on_key_press(self, event):
        key = event.char
        if key in "0123456789.+-*/()":
            if key == "*":
                key = "×"
            elif key == "/":
                key = "÷"
            self._on_action(key)


if __name__ == "__main__":
    app = LuminaMath()
    app.mainloop()