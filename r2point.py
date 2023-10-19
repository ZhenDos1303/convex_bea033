from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    def get_distance_to_segment(self, a, b):
        ak = sqrt((self.x - a.x) * (self.x - a.x) +
                  (self.y - a.y) * (self.y - a.y))
        kb = sqrt((self.x - b.x) * (self.x - b.x) +
                  (self.y - b.y) * (self.y - b.y))
        ab = sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y))

        # скалярное произведение векторов
        mul_scalar_akab = (self.x - a.x) * (b.x - a.x) + \
            (self.y - a.y) * (b.y - a.y)
        mul_scalar_bkab = (self.x - b.x) * (-b.x + a.x) + \
            (self.y - b.y) * (-b.y + a.y)

        if ab == 0:
            return ak
        elif mul_scalar_akab >= 0 and mul_scalar_bkab >= 0:
            p = (ak + kb + ab) / 2.0
            s = sqrt(abs((p * (p - ak) * (p - kb) * (p - ab))))
            return (2.0 * s) / ab
        elif mul_scalar_akab < 0 or mul_scalar_bkab < 0:
            return min(ak, kb)
        else:
            return 0

    def is_local(self, a, b):
        return self.get_distance_to_segment(a, b) <= 1


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
