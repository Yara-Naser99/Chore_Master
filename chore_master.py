import tkinter as tk
from tkinter import ttk

from Interval import Interval
from chore_type import chore_type
from schedule_generator import generate_schedule_using_ga


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.var_0_1 = tk.BooleanVar()
        self.var_0_2 = tk.BooleanVar()
        self.var_0_3 = tk.BooleanVar()
        self.var_0_4 = tk.BooleanVar()
        self.var_0_5 = tk.BooleanVar()
        self.var_0_6 = tk.BooleanVar()
        self.var_0_7 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)
        self.availabilities = []

        self.setup_widgets()

    def setup_widgets(self):
        # Create a Frame for the Checkbuttons
        self.check_frame = ttk.LabelFrame(self, text="Chore Types", padding=(20, 10))
        self.check_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        # Checkbuttons
        self.check_1 = ttk.Checkbutton(
            self.check_frame, text="Cleaning", variable=self.var_0_1, onvalue=True, offvalue=False
        )
        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.check_2 = ttk.Checkbutton(
            self.check_frame, text="Cooking", variable=self.var_0_2, onvalue=True, offvalue=False
        )
        self.check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.check_3 = ttk.Checkbutton(
            self.check_frame, text="Sweeping", variable=self.var_0_3, onvalue=True, offvalue=False
        )
        self.check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.check_4 = ttk.Checkbutton(
            self.check_frame, text="Grocery", variable=self.var_0_4, onvalue=True, offvalue=False
        )
        self.check_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.check_5 = ttk.Checkbutton(
            self.check_frame, text="Gardening", variable=self.var_0_5, onvalue=True, offvalue=False
        )
        self.check_5.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        self.check_6 = ttk.Checkbutton(
            self.check_frame, text="Ironing", variable=self.var_0_6, onvalue=True, offvalue=False
        )
        self.check_6.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

        self.check_7 = ttk.Checkbutton(
            self.check_frame, text="Dishes", variable=self.var_0_7, onvalue=True, offvalue=False
        )
        self.check_7.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Create a Frame for the Radiobuttons
        self.radio_frame = ttk.LabelFrame(self, text="Number of Housemates", padding=(20, 10))
        self.radio_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")

        def read_checkboxes():
            chore_duration_dict = {}
            if (self.var_0_1.get()):
                chore_duration_dict[chore_type.cleaning] = 2
            if (self.var_0_2.get()):
                chore_duration_dict[chore_type.cooking] = 1
            if (self.var_0_3.get()):
                chore_duration_dict[chore_type.sweeping] = 1
            if (self.var_0_4.get()):
                chore_duration_dict[chore_type.grocery] = 2
            if (self.var_0_5.get()):
                chore_duration_dict[chore_type.gardening] = 1
            if (self.var_0_6.get()):
                chore_duration_dict[chore_type.ironing] = 1
            if (self.var_0_7.get()):
                chore_duration_dict[chore_type.dishes] = 1
            return chore_duration_dict

        def read_availabilities(availabilities):
            housemate_ids_availability_dict = {}
            for i, availability in enumerate(availabilities):
                parts = availability.split('-')
                if len(parts) != 2:
                    # Skip invalid availability data
                    continue
                try:
                    start, end = map(int, parts)
                    housemate_ids_availability_dict[i + 1] = Interval(start, end)
                except ValueError:
                    # Skip invalid integer conversion
                    continue
            return housemate_ids_availability_dict

        def enter_availabilities():
            for widget in self.widgets_frame.winfo_children():
                widget.destroy()
            housemate_count = int(self.spinbox.get())
            entry_values = []
            for i in range(housemate_count):
                self.entry = ttk.Entry(self.widgets_frame)
                self.entry.insert(0, "")
                self.entry.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="ew")
                entry_values.append(self.entry)

            def update_availabilities():
                self.availabilities = [entry.get() for entry in entry_values]
                generate_schedules()  # Call the function to generate schedules after updating availabilities

            button = ttk.Button(self.widgets_frame, text="Generate Top Two Solutions", command=update_availabilities)
            button.grid(row=housemate_count, column=0, padx=5, pady=10, sticky="nsew")

            """    """

        def generate_schedules():
            chore_duration_dict = read_checkboxes()
            housemate_ids_availability_dict = read_availabilities(self.availabilities)
            self.paned = ttk.PanedWindow(self)
            self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

            self.pane_1 = ttk.Frame(self.paned, padding=5)
            self.paned.add(self.pane_1, weight=1)

            generate_schedule_using_ga(self.pane_1, chore_duration_dict, housemate_ids_availability_dict)

        # Radiobuttons
        # Spinbox
        self.spinbox = ttk.Spinbox(self.radio_frame, from_=1, to=10, increment=1)
        self.spinbox.insert(0, "0")
        self.spinbox.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.button = ttk.Button(self.radio_frame, text="Enter Housemates Availabilities", command=enter_availabilities)
        self.button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        self.widgets_frame = ttk.LabelFrame(self, text="Availabilities (e.g., 10-13)",
                                            padding=(20, 10))  # padding=(20, 10)
        self.widgets_frame.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew"
        )

        self.widgets_frame.columnconfigure(index=0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chore Master")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    root.mainloop()
