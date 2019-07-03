import tkinter as tk
from tkinter import filedialog
def selectfile():
    filename = filedialog.askopenfilename(initialdir = "/home",
                                          title = "Select file",
                                          filetypes = (("csv files","*.csv"),
                                                       ("Excel files", "*.xlsx"),
                                                       ("all files","*.*")))
    print('FILENAME: %s' %filename)


# Main window
main = tk.Tk()
main.title("Single Cell Labelling Tool")

# Widgets
button = tk.Button(main, text="Select file", command=selectfile)
button.pack(padx=5, pady=5)
# Run!
main.mainloop()