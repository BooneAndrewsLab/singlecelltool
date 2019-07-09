from PIL import ImageTk, Image
from tkinter import filedialog
from pathlib import Path
import tkinter as tk
import pandas as pd
import numpy as np
import platform
import math


class Menu:
    def __init__(self, main):
        self.main = main
        self.main.title("Single Cell Labelling Tool")
        self.main.geometry("900x600")

        # Declare global variables
        self.os = platform.system()
        self.homepath = str(Path.home())
        self.global_coordfilename = tk.StringVar()
        self.global_ptypefilename = tk.StringVar()
        self.global_stats = tk.StringVar()
        self.global_labeledcellcnt = tk.IntVar()
        self.global_currentpage = tk.IntVar()
        self.global_coordext = ['csv', 'xls', 'xlsx']
        self.global_ptypeext = ['txt']
        self.global_displaycellcnt = 20
        self.global_cropsize = 30

        # Initialization
        self.global_coordfilename.set("No file chosen")
        self.global_ptypefilename.set("No file chosen")
        self.global_labeledcellcnt.set(0)
        self.global_currentpage.set(1)

        # Initial Frame - Widgets
        self.frame_initial = tk.Frame(self.main)
        self.label_coordfile = tk.Label(self.frame_initial, text="Coordinates file", width=13, anchor="w")
        self.label_ptypefile = tk.Label(self.frame_initial, text="Phenotype list", width=13, anchor="w")
        self.label_uploadedcoord = tk.Label(self.frame_initial, textvariable=self.global_coordfilename,
                                            anchor="w", wraplength=600)
        self.label_uploadedptype = tk.Label(self.frame_initial, textvariable=self.global_ptypefilename,
                                            anchor="w", wraplength=600)
        self.button_coordfile = tk.Button(self.frame_initial, text="Choose file", anchor="w", command=self.coordfile)
        self.button_ptypefile = tk.Button(self.frame_initial, text="Choose file", anchor="w", command=self.ptypefile)
        self.button_start = tk.Button(self.frame_initial, text="START", justify="left", state="disabled",
                                      command=self.start)

        # Initial Frame - Layout
        self.frame_initial.pack(fill='both', expand=True)
        self.label_coordfile.grid(row=0, column=0, padx=5, pady=5)
        self.button_coordfile.grid(row=0, column=1, padx=5, pady=5)
        self.label_uploadedcoord.grid(row=0, column=2, padx=5, pady=5)
        self.label_ptypefile.grid(row=1, column=0, padx=5, pady=5)
        self.button_ptypefile.grid(row=1, column=1, padx=5, pady=5)
        self.label_uploadedptype.grid(row=1, column=2, padx=5, pady=5)
        self.button_start.grid(row=3, column=0, padx=5, pady=15)

    def check_uploads(self):
        if (self.global_coordfilename.get() != "No file chosen") \
                and (self.global_ptypefilename.get() != "No file chosen"):
            self.coord_ext = self.global_coordfilename.get().split('.')[1]
            ptype_ext = self.global_ptypefilename.get().split('.')[1]
            if (self.coord_ext in self.global_coordext) and (ptype_ext in self.global_ptypeext):
                self.button_start.config(state="normal")
            else:
                self.button_start.config(state="disabled")
        else:
            self.button_start.config(state="disabled")

    def coordfile(self):
        coord_filename = filedialog.askopenfilename(initialdir="/home/myra/phenomics/apps/singlecell",  # self.homepath
                                                    title="Select coordinates file",
                                                    filetypes=(("CSV files", "*.csv"),
                                                               ("Excel files", "*.xls*"),
                                                               ("All files", "*.*")))
        self.global_coordfilename.set(coord_filename)
        self.check_uploads()

    def ptypefile(self):
        ptype_filename = filedialog.askopenfilename(initialdir="/home/myra/phenomics/apps/singlecell",
                                                    title="Select phenotype list file",
                                                    filetypes=(("Text files", "*.txt"),
                                                               ("All files", "*.*")))
        self.global_ptypefilename.set(ptype_filename)
        self.check_uploads()

    def start(self):
        self.frame_initial.pack_forget()

        # Process phenotype list
        ptypefile = open(self.global_ptypefilename.get(), 'r')
        self.phenotypes = [p.strip() for p in ptypefile.readlines()]

        # Main canvas display
        self.canvas_display = tk.Canvas(self.main)
        self.scroll_vertical = tk.Scrollbar(self.main, orient='vertical', command=self.canvas_display.yview)
        self.canvas_display.pack(expand='yes', fill='both', side='left')
        self.scroll_vertical.pack(fill='y', side='right')
        self.canvas_display.configure(yscrollcommand=self.scroll_vertical.set)

        if self.os == 'Linux':
            self.canvas_display.bind_all("<4>", self.on_mousewheel)
            self.canvas_display.bind_all("<5>", self.on_mousewheel)
        else:
            self.canvas_display.bind_all("<MouseWheel>", self.on_mousewheel)

        # Initialize frame display map
        self.frame_alldisplay = {}

        # Inside the canvas
        self.button_restart = tk.Button(self.canvas_display, text="HOME", command=self.restart)
        self.button_export = tk.Button(self.canvas_display, text="Export labeled data", command=self.exportdata)
        self.label_stats = tk.Label(self.canvas_display, textvariable=self.global_stats)
        self.canvas_display.create_window(10, 10, window=self.button_restart, anchor='nw')
        self.canvas_display.create_window(80, 10, window=self.button_export, anchor='nw')
        self.canvas_display.create_window(700, 10, window=self.label_stats, anchor='nw')

        # Process coordinates file
        if self.coord_ext == 'csv':
            self.coord_df = pd.read_csv(self.global_coordfilename.get())
        else:
            self.coord_df = pd.read_excel(self.global_coordfilename.get())

        self.total_cellcnt = self.coord_df.shape[0]
        self.total_batchpage = int(math.ceil(self.total_cellcnt / self.global_displaycellcnt))
        self.global_stats.set("Label count: %d out of %d" %(self.global_labeledcellcnt.get(), self.total_cellcnt))

        # self.testdf = self.coord_df[:self.global_displaycellcnt]
        self.coord_df['Label'] = [None for _i in range(self.total_cellcnt)]
        self.selected_options = [tk.StringVar(value=self.phenotypes[0]) for _i in range(self.total_cellcnt)]

        self.create_cellframes(self.coord_df, self.global_currentpage.get())  # create frame for each cell

    def create_cellframes(self, dataframe, currentpage):
        # Create new frame display
        self.frame_display = tk.Frame(self.canvas_display)
        self.frame_alldisplay[currentpage] = self.frame_display
        self.canvas_display.create_window(0, 50, window=self.frame_display, anchor='nw')

        start = (currentpage-1)*self.global_displaycellcnt
        end = currentpage*self.global_displaycellcnt
        currentbatch_df = dataframe[start:end]

        for idx, path, center_x, center_y, _ptype in currentbatch_df.itertuples():
            cellcnt = idx + 1
            x = cellcnt % self.global_displaycellcnt
            if x%2 == 0:
                if x != 0:
                    row = int(x/2) - 1
                else:
                    row = int(self.global_displaycellcnt/2) - 1
                if cellcnt == self.global_displaycellcnt:
                    if cellcnt%2 == 0:
                        col = 1
                    else:
                        row = int(cellcnt / 2)
                        col = 0
                else:
                    col = 1
            else:
                row = int(x/2)
                col = 0
            # print('\tINDEX: %d - COORDINATE: %d,%d' %(cellcnt, row, col))
            cell = self.imagecrop(path, center_x, center_y)
            cellimage = ImageTk.PhotoImage(cell)

            self.labelframe_cell = tk.LabelFrame(self.frame_display, text="", bd=3)
            self.labelframe_cell.grid(row=row, column=col, padx=10, pady=20)

            self.label_cellimage = tk.Label(self.labelframe_cell, image=cellimage)
            self.label_cellimage.image = cellimage
            self.label_cellimage.pack(side='left')

            self.optionmenu = tk.OptionMenu(self.labelframe_cell, self.selected_options[idx], *self.phenotypes)
            self.optionmenu.config(width=20)

            self.button_saveptype = tk.Button(self.labelframe_cell, text="Save", name="%s" % str(idx + 1))
            self.button_saveptype.configure(command=lambda bid=idx, bsave=self.button_saveptype,
                                                           opts=self.optionmenu: self.save_phenotype(bid, bsave, opts))

            self.button_saveptype.pack(side='bottom')
            self.optionmenu.pack(side="bottom")

        # LabelFrame for next button/batch
        self.labelframe_cell = tk.LabelFrame(self.frame_display, text="", bd=0)
        self.labelframe_cell.grid(row=row+1, column=0, columnspan=2, pady=15)
        self.button_prevbatch = tk.Button(self.labelframe_cell, text="Prev",
                                          command=lambda type='prev': self.prevnextbatch(type))
        self.button_nextbatch = tk.Button(self.labelframe_cell, text="Next",
                                          command=lambda type='next': self.prevnextbatch(type))
        self.label_batchpage = tk.Label(self.labelframe_cell, text="Batch %d of %d" % (currentpage,
                                                                                       self.total_batchpage))

        self.button_nextbatch.pack(side='right')
        self.button_prevbatch.pack(side='right')
        self.label_batchpage.pack(side='left')

        # Setup canvas scroll region
        self.frame_display.update_idletasks()
        self.canvas_display.configure(scrollregion=(0, 0, 800, self.frame_display.winfo_height() + 50))

    def prevnextbatch(self, type):
        if type == 'next':
            if self.global_currentpage.get() != self.total_batchpage:
                page = self.global_currentpage.get() + 1
            else:
                page = 1
        else:
            if self.global_currentpage.get() != 1:
                page = self.global_currentpage.get() - 1
            else:
                page = self.total_batchpage
        self.global_currentpage.set(page)
        if page in self.frame_alldisplay.keys():
            self.frame_alldisplay[page].tkraise()
        else:
            self.create_cellframes(self.coord_df, page)

    def restart(self):
        self.canvas_display.delete('all')
        self.canvas_display.pack_forget()
        self.scroll_vertical.pack_forget()
        self.frame_initial.pack(fill=tk.BOTH, expand=True)
        self.global_coordfilename.set('No file chosen')
        self.global_ptypefilename.set('No file chosen')
        self.check_uploads()

    def exportdata(self):
        outpath = filedialog.asksaveasfilename(initialdir="/home/myra/phenomics/apps/singlecell",
                                               title="Select output folder and filename")
        if outpath.endswith('.csv'):
            outpath = outpath.split('.')[0] + '.csv'
        else:
            if '.' in outpath:
                outpath = outpath.split('.')[0] + '.csv'
            outpath = outpath + '.csv'
        self.coord_df.to_csv(outpath, index=False)

    def save_phenotype(self, bid, bsave, opts):
        self.coord_df.iloc[bid, 3] = self.selected_options[bid].get()
        self.global_labeledcellcnt.set(self.global_labeledcellcnt.get() + 1)
        self.global_stats.set("Label count: %d out of %d" % (self.global_labeledcellcnt.get(), self.total_cellcnt))
        bsave.config(state="disabled", text="Saved")
        opts.config(state="disabled")

    def imagecrop(self, imagepath, center_x, center_y):
        loc_left = center_x - self.global_cropsize
        loc_upper = center_y - self.global_cropsize
        loc_right = center_x + self.global_cropsize
        loc_lower = center_y + self.global_cropsize
        image = Image.open(imagepath)
        im_arr = np.array(image).astype(float)
        im_scale = 1 / im_arr.max()
        im_new = ((im_arr * im_scale) * 255).round().astype(np.uint8)
        image = Image.fromarray(im_new)
        return image.crop((loc_left, loc_upper, loc_right, loc_lower)).resize((200, 200), Image.LANCZOS)

    def on_mousewheel(self, event):
        if self.os == 'Linux':
            scroll = -1 if event.delta > 0 else 1
            if event.num == 4:
                scroll = scroll * -1
        elif self.os == 'Windows':
            scroll = (-1) * int((event.delta / 120) * 1)
        elif self.os == 'Darwin':
            scroll = event.delta
        print('OS: %s - EVENT DELTA: %s - SCROLL: %s' % (self.os, event.delta, scroll))
        self.canvas_display.yview_scroll(scroll, "units")

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
