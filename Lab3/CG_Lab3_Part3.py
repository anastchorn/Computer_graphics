import turtle

def apply_rules(rules, input_string, iterations):
    for _ in range(iterations):
        new_string = ""
        for symbol in input_string:
            new_string += rules.get(symbol, symbol)
        input_string = new_string
    return input_string

def draw_fractal(t, draw_string, angle, start_pos=(-200, 50)):
    t.clear()
    t.penup()
    t.goto(start_pos)
    t.pendown()
    for symbol in draw_string:
        if symbol == "F":
            t.forward(10)
        elif symbol == "+":
            t.right(angle)
        elif symbol == "-":
            t.left(angle)
    t.hideturtle()

def start_drawing():
    window = turtle.Screen()
    window.setup(800, 600)
    window.tracer(0)

    t = turtle.Turtle()
    t.speed(0)

    configurations = [
        ({"F": "F+F-F-F+F"}, "F", "lightblue", "Фрактальний хрест 2", 3),
        ({"X": "-YF+XFX+FY-", "Y": "+XF-YFY-FX+"}, "X", "lightgreen", "Фрактальна крива Гільберта", 3),
        ({"X": "XFX--XFX"}, "-X--X", "maroon", "Браслет Кришни", 2),
        ({"X": "X+YF+", "Y": "-FX-Y"}, "FX", "teal","Крива дракона", 7),
        ({"F": "FF+F+F+F+F+F-F"}, "F+F+F+F", "lightgreen", "Фрактальні кільця", 2),
        ({"X": "X+YF++YF-FX--FXFX-YF+", "Y": "-FX+YFYF++YF+FX--FX-Y"}, "XF", "white","Гексагональна крива Госпера", 2),
        ({"F": "FF+F-F+F+FF"}, "F+F+F+F", "lightgreen","Фрактальна плитка", 2),
        ({"F": "F++F++F+++++F-F++F"}, "F++F++F++F++F", "gray", "П’ятикутна фрактальна сніжинка", 2)

    ]

    theta_min, theta_max, theta_step = -180, 180, 1.5

    def draw_configurations(index=0, theta=theta_min):
        if index < len(configurations):
            rules, start_string, bg_color, name, iterations = configurations[index]
            if theta <= theta_max:
                window.bgcolor(bg_color)
                window.title(f"{name} при куті {theta}°")
                final_string = apply_rules(rules, start_string, iterations)
                draw_fractal(t, final_string, theta)
                window.update()
                window.ontimer(lambda: draw_configurations(index, theta + theta_step), 100)
            else:
                window.ontimer(lambda: draw_configurations(index + 1, theta_min), 1000)
        else:
            window.bye()

    draw_configurations()

start_drawing()
turtle.mainloop()

