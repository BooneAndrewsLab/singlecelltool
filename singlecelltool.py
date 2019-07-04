import tkinter as tk
from tkinter import filedialog

class Menu:
    def __init__(self, main):
        self.main = main
        self.main.title("Single Cell Labelling Tool")
        self.main.geometry("600x200")

        # Declare global variables
        self.global_coordfilename = tk.StringVar()
        self.global_ptypefilename = tk.StringVar()

        # Initialization
        self.global_coordfilename.set("No file chosen")
        self.global_ptypefilename.set("No file chosen")

        # Widgets
        self.label_coordfile = tk.Label(self.main, text="Coordinates file", width=13, anchor="w")
        self.label_ptypefile = tk.Label(self.main, text="Phenotype list", width=13, anchor="w")
        self.label_uploadedcoord = tk.Label(self.main, textvariable=self.global_coordfilename, anchor="w", wraplength=350)
        self.label_uploadedptype = tk.Label(self.main, textvariable=self.global_ptypefilename, anchor="w", wraplength=350)
        self.button_coordfile = tk.Button(self.main, text="Choose file", anchor="w", command=self.coordfile)
        self.button_ptypefile = tk.Button(self.main, text="Choose file", anchor="w", command=self.ptypefile)
        self.button_start = tk.Button(self.main, text="START", justify="left", command=self.start)

        # Layout
        self.label_coordfile.grid(row=0, column=0, padx=5, pady=5)
        self.button_coordfile.grid(row=0, column=1, padx=5, pady=5)
        self.label_uploadedcoord.grid(row=0, column=2, padx=5, pady=5)
        self.label_ptypefile.grid(row=1, column=0, padx=5, pady=5)
        self.button_ptypefile.grid(row=1, column=1, padx=5, pady=5)
        self.label_uploadedptype.grid(row=1, column=2, padx=5, pady=5)
        self.button_start.grid(row=3, column=0, padx=5, pady=15)

    def coordfile(self):
        self.coord_filename = filedialog.askopenfilename(initialdir="/home/myra/phenomics/apps/singlecell",
                                                         title="Select file",
                                                         filetypes=(("CSV files", "*.csv"),
                                                                    ("Excel files", "*.xls*"),
                                                                    ("All files", "*.*")))
        self.global_coordfilename.set(self.coord_filename)

    def ptypefile(self):
        self.ptype_filename = filedialog.askopenfilename(initialdir="/home/myra/phenomics/apps/singlecell",
                                                         title="Select file",
                                                         filetypes=(("Text files", "*.txt"),
                                                                    ("CSV files", "*.csv"),
                                                                    ("Excel files", "*.xls*"),
                                                                    ("All files", "*.*")))

        self.global_ptypefilename.set(self.ptype_filename)

    def start(self):
        print('START')
        print('Process coordinate file: %s' %self.global_coordfilename.get())
        print('Process phenotype file: %s' %self.global_ptypefilename.get())

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()