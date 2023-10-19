from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def local_segments(self):
        return 0

    def segment(self, a, b):
        self.local1 = a
        self.local2 = b
        return self


class Void(Figure):
    """ "Hульугольник" """

    def __init__(self):
        self.local1 = R2Point(0.0, 0.0)
        self.local2 = R2Point(0.0, 0.0)

    def add(self, p):
        return Point(p).segment(self.local1, self.local2)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p
        self.local1 = R2Point(0.0, 0.0)
        self.local2 = R2Point(0.0, 0.0)

    def add(self, q):
        return self if self.p == q else Segment(self.p, q).segment(self.local1, self.local2)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q
        self.local1 = R2Point(0.0, 0.0)
        self.local2 = R2Point(0.0, 0.0)

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.local1, self.local2)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r).segment(self.local1, self.local2)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q).segment(self.local1, self.local2)
        else:
            return self

    def local_segments(self):
        if self.p.is_local(self.local1, self.local2) and self.q.is_local(self.local1, self.local2):
            return 1
        return 0


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, local1=None, local2=None):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        # get sum of is_local for (a, b) and (b, c) and (c, a)
        if local1 is None or local2 is None:
            local1 = R2Point(0.0, 0.0)
            local2 = R2Point(0.0, 0.0)
        self.segment(local1, local2)
        self.locals = Segment(a, b).segment(
            self.local1, self.local2).local_segments()
        self.locals += Segment(b, c).segment(self.local1,
                                             self.local2).local_segments()
        self.locals += Segment(c, a).segment(self.local1,
                                             self.local2).local_segments()

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):
        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека

            self._perimeter -= self.points.first().dist(self.points.last())
            self.delete_local_segment(self.points.first(), self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self.delete_local_segment(p, self.points.first())
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self.delete_local_segment(self.points.last(), p)
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self.add_local_segment(t, self.points.first())
            self.add_local_segment(t, self.points.last())
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)

        return self

    def delete_local_segment(self, a, b):
        self.locals -= Segment(a, b).segment(self.local1,
                                             self.local2).local_segments()

    def add_local_segment(self, a, b):
        self.locals += Segment(a, b).segment(self.local1,
                                             self.local2).local_segments()

    def local_segments(self):
        return self.locals


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
