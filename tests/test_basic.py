import time

import numpy as np
from polyline_ruler import LineSegment, intersect_segments, tf


def test_segment():
    seg = LineSegment([0, 0, 0], [10, 0, 0])
    assert 4.0 == seg.distance([5.0, 4.0, 0.0])
    assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
    assert 5.0 == seg.distance([14.0, 3.0, 0.0])
    seg = LineSegment([0, 0, 0], [0, 0, 0])
    assert 5.0 == seg.distance([3.0, 4.0, 0.0])
    assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
    assert 13.0 == seg.distance([5.0, 12.0, 0.0])


def test_transform():
    llas = [[123, 45, 6], [124, 56, 7]]
    enus = tf.lla2enu(llas)
    assert np.linalg.norm(enus[0]) == 0.0
    llas2 = tf.enu2lla(enus, anchor_lla=llas[0])
    assert np.all(llas2 == llas)

    ecefs = tf.lla2ecef(llas)
    ecef1 = tf.lla2ecef(*llas[0])
    ecef2 = tf.lla2ecef(*llas[1])
    assert np.all(ecefs[0] == ecef1)
    assert np.all(ecefs[1] == ecef2)
    llas3 = tf.ecef2lla(ecefs)
    assert np.abs(llas3 - llas).max() < 1e-6
    assert np.abs(llas3 - llas)[:, :2].max() < 1e-11
    assert np.abs(ecefs - tf.lla2ecef(llas3)).max() < 1e-6


class Timer:
    def __init__(self, title: str):
        self.title: str = title

    def __enter__(self):
        self.start: float = time.time()
        return self

    def __exit__(self, *args):
        self.end: float = time.time()

    @property
    def interval(self) -> float:
        return self.end - self.start


def test_transform_cheap_ruler():
    for length in [10, 100, 1000, 1e4, 1e5]:
        enus = np.zeros((1000, 3))
        enus[:, 0] = np.linspace(0, length, len(enus))
        llas = tf.enu2lla(enus, anchor_lla=[123, 45, 6])

        with Timer("enu2lla") as t1:
            enus1 = tf.lla2enu(llas)
        with Timer("enu2lla, cheap ruler") as t2:
            enus2 = tf.lla2enu(llas, cheap_ruler=False)
        print(f"\nlength: {length}")
        print(t1.interval, t2.interval, t2.interval / t1.interval)
        delta = np.abs(enus1 - enus2).max()
        print("delta", delta)


def test_intersections():
    pt, t, s = intersect_segments([-1, 0], [1, 0], [0, -1], [0, 1])
    assert np.all(pt == [0, 0])
    assert t == 0.5
    assert s == 0.5
    pt, t, s = intersect_segments([-1, 0], [1, 0], [0, -1], [0, 3])
    assert np.all(pt == [0, 0])
    assert t == 0.5
    assert s == 0.25

    pt, t, s = intersect_segments([-1, 0, 0], [1, 0, 20], [0, -1, -100], [0, 3, 300])
    assert np.all(pt == [0, 0, 5.0])
    assert t == 0.5
    assert s == 0.25

    seg1 = LineSegment([-1, 0, 0], [1, 0, 20])
    seg2 = LineSegment([0, -1, -100], [0, 3, 300])
    pt2, t2, s2 = seg1.intersects(seg2)
    assert np.all(pt == pt2) and t == t2 and s == s2


from pybind11_rdp import LineSegment as LineSegment2

seg1 = LineSegment([-1, 0, 0], [1, 0, 20])
seg2 = LineSegment2([0, -1, -100], [0, 3, 300])
pt2, t2, s2 = seg1.intersects(seg2)
print()
