# from os.path import basename, splitext
import tkinter as tk
from tkinter import Label, Button, Scale, Entry, Frame, Canvas, Checkbutton
from colorsys import rgb_to_hsv, hsv_to_rgb
from functools import partial
from tkinter import ttk
from pathlib import Path
from os import listdir


class ScaleFrame(Frame):
    def __init__(self, master=None, cnf={}, label="", from_=0, to=0xFF, **kw):
        self.step = 10
        self.from_ = from_
        self.to = to

        super().__init__(master, borderwidth=2, relief="raised")

        self.var = tk.IntVar(self, 0, "var{}".format(label))

        self.label = Label(self, text=label)

        self.scale = Scale(
            self,
            from_=self.from_,
            to=self.to,
            showvalue=0,
            orient="horizontal",
            width=12,
            length=330,
            variable=self.var,
        )

        self.entry = Entry(self, width=5, textvariable=self.var)

        self.canvas = Canvas(self, width=300, height=20)

        self.scale.bind("<Button-4>", self.up)
        self.entry.bind("<Button-4>", self.up)
        self.scale.bind("<Button-5>", self.down)
        self.entry.bind("<Button-5>", self.down)
        self.canvas.bind("<Button-1>", self.canvasClickHandler)
        self.canvas.bind("<Button-4>", self.canvasUpHandler)
        self.canvas.bind("<Button-5>", self.canvasDownHandler)

        self.label.grid(row="1", column=0, sticky="s")
        self.canvas.grid(row="1", column=1, sticky="n")
        self.entry.grid(row="1", column=2, sticky="s")
        self.scale.grid(row="0", column=1, sticky="s")

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

    def canvasClickHandler(self, e: tk.Event):
        w = e.widget.winfo_width()
        x = e.x
        self.value = int(x / w * self.to)

    def canvasUpHandler(self, e: tk.Event = None):
        if self.value + self.step > self.to:
            self.value = self.to
        else:
            self.value += self.step

    def canvasDownHandler(self, e: tk.Event = None):
        if self.value - self.step < self.from_:
            self.value = 0
        else:
            self.value -= self.step


class Application(tk.Tk):
    name = "ColorMishMash"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        c = Path("~/.config").expanduser()
        if not c.exists():
            c.mkdir()
        self.confdir = Path("~/.config/colormishmash").expanduser()
        if not self.confdir.exists():
            self.confdir.mkdir()
        self.savelist = sorted(listdir(self.confdir))

        self.bind("<Escape>", self.clickEscape)
        self.resizable(False, False)

        self.lblMain = Label(self, text="ColorMishMash", font="16")

        self.frameSave = Frame(self)
        self.varSave = tk.StringVar(self, "", "varSave")
        # self.varSave.trace("w", self.load)
        self.comboSave = ttk.Combobox(
            self.frameSave, values=self.savelist, textvariable=self.varSave
        )
        self.comboSave.bind("<<ComboboxSelected>>", self.load)
        self.btnSave = Button(self.frameSave, text="Save", command=self.save)
        self.btnQuit = Button(self.frameSave, text="Quit", command=self.quit)

        self.frameR = ScaleFrame(self, label="R")
        self.frameR.label.config(fg="#FF0000")

        self.frameG = ScaleFrame(self, label="G")
        self.frameG.label.config(fg="#009900")

        self.frameB = ScaleFrame(self, label="B")
        self.frameB.label.config(fg="#0000FF")

        self.frameCanvas = Frame(self, width=400, height=240)
        self.width2 = self.frameCanvas.cget("width") // 2
        self.height2 = self.frameCanvas.cget("height") // 2

        self.canvas2 = Canvas(
            self.frameCanvas,
            width=self.width2,
            height=self.height2,
            bg="#F0F000",
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas3 = Canvas(
            self.frameCanvas,
            width=self.width2,
            height=self.height2,
            bg="#F000F0",
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas4 = Canvas(
            self.frameCanvas,
            width=self.width2,
            height=self.height2,
            bg="#0000F0",
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas5 = Canvas(
            self.frameCanvas,
            width=self.width2 * 4 // 3,
            height=self.height2 * 4 // 3,
            bg="#000000",
            borderwidth=-2,
            highlightthickness=0,
        )

        self.canvas1 = Canvas(
            self.frameCanvas,
            width=self.width2,
            height=self.height2,
            bg="#F00000",
            borderwidth=0,
            highlightthickness=0,
        )

        self.frameMem = Frame(self)
        self.canvasMem = []
        for row in range(3):
            for column in range(8):
                canvas = Canvas(self.frameMem, width=48, height=48, bg="#ef12ab")
                canvas.grid(row=row, column=column)
                self.canvasMem.append(canvas)
                canvas.bind("<Button-1>", self.clickHandler)
        self.canvas1.bind("<Button-1>", self.clickHandler)
        self.canvas2.bind("<Button-1>", self.clickHandler)
        self.canvas3.bind("<Button-1>", self.clickHandler)
        self.canvas4.bind("<Button-1>", self.clickHandler)
        self.canvas5.bind("<Button-1>", self.clickHandler)

        self.canvasMain = self.canvas5
        self.marker = self.canvasMain.create_oval(
            120, 80, 130, 90, width=3, outline="black", fill="white"
        )
        self.canvas1.bind("<Button-3>", partial(self.setMainCanvas))
        self.canvas2.bind("<Button-3>", partial(self.setMainCanvas))
        self.canvas3.bind("<Button-3>", partial(self.setMainCanvas))
        self.canvas4.bind("<Button-3>", partial(self.setMainCanvas))
        self.canvas5.bind("<Button-3>", partial(self.setMainCanvas))

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

        self.frameSave.pack(fill="x")
        self.comboSave.pack(side="left", padx=3)
        self.btnSave.pack(side="left")
        self.btnQuit.pack(side="right", padx=3)

        self.frameR.pack(ipady=4)
        self.frameG.pack(ipady=4)
        self.frameB.pack(ipady=4)
        self.grayBtn.pack(anchor="w")
        self.frameH.pack(ipady=4)
        self.frameS.pack(ipady=4)
        self.frameV.pack(ipady=4)

        self.frameCanvas.pack()
        self.canvas1.place(x=0, y=0)
        self.canvas2.place(x=self.width2, y=0)
        self.canvas3.place(x=0, y=self.height2)
        self.canvas4.place(x=self.width2, y=self.height2)
        self.canvas5.place(x=self.width2 // 2, y=self.height2 // 2)

        self.text1 = self.canvas1.create_text(
            123, 96, text="Blábol ipsum", font=("Verdana", 14, "bold")
        )
        self.text2 = self.canvas5.create_text(
            179, 131, text="Lorem blábol", font=("Verdana", 14, "bold")
        )

        self.frameMem.pack()

        # Load
        if len(self.savelist):
            self.comboSave.current(0)
            self.load()

    def clickHandler(self, event):
        if self.cget("cursor") != "pencil":  # kliknu poprve
            self.config(cursor="pencil")
            self.touchcolor = event.widget.cget("bg")
        else:  # kliknu podruhe
            self.config(cursor="")
            if event.widget is self.canvasMain:
                self.frameR.value = int(self.touchcolor[1:3], 16)
                self.frameG.value = int(self.touchcolor[3:5], 16)
                self.frameB.value = int(self.touchcolor[5:], 16)
            else:
                event.widget.config(bg=self.touchcolor)
            if event.widget is self.canvas5:
                self.canvas1.itemconfig(self.text1, fill=self.touchcolor)
            if event.widget is self.canvas4:
                self.canvas5.itemconfig(self.text2, fill=self.touchcolor)

    def clickEscape(self, event: tk.Event):
        self.config(cursor="")

    def setMainCanvas(self, event: tk.Event):
        self.canvasMain.delete(self.marker)
        css = event.widget.cget("bg")
        r = int(css[1:3], 16)
        g = int(css[3:5], 16)
        b = int(css[5:], 16)
        self.canvasMain = event.widget
        self.frameR.value = r
        self.frameG.value = g
        self.frameB.value = b
        if self.canvasMain is self.canvas1:
            self.marker = self.canvasMain.create_oval(
                10, 10, 20, 20, width=3, outline="black", fill="white"
            )
        elif self.canvasMain is self.canvas2:
            self.marker = self.canvasMain.create_oval(
                180, 10, 190, 20, width=3, outline="black", fill="white"
            )
        elif self.canvasMain is self.canvas3:
            self.marker = self.canvasMain.create_oval(
                10, 100, 20, 110, width=3, outline="black", fill="white"
            )
        elif self.canvasMain is self.canvas4:
            self.marker = self.canvasMain.create_oval(
                180, 100, 190, 110, width=3, outline="black", fill="white"
            )
        elif self.canvasMain is self.canvas5:
            self.marker = self.canvasMain.create_oval(
                # 220, 10, 230, 20, width=3, outline="black", fill="white"
                120,
                80,
                130,
                90,
                width=3,
                outline="black",
                fill="white",
            )

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
            c.create_line(i, 0, i, 20, fill=color)

    def updateGradientS(self):
        c = self.frameS.canvas
        c.delete("all")
        for i in range(101):
            r, g, b = hsv_to_rgb(
                self.frameH.value / 359, i / 100, self.frameV.value / 100
            )
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            # c.create_line(i, 0, i, 20, fill=color)
            c.create_rectangle(i * 3, 0, 3 * (i + 1), 20, fill=color, width=0)

    def updateGradientV(self):
        c = self.frameV.canvas
        c.delete("all")
        for i in range(101):
            r, g, b = hsv_to_rgb(
                self.frameH.value / 359, self.frameS.value / 100, i / 100
            )
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            # c.create_line(i, 0, i, 20, fill=color)
            c.create_rectangle(i * 3, 0, 3 * (i + 1), 20, fill=color, width=0)

    def updateGradientR(self):
        c = self.frameR.canvas
        c.delete("all")
        for i in range(301):
            color = "#{:02X}{:02X}{:02X}".format(
                int(i * 255 / 300), self.frameG.value, self.frameB.value
            )
            c.create_line(i, 0, i, 20, fill=color)

    def updateGradientG(self):
        c = self.frameG.canvas
        c.delete("all")
        for i in range(301):
            color = "#{:02X}{:02X}{:02X}".format(
                self.frameR.value, int(i * 255 / 300), self.frameB.value
            )
            c.create_line(i, 0, i, 20, fill=color)

    def updateGradientB(self):
        c = self.frameB.canvas
        c.delete("all")
        for i in range(301):
            color = "#{:02X}{:02X}{:02X}".format(
                self.frameR.value, self.frameG.value, int(i * 255 / 300)
            )
            c.create_line(i, 0, i, 20, fill=color)

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
        if self.canvasMain is self.canvas5:
            self.canvas1.itemconfig(self.text1, fill=self.color)
        if self.canvasMain is self.canvas4:
            self.canvas5.itemconfig(self.text2, fill=self.color)

        if var is not self.frameH.var:
            self.updateGradientH()
        if var is not self.frameS.var:
            self.updateGradientS()
        if var is not self.frameV.var:
            self.updateGradientV()
        if var is not self.frameR.var:
            self.updateGradientR()
        if var is not self.frameG.var:
            self.updateGradientG()
        if var is not self.frameB.var:
            self.updateGradientB()

        self.frameR.var.trace("w", partial(self.colormake, var=self.frameR.var))
        self.frameG.var.trace("w", partial(self.colormake, var=self.frameG.var))
        self.frameB.var.trace("w", partial(self.colormake, var=self.frameB.var))
        self.frameS.var.trace("w", partial(self.colormake, var=self.frameS.var))
        self.frameH.var.trace("w", partial(self.colormake, var=self.frameH.var))
        self.frameV.var.trace("w", partial(self.colormake, var=self.frameV.var))

    def CSStoRGB(self, source):
        if isinstance(source, tk.Canvas):
            css = source.cget("bg")
            self.frameR.value = int(css[1:3], 16)
            self.frameG.value = int(css[3:5], 16)
            self.frameG.value = int(css[5:], 16)

    def save(self):
        filename = self.varSave.get()
        checkname = ""
        for c in filename:
            if c.upper() in "-_1234567890QWERTYUIOPASDFGHJKLZXCVBNM":
                checkname += c
        p = Path(f"~/.config/colormishmash/{checkname}").expanduser()
        with p.open("w") as f:
            f.write(self.canvas1.cget("bg") + "\n")
            f.write(self.canvas2.cget("bg") + "\n")
            f.write(self.canvas3.cget("bg") + "\n")
            f.write(self.canvas4.cget("bg") + "\n")
            f.write(self.canvas5.cget("bg") + "\n")
            for canvas in self.canvasMem:
                f.write(canvas.cget("bg") + "\n")
        choice = self.varSave.get()
        self.savelist = sorted(listdir(self.confdir))
        self.comboSave.config(values=self.savelist)
        self.varSave.set(choice)

    # def load(self, varname, index, mode):
    def load(self, event: tk.Event = None):
        filename = self.varSave.get()
        conffile = Path(f"~/.config/colormishmash/{filename}").expanduser()
        if conffile.is_file():
            with conffile.open("r") as f:
                self.canvas1.config(bg=f.readline().strip())
                self.canvas2.config(bg=f.readline().strip())
                self.canvas3.config(bg=f.readline().strip())
                self.canvas4.config(bg=f.readline().strip())
                self.canvas5.config(bg=f.readline().strip())
                for canvas in self.canvasMem:
                    canvas.config(bg=f.readline().strip())
            self.CSStoRGB(self.canvasMain)
            self.canvas1.itemconfig(self.text1, fill=self.canvas5.cget("bg"))
            self.canvas5.itemconfig(self.text2, fill=self.canvas4.cget("bg"))

    def quit(self, event=None):
        super().quit()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
