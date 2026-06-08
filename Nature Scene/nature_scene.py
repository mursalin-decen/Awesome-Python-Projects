import turtle

screen = turtle.Screen()
screen.bgcolor("skyblue")

pen = turtle.Turtle()
pen.speed(0)

# Sun
pen.penup()
pen.goto(250, 180)
pen.pendown()
pen.color("yellow")
pen.begin_fill()
pen.circle(50)
pen.end_fill()

# Ground
pen.penup()
pen.goto(-400, -100)
pen.pendown()
pen.color("green")
pen.begin_fill()
for _ in range(2):
    pen.forward(800)
    pen.right(90)
    pen.forward(200)
    pen.right(90)
pen.end_fill()

# House body
pen.penup()
pen.goto(-100, -100)
pen.pendown()
pen.color("brown")
pen.begin_fill()
for _ in range(4):
    pen.forward(200)
    pen.left(90)
pen.end_fill()

# Roof
pen.penup()
pen.goto(-120, 100)
pen.pendown()
pen.color("red")
pen.begin_fill()
pen.goto(0, 220)
pen.goto(120, 100)
pen.goto(-120, 100)
pen.end_fill()

# Door
pen.penup()
pen.goto(-30, -100)
pen.pendown()
pen.color("darkred")
pen.begin_fill()
for _ in range(2):
    pen.forward(60)
    pen.left(90)
    pen.forward(100)
    pen.left(90)
pen.end_fill()

# Window 1
pen.penup()
pen.goto(-80, 0)
pen.pendown()
pen.color("lightblue")
pen.begin_fill()
for _ in range(4):
    pen.forward(40)
    pen.left(90)
pen.end_fill()

# Window 2
pen.penup()
pen.goto(40, 0)
pen.pendown()
pen.begin_fill()
for _ in range(4):
    pen.forward(40)
    pen.left(90)
pen.end_fill()

# Tree trunk
pen.penup()
pen.goto(-250, -100)
pen.pendown()
pen.color("saddlebrown")
pen.begin_fill()
for _ in range(2):
    pen.forward(40)
    pen.left(90)
    pen.forward(120)
    pen.left(90)
pen.end_fill()

# Tree leaves
pen.penup()
pen.goto(-270, 20)
pen.pendown()
pen.color("darkgreen")
pen.begin_fill()
pen.circle(60)
pen.end_fill()

pen.hideturtle()

turtle.done()