import turtle

# Setup window
win = turtle.Screen()
win.title("Turtle Movement with WASD and Arrow Keys")
win.bgcolor("white")

# Create turtle
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.speed(0)

# Movement functions
def move_up():
    player.setheading(90)
    player.forward(10)

def move_down():
    player.setheading(270)
    player.forward(10)

def move_left():
    player.setheading(180)
    player.forward(10)

def move_right():
    player.setheading(0)
    player.forward(10)

# Keyboard bindings
win.listen()
win.onkeypress(move_up, "w")
win.onkeypress(move_down, "s")
win.onkeypress(move_left, "a")
win.onkeypress(move_right, "d")

win.onkeypress(move_up, "Up")
win.onkeypress(move_down, "Down")
win.onkeypress(move_left, "Left")
win.onkeypress(move_right, "Right")

# Keep the window open
win.mainloop()

