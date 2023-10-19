from tkinter import *
from r2point import R2Point
import math

# Размер окна
SIZE = 600
# Коэффициент гомотетии
SCALE = 50


def x(p):
    """ преобразование x-координаты """
    return SIZE / 2 + SCALE * p.x


def y(p):
    """ преобразование y-координаты """
    return SIZE / 2 - SCALE * p.y


class TkDrawer:
    """ Графический интерфейс для выпуклой оболочки """

    # Конструктор
    def __init__(self):
        self.root = Tk()
        self.root.title("Выпуклая оболочка")
        self.root.geometry(f"{SIZE+5}x{SIZE+5}")
        self.root.resizable(False, False)
        self.root.bind('<Control-c>', quit)
        self.canvas = Canvas(self.root, width=SIZE, height=SIZE)
        self.canvas.pack(padx=5, pady=5)

    # Завершение работы
    def close(self):
        self.root.quit()

    # Стирание существующей картинки и рисование осей координат
    def clean(self):
        self.canvas.create_rectangle(0, 0, SIZE, SIZE, fill="white")
        self.canvas.create_line(0, SIZE / 2, SIZE, SIZE / 2, fill="blue")
        self.canvas.create_line(SIZE / 2, 0, SIZE / 2, SIZE, fill="blue")
        self.root.update()

    # Рисование точки
    def draw_point(self, p):
        self.canvas.create_oval(
            x(p) + 1, y(p) + 1, x(p) - 1, y(p) - 1, fill="black")
        self.root.update()

    # Рисование линии
    def draw_line(self, p, q):
        self.canvas.create_line(x(p), y(p), x(q), y(q), fill="black", width=2)
        self.root.update()

    def draw_neighborhood_of_the_segment(self, point1, point2):
        # Calculate the angle of the segment
        angle = math.atan2(point2.y - point1.y, point2.x - point1.x)
        # Make new points with shift
        point1_bottom = R2Point(
            point1.x + math.sin(angle), point1.y - math.cos(angle))
        point1_top = R2Point(point1.x - math.sin(angle),
                             point1.y + math.cos(angle))
        point2_bottom = R2Point(
            point2.x + math.sin(angle), point2.y - math.cos(angle))
        point2_top = R2Point(point2.x - math.sin(angle),
                             point2.y + math.cos(angle))
        # Draw the top and bottom lines with corresponding shift
        self.canvas.create_line(x(point1_bottom), y(point1_bottom), x(
            point2_bottom), y(point2_bottom), fill="red", width=2)
        self.canvas.create_line(x(point1_top), y(point1_top), x(
            point2_top), y(point2_top), fill="red", width=2)
        # Calculate start and end angles for arc
        start_angle = (angle + math.pi / 2) / math.pi * 180
        if start_angle < 0:
            start_angle += 360
        end_angle = (angle - math.pi / 2) / math.pi * 180
        if end_angle < 0:
            end_angle += 360

        point1_start = R2Point(point1.x + 1, point1.y + 1)
        point1_end = R2Point(point1.x - 1, point1.y - 1)
        self.canvas.create_arc(x(point1_start), y(point1_start), x(point1_end), y(point1_end),
                               start=start_angle, extent=180, style='arc', outline='red', width=2)
        point2_start = R2Point(point2.x + 1, point2.y + 1)
        point2_end = R2Point(point2.x - 1, point2.y - 1)
        self.canvas.create_arc(x(point2_start), y(point2_start), x(point2_end), y(point2_end),
                               start=end_angle, extent=180, style='arc', outline='red', width=2)


if __name__ == "__main__":
    import time
    from r2point import R2Point
    tk = TkDrawer()
    tk.clean()
    tk.draw_point(R2Point(2.0, 2.0))
    tk.draw_line(R2Point(0.0, 0.0), R2Point(1.0, 1.0))
    tk.draw_line(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
    time.sleep(5)
