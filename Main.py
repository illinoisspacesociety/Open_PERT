# https://tkdocs.com/tutorial/

from tkinter import *
from tkinter import ttk

from Class import Node, timedelta
import Nodes    # this line IS NECESSARY despite the IDE suggesting otherwise
import Network


def close(win):
    win.destroy()


def callback(obj):
    newin = Toplevel(root)
    newin.title(obj.name)
    display = Label(newin, text="Test")
    display.pack()


def draw():
    # create canvas for drawing
    canvas = Canvas(root)
    canvas.grid(column=0, row=0, sticky=(N, E, W, S))
    root.columnconfigure(0, weight=30)
    root.rowconfigure(0, weight=30)

    # background
    canvas.create_rectangle(0, 0, 3000, 3000, fill="#41f461")

    # draw nodes as buttons and link dependencies with lines
    for elem, nodeObj in enumerate(Node.registry):
        button = ttk.Button(canvas, text=nodeObj.name+"\nStart: "+nodeObj.start.strftime("%m/%d/%y") +
                            "\nEnd: "+nodeObj.end.strftime("%m/%d/%y"), command=lambda: callback(nodeObj))
        button.grid(column=nodeObj.x, row=nodeObj.y, columnspan=nodeObj.dur, sticky=(W, E))

        # padding goes before getting coordinates
        for child in canvas.winfo_children():
            child.grid_configure(padx=25, pady=25)

        # collect node positional info for line connections
        canvas.pack()
        root.update_idletasks()
        nodeObj.cx = button.winfo_x()
        nodeObj.cy = button.winfo_y()
        days = nodeObj.end - Nodes.epoch
        print(button.winfo_y())
        print(nodeObj.name, "  ", nodeObj.end)

    # draw dependency lines
    for pair in Network.lines:
        obj1 = getattr(Nodes, pair[0])
        obj2 = getattr(Nodes, pair[1])
        ln = canvas.create_line(obj1.cx, obj1.cy, obj2.cx, obj2.cy)
        print(obj1.cx, obj1.cy, obj2.cx, obj2.cy)
        canvas.itemconfigure(ln, fill='orange', width=3)

    canvas.pack()


root = Tk()
root.title("Open PERT")

draw()


root.mainloop()
