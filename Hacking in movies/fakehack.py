import secrets
import turtle
import time
screen = turtle.Screen()
screen.setup(width=1000, height=700)
screen.bgcolor("black")
screen.title("Hacking")
t = turtle.Turtle()
t.hideturtle()
t.color("lime")
t.penup()
x = -470
y = 300

t.goto(x, y)

bruh = secrets.token_hex(100000)

for i in range(0, len(bruh), 80):
    line = bruh[i:i + 80]

    t.write(
        line,
        font=("Courier", 10, "normal")
    )

    y -= 15

    if y < -330:
        t.clear()
        y = 300

    t.goto(x, y)

    screen.update()
    time.sleep(0.01)

turtle.done()