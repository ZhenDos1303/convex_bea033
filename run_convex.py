from r2point import R2Point
from convex import Void

f = Void()
try:
    x1, y1 = map(float, input("Enter first point: ").split())
    x2, y2 = map(float, input("Enter second point: ").split())
    f.segment(R2Point(x1, y1), R2Point(x2, y2))
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}")
        print(f"Local segments: {f.local_segments()}\n")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
