from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter as tk
import pandas as pd
import numpy as np
import platform
import math
import os


class Menu:
    def __init__(self, main):
        self.main = main
        self.main.title("Single Cell Labelling Tool")
        self.main.geometry("900x600")

        # Declare global variables
        self.os = platform.system()
        self.homepath = os.path.expanduser('~')
        self.global_coordfilename = tk.StringVar()
        self.global_ptypefilename = tk.StringVar()
        self.global_stats = tk.StringVar()
        self.global_labeledcellcnt = tk.IntVar()
        self.global_currentpage = tk.IntVar()
        self.global_displaycellcnt = tk.IntVar()
        self.global_cropsize = tk.IntVar()
        self.global_limitcell = tk.StringVar()
        self.global_colcount = tk.IntVar()
        self.global_coordext = ['csv', 'xls', 'xlsx']
        self.global_ptypeext = ['txt']

        # Initialization
        self.initialize()

        # Initial Frame - Widgets
        self.frame_initial = tk.Frame(self.main)
        self.label_coordfile = tk.Label(self.frame_initial, text="Cell data file", width=13, anchor="w")
        self.label_ptypefile = tk.Label(self.frame_initial, text="Phenotype list", width=13, anchor="w")
        self.label_uploadedcoord = tk.Label(self.frame_initial, textvariable=self.global_coordfilename,
                                            anchor="w", wraplength=600)
        self.label_uploadedptype = tk.Label(self.frame_initial, textvariable=self.global_ptypefilename,
                                            anchor="w", wraplength=600)

        self.label_limitcell = tk.Label(self.frame_initial, text="Cell count", width=13, anchor="w")
        self.entry_limitcell = tk.Entry(self.frame_initial, textvariable=self.global_limitcell, width=12)
        self.label_defaultlimitcell = tk.Label(self.frame_initial, text="Total cells to be processed from the "
                                                                        "input file. This is optional. "
                                                                        "By default, all cells will be processed.")

        self.label_displaycell = tk.Label(self.frame_initial, text="Display limit", width=13, anchor="w")
        self.entry_displaycell = tk.Entry(self.frame_initial, textvariable=self.global_displaycellcnt, width=12)
        self.label_defaultdisplaycell = tk.Label(self.frame_initial, text="Number of cells to be displayed on a "
                                                                          "single page. The default is 20.")

        self.label_cropsize = tk.Label(self.frame_initial, text="Crop size", width=13, anchor="w")
        self.entry_cropsize = tk.Entry(self.frame_initial, textvariable=self.global_cropsize, width=12)
        self.label_defaultcropsize = tk.Label(self.frame_initial, text="Pixel size to be used in cropping cells "
                                                                       "from the image. The default is 50.")

        self.button_coordfile = tk.Button(self.frame_initial, text="Choose file", anchor="w", command=self.coordfile)
        self.button_ptypefile = tk.Button(self.frame_initial, text="Choose file", anchor="w", command=self.ptypefile)
        self.button_start = tk.Button(self.frame_initial, text="START", state="disabled", command=self.start)

        # Initial Frame - Layout
        self.frame_initial.pack(fill='both', expand=True)
        self.label_coordfile.grid(row=0, column=0, padx=5, pady=5)
        self.button_coordfile.grid(row=0, column=1, padx=5, pady=5)
        self.label_uploadedcoord.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.label_ptypefile.grid(row=1, column=0, padx=5, pady=5)
        self.button_ptypefile.grid(row=1, column=1, padx=5, pady=5)
        self.label_uploadedptype.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.label_limitcell.grid(row=2, column=0, padx=5, pady=5)
        self.entry_limitcell.grid(row=2, column=1, padx=5, pady=5)
        self.label_defaultlimitcell.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.label_displaycell.grid(row=3, column=0, padx=5, pady=5)
        self.entry_displaycell.grid(row=3, column=1, padx=5, pady=5)
        self.label_defaultdisplaycell.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.label_cropsize.grid(row=4, column=0, padx=5, pady=5)
        self.entry_cropsize.grid(row=4, column=1, padx=5, pady=5)
        self.label_defaultcropsize.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.button_start.grid(row=6, column=0, padx=5, pady=15, sticky="w")

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
        self.canvas_allframes = {}

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

        try:
            self.total_cellcnt = int(self.global_limitcell.get())
            self.coord_df = self.coord_df[:self.total_cellcnt]
        except ValueError:
            self.total_cellcnt = self.coord_df.shape[0]

        self.global_colcount.set(self.coord_df.shape[1])

        self.total_batchpage = int(math.ceil(self.total_cellcnt / self.global_displaycellcnt.get()))
        self.global_stats.set("Label count: %d out of %d" %(self.global_labeledcellcnt.get(), self.total_cellcnt))

        # self.testdf = self.coord_df[:self.global_displaycellcnt.get()]
        self.coord_df['Saved Label'] = [None for _i in range(self.total_cellcnt)]
        self.selected_options = [tk.StringVar(value=self.phenotypes[0]) for _i in range(self.total_cellcnt)]

        self.create_cellframes(self.coord_df, self.global_currentpage.get())  # create frame for each cell

    def create_cellframes(self, dataframe, currentpage):
        # Create new frame display
        self.frame_display = tk.Frame(self.canvas_display)
        self.frame_alldisplay[currentpage] = self.frame_display
        self.canvas_allframes[currentpage] = self.canvas_display.create_window(0, 50, window=self.frame_display,
                                                                               anchor='nw')

        start = (currentpage-1)*self.global_displaycellcnt.get()
        end = currentpage*self.global_displaycellcnt.get()
        currentbatch_df = dataframe[start:end]

        pos = 1
        for idx, path, center_x, center_y in currentbatch_df.iloc[:,:3].itertuples():
            modpos = pos % 2
            if modpos == 0:
                row = int(pos/2) - 1
                col = 1
            else:
                row = int(pos/2)
                col = 0

            # print('\tINDEX: %d - POSITION: %s - COORDINATE: %d,%d' %(idx+1, pos, row, col))
            pos += 1
            cell = self.imagecrop(path, center_x, center_y)
            cellimage = ImageTk.PhotoImage(cell)

            self.labelframe_cell = tk.LabelFrame(self.frame_display, text="%d" %(idx+1), bd=3)
            self.labelframe_cell.grid(row=row, column=col, padx=10, pady=20)

            self.label_cellimage = tk.Label(self.labelframe_cell, image=cellimage)
            self.label_cellimage.image = cellimage
            # self.label_cellimage.pack(side="left")
            self.label_cellimage.grid(row=0, column=0, sticky="nw", rowspan=5)

            self.label_cellpath = tk.Label(self.labelframe_cell, text="%s" % os.path.basename(path).split('.')[0])
            self.label_cellcoord = tk.Label(self.labelframe_cell, text="x=%s, y=%s" % (center_x, center_y))

            if self.global_colcount.get() == 4:
                self.label_initiallabel = tk.Label(self.labelframe_cell, wraplength=200,
                                                   text="Initial label: %s" % self.coord_df.iloc[idx, 3])

            self.optionmenu = tk.OptionMenu(self.labelframe_cell, self.selected_options[idx], *self.phenotypes)
            self.optionmenu.config(width=20)

            self.button_saveptype = tk.Button(self.labelframe_cell, text="Save", name="%s" % str(idx + 1))
            self.button_saveptype.configure(command=lambda bid=idx, bsave=self.button_saveptype,
                                                           opts=self.optionmenu: self.save_phenotype(bid, bsave, opts))

            self.label_cellpath.grid(row=0, column=1, sticky="w", padx=5, pady=(20,0))
            self.label_cellcoord.grid(row=1, column=1, sticky="w", padx=5, pady=0)
            if self.global_colcount.get() == 4:
                self.label_initiallabel.grid(row=2, column=1, sticky="w", padx=5, pady=0)
            self.optionmenu.grid(row=3, column=1, padx=5, pady=(20, 0))
            self.button_saveptype.grid(row=4, column=1, padx=5, pady=0)


        # LabelFrame for next button/batch
        self.labelframe_cell = tk.LabelFrame(self.frame_display, text="", bd=0)
        self.labelframe_cell.grid(row=row+1, column=0, columnspan=2, pady=15)

        if self.total_batchpage > 1:
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
        self.canvas_display.yview_moveto(0)
        self.canvas_display.configure(scrollregion=(0, 0, self.frame_display.winfo_width(),
                                                    self.labelframe_cell.winfo_y() + 90))


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
            self.canvas_display.yview_moveto(0)
            self.canvas_display.configure(scrollregion=(0, 0, self.frame_alldisplay[page].winfo_width(),
                                                        self.frame_alldisplay[page].winfo_height() + 45))
            self.frame_alldisplay[page].tkraise()
            self.canvas_display.itemconfigure(self.canvas_allframes[page], state='normal')
            for p in self.frame_alldisplay.keys():
                if p != page:
                    self.canvas_display.itemconfigure(self.canvas_allframes[p], state='hidden')
        else:
            for p in self.frame_alldisplay.keys():
                if p != page:
                    self.canvas_display.itemconfigure(self.canvas_allframes[p], state='hidden')
            self.create_cellframes(self.coord_df, page)

    def initialize(self):
        self.global_coordfilename.set("No file chosen")
        self.global_ptypefilename.set("No file chosen")
        self.global_labeledcellcnt.set(0)
        self.global_currentpage.set(1)
        self.global_displaycellcnt.set(20)
        self.global_cropsize.set(50)
        self.global_limitcell.set("")
        self.global_colcount.set(0)

    def restart(self):
        self.canvas_display.delete('all')
        self.canvas_display.pack_forget()
        self.scroll_vertical.pack_forget()
        self.frame_initial.pack(fill=tk.BOTH, expand=True)
        self.initialize()

        # self.frame_alldisplay = {}
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
        self.coord_df.iloc[bid, self.global_colcount.get()] = self.selected_options[bid].get()
        self.global_labeledcellcnt.set(self.global_labeledcellcnt.get() + 1)
        self.global_stats.set("Label count: %d out of %d" % (self.global_labeledcellcnt.get(), self.total_cellcnt))
        bsave.config(state="disabled", text="Saved")
        opts.config(state="disabled")

    def imagecrop(self, imagepath, center_x, center_y):
        loc_left = center_x - self.global_cropsize.get()/2
        loc_upper = center_y - self.global_cropsize.get()/2
        loc_right = center_x + self.global_cropsize.get()/2
        loc_lower = center_y + self.global_cropsize.get()/2
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
        else:
            scroll = 1
        self.canvas_display.yview_scroll(scroll, "units")

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
