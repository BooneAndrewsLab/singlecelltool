from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter as tk
import pandas as pd
import numpy as np


class Menu:
    def __init__(self, main):
        self.main = main
        self.main.title("Single Cell Labelling Tool")
        self.main.geometry("600x200")

        # Declare global variables
        self.global_coordfilename = tk.StringVar()
        self.global_ptypefilename = tk.StringVar()
        self.allowed_coordext = ['csv', 'xls', 'xlsx']
        self.allowed_ptypeext = ['txt']
        self.display_cellcount = 10
        self.display_cropsize = 30

        # Initialization
        self.global_coordfilename.set("No file chosen")
        self.global_ptypefilename.set("No file chosen")

        # Initial Frame - Widgets
        self.frame_initial = tk.Frame(self.main)
        self.label_coordfile = tk.Label(self.frame_initial, text="Coordinates file", width=13, anchor="w")
        self.label_ptypefile = tk.Label(self.frame_initial, text="Phenotype list", width=13, anchor="w")
        self.label_uploadedcoord = tk.Label(self.frame_initial, textvariable=self.global_coordfilename, anchor="w", wraplength=350)
        self.label_uploadedptype = tk.Label(self.frame_initial, textvariable=self.global_ptypefilename, anchor="w", wraplength=350)
        self.button_coordfile = tk.Button(self.frame_initial, text="Choose file", anchor="w", command=self.coordfile)
        self.button_ptypefile = tk.Button(self.frame_initial, text="Choose file", anchor="w", command=self.ptypefile)
        self.button_start = tk.Button(self.frame_initial, text="START", justify="left", state="disabled", command=self.start)

        # Initial Frame - Layout
        self.frame_initial.pack(fill=tk.BOTH, expand=True)
        self.label_coordfile.grid(row=0, column=0, padx=5, pady=5)
        self.button_coordfile.grid(row=0, column=1, padx=5, pady=5)
        self.label_uploadedcoord.grid(row=0, column=2, padx=5, pady=5)
        self.label_ptypefile.grid(row=1, column=0, padx=5, pady=5)
        self.button_ptypefile.grid(row=1, column=1, padx=5, pady=5)
        self.label_uploadedptype.grid(row=1, column=2, padx=5, pady=5)
        self.button_start.grid(row=3, column=0, padx=5, pady=15)

    def check_uploads(self):
        if (self.global_coordfilename.get() != "No file chosen") \
                and (self.global_ptypefilename.get()!= "No file chosen"):
            self.coord_ext = self.global_coordfilename.get().split('.')[1]
            self.ptype_ext = self.global_ptypefilename.get().split('.')[1]
            if (self.coord_ext in self.allowed_coordext) and (self.ptype_ext in self.allowed_ptypeext):
                self.button_start.config(state="normal")
            else:
                self.button_start.config(state="disabled")
        else:
            self.button_start.config(state="disabled")

    def coordfile(self):
        self.coord_filename = filedialog.askopenfilename(initialdir="/home/myra/phenomics/apps/singlecell",
                                                         title="Select coordinates file",
                                                         filetypes=(("CSV files", "*.csv"),
                                                                    ("Excel files", "*.xls*"),
                                                                    ("All files", "*.*")))
        self.global_coordfilename.set(self.coord_filename)
        self.check_uploads()

    def ptypefile(self):
        self.ptype_filename = filedialog.askopenfilename(initialdir="/home/myra/phenomics/apps/singlecell",
                                                         title="Select phenotype list file",
                                                         filetypes=(("Text files", "*.txt"),
                                                                    ("All files", "*.*")))
        self.global_ptypefilename.set(self.ptype_filename)
        self.check_uploads()

    def start(self):
        self.frame_initial.pack_forget()
        # Display Frame - Widgets
        self.canvas_display = tk.Canvas(self.main, yscrollincrement=2, scrollregion=(0,0,500,500))
        self.scroll_y = tk.Scrollbar(self.canvas_display, orient="vertical", command=self.canvas_display.yview)
        self.scroll_y.pack(side='right', fill='y')
        self.canvas_display.configure(yscrollcommand=self.scroll_y.set)

        self.frame_display = tk.Frame(self.canvas_display)
        # self.label_test = tk.Label(self.frame_display, text="View single cells")

        # Display Frame - Layout
        self.canvas_display.pack(fill=tk.BOTH, expand=True)
        self.frame_display.pack(fill=tk.BOTH, expand=True)
        # self.label_test.grid(row=0, column=0, padx=5, pady=5)

        # Process phenotype list
        ptypefile = open(self.global_ptypefilename.get(), 'r')
        self.phenotypes = [p.strip() for p in ptypefile.readlines()]

        # Process coordinate file
        if self.coord_ext == 'csv':
            self.coord_df = pd.read_csv(self.global_coordfilename.get())
        else:
            self.coord_df = pd.read_excel(self.global_coordfilename.get())

        testdf = self.coord_df[:10]
        for idx, path, center_x, center_y in testdf.itertuples():
            cellcnt = idx + 1
            x = cellcnt % self.display_cellcount
            if x%2 == 0:
                col = 1
                if x != 0:
                    row = int(x/2) - 1
                else:
                    row = int(cellcnt/2) - 1
            else:
                row = int(x/2)
                col = 0

            # print('INDEX: %d - COORDINATE: %d,%d' %(cellcnt, row, col))
            cell = self.imagecrop(path, center_x, center_y)
            cellimage = ImageTk.PhotoImage(cell)
            self.label_cellimage = tk.Label(self.frame_display, image=cellimage)
            self.label_cellimage.image = cellimage
            self.label_cellimage.grid(row=row, column=col, padx=25, pady=15)

    def imagecrop(self, imagepath, center_x, center_y):
        loc_left = center_x - self.display_cropsize
        loc_upper = center_y - self.display_cropsize
        loc_right = center_x + self.display_cropsize
        loc_lower = center_y + self.display_cropsize
        image = Image.open(imagepath)
        im_arr = np.array(image).astype(float)
        im_scale = 1 / im_arr.max()
        im_new = ((im_arr * im_scale) * 255).round().astype(np.uint8)
        image = Image.fromarray(im_new)
        return image.crop((loc_left, loc_upper, loc_right, loc_lower)).resize((200,200), Image.LANCZOS)


if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()