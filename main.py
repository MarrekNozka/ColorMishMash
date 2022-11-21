#!/usr/bin/env python3

# from os.path import basename, splitext
import tkinter as tk
from tkinter import Label, Button, Scale, Entry, Frame, Canvas, Checkbutton
from colorsys import rgb_to_hsv, hsv_to_rgb
from functools import partial

# from tkinter import ttk


class ScaleFrame(Frame):
    def __init__(self, master=None, cnf={}, label="", from_=0, to=0xFF, **kw):
        self.from_ = from_
        self.to = to

        super().__init__(master)

        self.var = tk.IntVar(self, 0, "var{}".format(label))

        self.label = Label(self, text=label)

        self.scale = Scale(
            self,
            from_=self.from_,
            to=self.to,
            showvalue=0,
            orient="horizontal",
            length=330,
            variable=self.var,
        )

        self.entry = Entry(self, width=5, textvariable=self.var)

        self.canvas = Canvas(self, width=300, height=12)

        self.scale.bind("<Button-4>", self.up)
        self.entry.bind("<Button-4>", self.up)
        self.scale.bind("<Button-5>", self.down)
        self.entry.bind("<Button-5>", self.down)

        self.label.grid(row="1", column=0, sticky="s")
        self.scale.grid(row="1", column=1, sticky="s")
        self.entry.grid(row="1", column=2, sticky="s")
        self.canvas.grid(row="0", column=1, sticky="n")

    @property
    def value(self):
        return self.var.get()

    @value.setter
    def value(self, new):
        self.var.set(new)

    def up(self, event=None):
        if self.value < self.to:
            self.value += 1

    def down(self, event=None):
        if self.value > self.from_:
            self.value -= 1


class Application(tk.Tk):
    name = "ColorMishMash"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        self.bind("<Escape>", self.quit)

        self.lblMain = Label(self, text="ColorMishMash")

        self.frameR = ScaleFrame(self, label="R")
        self.frameR.label.config(fg="#FF0000")

        self.frameG = ScaleFrame(self, label="G")
        self.frameG.label.config(fg="#009900")

        self.frameB = ScaleFrame(self, label="B")
        self.frameB.label.config(fg="#0000FF")

        self.btnQuit = Button(self, text="Quit", command=self.quit)

        self.canvasMain = Canvas(self, width=333, height=222, bg="#000000")

        self.varGray = tk.BooleanVar()
        self.grayBtn = Checkbutton(self, text="Gray", variable=self.varGray)

        self.frameH = ScaleFrame(self, label="H", to=359)
        self.frameS = ScaleFrame(self, label="S", to=100)
        self.frameV = ScaleFrame(self, label="V", to=100)

        self.frameR.var.trace("w", partial(self.colormake, var=self.frameR.var))
        self.frameG.var.trace("w", partial(self.colormake, var=self.frameG.var))
        self.frameB.var.trace("w", partial(self.colormake, var=self.frameB.var))
        self.frameS.var.trace("w", partial(self.colormake, var=self.frameS.var))
        self.frameH.var.trace("w", partial(self.colormake, var=self.frameH.var))
        self.frameV.var.trace("w", partial(self.colormake, var=self.frameV.var))

        self.lblMain.pack()
        self.frameR.pack()
        self.frameG.pack()
        self.frameB.pack()
        self.grayBtn.pack(anchor="w")
        self.frameH.pack()
        self.frameS.pack()
        self.frameV.pack()
        self.canvasMain.pack()
        self.btnQuit.pack()

    def updateGradientH(self):
        c = self.frameH.canvas
        c.delete("all")
        for i in range(301):
            r, g, b = hsv_to_rgb(
                i / 300, self.frameS.value / 100, self.frameV.value / 100
            )
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            # print(color)
            c.create_line(i, 0, i, 12, fill=color)

    def colormake(self, varname, index, mode, var):
        # print(varname, index, mode)

        traceinfo = self.frameR.var.trace_info()
        self.frameR.var.trace_remove(traceinfo[0][0], traceinfo[0][1])
        traceinfo = self.frameG.var.trace_info()
        self.frameG.var.trace_remove(traceinfo[0][0], traceinfo[0][1])
        traceinfo = self.frameB.var.trace_info()
        self.frameB.var.trace_remove(traceinfo[0][0], traceinfo[0][1])
        traceinfo = self.frameS.var.trace_info()
        self.frameS.var.trace_remove(traceinfo[0][0], traceinfo[0][1])
        traceinfo = self.frameH.var.trace_info()
        self.frameH.var.trace_remove(traceinfo[0][0], traceinfo[0][1])
        traceinfo = self.frameV.var.trace_info()
        self.frameV.var.trace_remove(traceinfo[0][0], traceinfo[0][1])

        if "R" in varname or "G" in varname or "B" in varname:
            r = self.frameR.value
            g = self.frameG.value
            b = self.frameB.value

            if self.varGray.get():
                self.frameR.value = var.get()
                self.frameG.value = var.get()
                self.frameB.value = var.get()

            h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)

            self.frameH.value = int(359 * h)
            self.frameS.value = int(100 * s)
            self.frameV.value = int(100 * v)
        else:
            h = self.frameH.value
            s = self.frameS.value
            v = self.frameV.value

            r, g, b = hsv_to_rgb(h / 359, s / 100, v / 100)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)

            self.frameR.value, self.frameG.value, self.frameB.value = r, g, b

        self.color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        self.canvasMain.config(bg=self.color)
        self.updateGradientH()

        self.frameR.var.trace("w", partial(self.colormake, var=self.frameR.var))
        self.frameG.var.trace("w", partial(self.colormake, var=self.frameG.var))
        self.frameB.var.trace("w", partial(self.colormake, var=self.frameB.var))
        self.frameS.var.trace("w", partial(self.colormake, var=self.frameS.var))
        self.frameH.var.trace("w", partial(self.colormake, var=self.frameH.var))
        self.frameV.var.trace("w", partial(self.colormake, var=self.frameV.var))

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()
