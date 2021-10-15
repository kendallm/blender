
from mathutils import Vector, Matrix


def scale_matrix(x: float, y: float, z: float) -> Matrix:
    matx = Matrix.Scale(x, 4, Vector((1, 0, 0)))
    maty = Matrix.Scale(y, 4, Vector((0, 1, 0)))
    matz = Matrix.Scale(z, 4, Vector((0, 0, 1)))
    return matx @ maty @ matz


def polar(angle: float, radius: float, z: float = 0.0) -> Vector:
    x = radius * cos(angle)
    y = radius * sin(angle)
    return Vector((x, y, z))


def hex_to_rgb(h, alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r, g, b)] + [alpha])


def mix(a, b, t):
    return (1 - t) * a + t * b


def clamp(x, low=0, high=1):
    if x <= low:
        return low
    if x >= high:
        return high
    return x


def linearstep(low, high, x):
    x = clamp(x, low, high)
    return (x - low) / (high - low)


def smoothstep(low, high, x):
    t = clamp((x - low) / (high - low))
    return t * t * (3 - 2 * t)


def step(threshold: float, x: float) -> float:
    return 0.0 if x < threshold else 1.0


def cubic_pulse(c: float, w: float, x: float):
    x = abs(x - c)
    if x > w:
        return 0.0
    x /= w
    return 1.0 - x * x * (3.0 - 2.0 * x)


def remap(x, start1, end1, start2, end2, do_clamp=False):
    range1 = end1 - start1
    range2 = end2 - start2
    if range1 == 0:
        range1 = 1
    t = (x - start1) / range1
    return start2 + clamp(t) * range2 if do_clamp else start2 + t * range2