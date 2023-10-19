from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
f = Void()
tk.clean()

try:
    x1, y1 = map(float, input("Enter first point: ").split())
    x2, y2 = map(float, input("Enter second point: ").split())
    f.segment(R2Point(x1, y1), R2Point(x2, y2))
    while True:
        f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        tk.draw_neighborhood_of_the_segment(R2Point(x1, y1), R2Point(x2, y2))
        print(f"S = {f.area()}, P = {f.perimeter()},")
        print(f"Local segments: {f.local_segments()}\n")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
