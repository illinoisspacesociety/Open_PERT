# https://tkdocs.com/tutorial/

from tkinter import *
from tkinter import ttk
import pickle
import copy

from Class import Node, datetime
import Nodes
from Nodes import source
from Network import allNodes


def save(canvas, win, obj, name, label, dur, dep, end):
    obj.name = name.get()
    obj.label = label.get()
    obj.dur = dur.get()
    obj.dep = dep.get().split()
    obj.end = datetime.strptime(end.get(), "%y/%m/%d")
    allNodes.append(obj)
    file = open(source, "wb")
    pickle.dump(allNodes, file)
    file.close()
    canvas.destroy()
    draw()
    win.destroy()


def callback(canvas, obj):
    newin = Toplevel(root)
    newin.title(obj.name)

    name = StringVar()
    label = StringVar()
    dur = IntVar()
    dep = StringVar()
    end = StringVar()

    lb = Label(newin, text="Name")
    lb.grid(column=0, row=1)
    lb = Label(newin, text="Label")
    lb.grid(column=0, row=2)
    lb = Label(newin, text="Duration")
    lb.grid(column=0, row=3)
    lb = Label(newin, text="Dependencies")
    lb.grid(column=0, row=4)
    lb = Label(newin, text="End Date")
    lb.grid(column=0, row=5)

    entry = ttk.Entry(newin, width=25, textvariable=name)
    entry.grid(column=1, row=1)
    entry.insert(0, obj.name)
    entry = ttk.Entry(newin, width=25, textvariable=label)
    entry.grid(column=1, row=2)
    entry.insert(0, obj.label)
    entry = ttk.Entry(newin, width=25, textvariable=dur)
    entry.grid(column=1, row=3)
    entry.delete(0, END)
    entry.insert(0, obj.dur)
    entry = ttk.Entry(newin, width=25, textvariable=dep)
    entry.grid(column=1, row=4)
    sep = " "
    entry.insert(0, sep.join(obj.dep))
    entry = ttk.Entry(newin, width=25, textvariable=end)
    entry.grid(column=1, row=5)
    entry.insert(0, obj.end.strftime("%y/%m/%d"))

    button = Button(newin, text="Save", command=lambda a=newin, b=obj,
                    n=name, lb=label, t=dur, d=dep, e=end: save(canvas, a, b, n, lb, t, d, e))
    button.grid(column=0, row=6, columnspan=2)


def callnew(canvas):
    newin = Toplevel(root)
    newin.title("New Event")

    obj = copy.deepcopy(Node.registry[0])

    name = StringVar()
    label = StringVar()
    dur = IntVar()
    dep = StringVar()
    end = StringVar()

    lb = Label(newin, text="Name")
    lb.grid(column=0, row=1)
    lb = Label(newin, text="Label")
    lb.grid(column=0, row=2)
    lb = Label(newin, text="Duration")
    lb.grid(column=0, row=3)
    lb = Label(newin, text="Dependencies")
    lb.grid(column=0, row=4)
    lb = Label(newin, text="End Date")
    lb.grid(column=0, row=5)

    entry = ttk.Entry(newin, width=25, textvariable=name)
    entry.grid(column=1, row=1)
    entry.insert(0, obj.name)
    entry = ttk.Entry(newin, width=25, textvariable=label)
    entry.grid(column=1, row=2)
    entry.insert(0, obj.label)
    entry = ttk.Entry(newin, width=25, textvariable=dur)
    entry.grid(column=1, row=3)
    entry.delete(0, END)
    entry.insert(0, obj.dur)
    entry = ttk.Entry(newin, width=25, textvariable=dep)
    entry.grid(column=1, row=4)
    sep = " "
    entry.insert(0, sep.join(obj.dep))
    entry = ttk.Entry(newin, width=25, textvariable=end)
    entry.grid(column=1, row=5)
    entry.insert(0, obj.end.strftime("%y/%m/%d"))

    button = Button(newin, text="Save", command=lambda a=newin, b=obj,
                    n=name, ln=label, t=dur, d=dep, e=end: save(canvas, a, b, n, ln, t, d, e))
    button.grid(column=0, row=6, columnspan=2)


def draw():
    import Network

    # create canvas for drawing
    canvas = Canvas(root)
    canvas.grid(column=0, row=0, sticky=(N, E, W, S))
    root.columnconfigure(0, weight=30)
    root.rowconfigure(0, weight=30)

    # background
    canvas.create_rectangle(0, 0, 3000, 3000, fill="#5e708e")

    # button for adding nodes
    button = ttk.Button(canvas, text="Add Event", command=lambda c=canvas: callnew(c))
    button.grid(column=0, row=100, columnspan=3, sticky=(W, E))

    buttons = []

    # draw nodes as buttons
    for elem, nodeObj in enumerate(allNodes):
        button = ttk.Button(canvas, text=nodeObj.label+"\nStart: "+nodeObj.start.strftime("%m/%d/%y")+"\nEnd: " +
                            nodeObj.end.strftime("%m/%d/%y"), command=lambda c=canvas, a=nodeObj: callback(c, a))
        button.grid(column=nodeObj.x, row=nodeObj.y, columnspan=40, sticky=(W, E))

        buttons.append(button)

        # padding goes before getting coordinates
        for child in canvas.winfo_children():
            child.grid_configure(padx=30, pady=30)

        canvas.pack()

    # calculate line positions
    root.update_idletasks()
    for elem, nodeObj in enumerate(allNodes):
        button = buttons[elem]
        nodeObj.ix = button.winfo_x() + 0.0 * button.winfo_width()
        nodeObj.iy = button.winfo_y() + 0.5 * button.winfo_height()
        nodeObj.ox = button.winfo_x() + 1.0 * button.winfo_width()
        nodeObj.oy = button.winfo_y() + 0.5 * button.winfo_height()

    # draw dependency lines
    for pair in Network.lines:
        obj1 = getattr(Nodes, pair[0])
        obj2 = getattr(Nodes, pair[1])
        ln = canvas.create_line(obj1.ox, obj1.oy, obj2.ix, obj2.iy)
        canvas.itemconfigure(ln, fill='orange', width=3)

    canvas.pack()


root = Tk()
root.title("Open PERT")

draw()

root.mainloop()
