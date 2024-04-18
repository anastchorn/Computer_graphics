import turtle

def apply_rules(rules, input_string, iterations):
    for _ in range(iterations):
        new_string = ""
        for symbol in input_string:
            new_string += rules.get(symbol, symbol)
        input_string = new_string
    return input_string

def draw_fractal(t, draw_string, angle, name):

    t.penup()
    t.goto(-200,50)
    t.pendown()

    for symbol in draw_string:
        if symbol == "F":
            t.forward(10)
        elif symbol == "+":
            t.right(angle)
        elif symbol == "-":
            t.left(angle)
    t.hideturtle()


def start_drawing(index=0):
    configurations = [
        ({"F": "F+F-F-F+F"}, "F", "lightblue", 100, "Фрактальний хрест 2", 4),
        ({"X": "-YF+XFX+FY-", "Y": "+XF-YFY-FX+"}, "X", "lightgreen", 60, "Фрактальна крива Гільберта", 4),
        ({"X": "XFX--XFX"}, "-X--X", "maroon", 110, "Браслет Кришни", 4),
        ({"X": "X+YF+", "Y": "-FX-Y"}, "FX", "teal", 75, "Крива дракона", 7),
        ({"F": "FF+F+F+F+F+F-F"}, "F+F+F+F", "lightgreen", 60, "Фрактальні кільця", 5),
        ({"X": "X+YF++YF-FX--FXFX-YF+", "Y": "-FX+YFYF++YF+FX--FX-Y"}, "XF", "white", 90, "Гексагональна крива Госпера", 3),
        ({"F": "FF+F-F+F+FF"}, "F+F+F+F", "lightgreen", 60,"Фрактальна плитка", 2),
        ({"F": "F++F++F+++++F-F++F"}, "F++F++F++F++F", "gray", 45,"П’ятикутна фрактальна сніжинка", 2)
    ]

    if index < len(configurations):
        rules, start_string, bg_color, angle, name, iterations = configurations[index]
        turtle.clear()
        window = turtle.Screen()
        window.clear()
        window.bgcolor(bg_color)
        window.title(name)
        final_string = apply_rules(rules, start_string, iterations)
        window.tracer(0)
        t = setup_turtle()
        draw_fractal(t, final_string, angle, name)
        window.update()
        turtle.penup()
        turtle.setpos(-500,300)
        turtle.pendown()

        turtle.ontimer(lambda: start_drawing(index + 1), 2000)

def setup_turtle():
    t = turtle.Turtle()
    t.speed(0)
    return t

turtle.setup(800, 600)
start_drawing()
turtle.mainloop()
