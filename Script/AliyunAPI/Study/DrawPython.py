#PythonDraw.py

import turtle
turtle.setup(800,600,0,0)
turtle.penup()
turtle.fd(-250)
turtle.pendown()
turtle.pensize(10)
turtle.pencolor("gray")
turtle.seth(-40)
color = ['red','orange','yellow','blue']
for i in range(4):
    turtle.pencolor(color[i])
    turtle.circle(40,80)
    turtle.circle(-40,80)
turtle.done()