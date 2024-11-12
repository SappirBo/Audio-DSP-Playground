import tkinter as tk

class EffectWindow:
    '''
    Calls of window shown for each effect, the window is dynamicly created according to the 'effect_data' dict from the effect class.
    '''
    def __init__(self, master: tk.Tk, effect_name: str, effect_data: dict, effect_callback):
        self.master = master
        self.effect_name = effect_name
        self.effect_data = effect_data

        self.add_effect_callback = effect_callback

        self.window = tk.Toplevel(self.master)
        self.window.title(f"{effect_name} Parameters")

        parameters = effect_data.get("parameters", {})

        # Dictionary to store parameter variables
        self.param_values = {}

        for param_name, param_info in parameters.items():
            tk.Label(self.window, text=param_name).pack()

            if 'p_type' not in param_info:
                raise Exception(f"p_type is not implemented for {self.effect_name}: {param_name}.")

            if param_info.get("p_type") == "button":
                button = tk.Button(
                    self.window,
                    bg="snow",
                    command=lambda: self.toggle_button(param_name, button)
                )
                button.pack()
                var = tk.BooleanVar()
                self.param_values[param_name] = var
            elif param_info.get("p_type") == "slider":
                resolution = param_info.get("step", 0.001)
                min_val = param_info.get("min", 0)
                max_val = param_info.get("max", 100)
                default = param_info.get("default", min_val)

                # Use DoubleVar or IntVar based on default value and resolution
                if isinstance(default, float) or isinstance(resolution, float):
                    var = tk.DoubleVar(value=default)
                else:
                    var = tk.IntVar(value=default)

                scale = tk.Scale(
                    self.window,
                    variable=var,
                    from_=min_val,
                    to=max_val,
                    resolution=resolution,
                    orient=tk.HORIZONTAL,
                    length=300
                )
                scale.pack()

                self.param_values[param_name] = var
            else:
                wrong_type = param_info.get("p_type")
                raise Exception(f"p_type '{wrong_type}' is not supported yet")

        # Button to apply effect
        tk.Button(
            self.window,
            text="Apply Effect",
            command=self.apply_effect
        ).pack(pady=10)

    def toggle_button(self, param_name, button)->None:
        self.param_values[param_name].set(not self.param_values[param_name].get())
        print(self.param_values[param_name].get())
        new_color = "gold3" if self.param_values[param_name].get() else "snow"
        button.config(bg=new_color)

    def apply_effect(self):
        # Retrieve parameter values
        params = {name: var.get() for name, var in self.param_values.items()}
        self.add_effect_callback(self.get_as_dict(self.effect_name, params ))
        self.window.destroy()

    def get_as_dict(self, effect_name, values) -> dict:
        return {
            "effect_name": effect_name,
            "arguments": values
        }
