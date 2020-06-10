""""Paint program by Dave Michell.

Subject: tkinter "paint" example
From: Dave Mitchell <davem@magnet.com>
To: python-list@cwi.nl
Date: Fri, 23 Jan 1998 12:18:05 -0500 (EST)

  Not too long ago (last week maybe?) someone posted a request
for an example of a paint program using Tkinter. Try as I might
I can't seem to find it in the archive, so i'll just post mine
here and hope that the person who requested it sees this!

  All this does is put up a canvas and draw a smooth black line
whenever you have the mouse button down, but hopefully it will
be enough to start with.. It would be easy enough to add some
options like other shapes or colors...

                                                yours,
                                                dave mitchell
                                                davem@magnet.com
"""

from tkinter import *
import math

"""paint.py: not exactly a paint program.. just a smooth line drawing demo."""

b1 = "up"
xold, yold = None, None

root = Tk()
drawing_area = Canvas(root)

def main():

    global drawing_area
    drawing_area.pack()
    drawing_area.bind("<Motion>", motion)
    drawing_area.bind("<ButtonPress-1>", b1down)
    drawing_area.bind("<ButtonRelease-1>", b1up)
    drawing_area.config(width=1024, height=1024, bg='white')
    root.mainloop()

def b1down(event):
    global b1
    b1 = "down"           # you only want to draw when the button is down
                          # because "Motion" events happen -all the time-

def b1up(event):
    global b1, xold, yold
    b1 = "up"
    xold = None           # reset the line when you let go of the button
    yold = None

def motion(event):
    if b1 == "down":
        global xold, yold
        global drawing_area
        print(event.x)
        print(xold)

        if xold is not None and yold is not None:
            r = math.sqrt(  (event.x - xold)**2 + (event.y - yold)**2  )
            event.widget.create_line(xold,yold,event.x,event.y,width = 5 * r, smooth=True)
                          # here's where you draw it. smooth. neat.
        xold = event.x
        yold = event.y

        print(event)

        if event.x > 1000 and event.y > 1000:
            drawing_area.delete('all')

if __name__ == "__main__":
    main()