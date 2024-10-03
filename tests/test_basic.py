from __future__ import annotations

import time

import numpy as np

from polyline_ruler import (
    CheapRuler,
    LineSegment,
    PolylineRuler,
    douglas_simplify,
    douglas_simplify_indexes,
    douglas_simplify_mask,
    intersect_segments,
    snap_onto_2d,
    tf,
)


def test_segment():
    seg = LineSegment([0, 0, 0], [10, 0, 0])
    assert seg.distance([5.0, 4.0, 0.0]) == 4.0
    assert seg.distance([-4.0, 3.0, 0.0]) == 5.0
    assert seg.distance([14.0, 3.0, 0.0]) == 5.0

    assert np.all(seg.A == [0, 0, 0])
    assert np.all(seg.B == [10, 0, 0])
    assert np.all(seg.AB == [10, 0, 0])
    assert seg.length == 10.0
    assert seg.length2 == 100.0

    seg = LineSegment([0, 0, 0], [0, 0, 0])
    assert seg.distance([3.0, 4.0, 0.0]) == 5.0
    assert seg.distance([-4.0, 3.0, 0.0]) == 5.0
    assert seg.distance([5.0, 12.0, 0.0]) == 13.0


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


def test_transform_T():
    T_ecef_enu = tf.T_ecef_enu(123, 45, 6.7)
    R_ecef_enu = tf.R_ecef_enu(123, 45)
    assert np.all(T_ecef_enu[:3, :3] == R_ecef_enu)
    assert np.all(T_ecef_enu[:3, 3] == tf.lla2ecef(123, 45, 6.7))
    T_ecef_enu2 = tf.T_ecef_enu([123, 45, 6.7])
    assert np.all(T_ecef_enu == T_ecef_enu2)

    enus = np.random.random((100, 3))
    copy = np.copy(enus)
    ecefs = tf.apply_transform(T_ecef_enu, enus)
    assert np.all(enus == copy)
    tf.apply_transform_inplace(T_ecef_enu, enus)
    assert np.all(enus != copy)
    assert np.all(enus == ecefs)

    # python version
    ecefs2 = (T_ecef_enu[:3, :3] @ copy.T + T_ecef_enu[:3, 3][:, np.newaxis]).T
    assert np.all(ecefs == ecefs2)


def test_intersections():
    pt, t, s = intersect_segments([-1, 0], [1, 0], [0, -1], [0, 1])
    assert np.all(pt == [0, 0])
    assert t == 0.5
    assert s == 0.5
    pt, t, s = intersect_segments([-1, 0], [1, 0], [0, -1], [0, 3])
    assert np.all(pt == [0, 0])
    assert t == 0.5
    assert s == 0.25

    pt, t, s, _ = intersect_segments([-1, 0, 0], [1, 0, 20], [0, -1, -100], [0, 3, 300])
    assert np.all(pt == [0, 0, 5.0])
    assert t == 0.5
    assert s == 0.25

    seg1 = LineSegment([-1, 0, 0], [1, 0, 20])
    seg2 = LineSegment([0, -1, -100], [0, 3, 300])
    pt2, t2, s2, _ = seg1.intersects(seg2)
    assert np.all(pt == pt2) and t == t2 and s == s2

    A = [[-1, 0, 10], [1, 0, 10]]
    B = [[0, -1, 20], [0, 1, 20]]
    pt, t, s, half_span = LineSegment(*A).intersects(LineSegment(*B))
    assert np.all(pt == [0, 0, 15]) and t == 0.5 and s == 0.5 and half_span == 5.0
    pt, t, s, half_span = LineSegment(*B).intersects(LineSegment(*A))
    assert np.all(pt == [0, 0, 15]) and t == 0.5 and s == 0.5 and half_span == -5.0


def test_intersections_parallel():
    # o---o
    #         o----o
    A = [[-2, 0], [-1, 0]]
    B = [[1, 0], [2, 0]]
    ret = intersect_segments(*A, *B)
    assert ret is None
    ret = intersect_segments(*B, *A)
    assert ret is None

    # o----------------------o
    #                     o----------------------o
    A = [[-9, 0], [1, 0]]
    B = [[-1, 0], [9, 0]]
    P, t, s = intersect_segments(*A, *B)
    assert np.all(P == [0, 0])
    assert t == 0.9
    assert s == 0.1
    P, t, s = intersect_segments(*B, *A)
    assert np.all(P == [0, 0])
    assert t == 0.1
    assert s == 0.9
    P, t, s = intersect_segments(*A[::-1], *B)
    assert np.all(P == [0, 0])
    assert t == 0.1
    assert np.abs(s - 0.1) < 1e-15
    P, t, s = intersect_segments(*A, *B[::-1])
    assert np.all(P == [0, 0])
    assert t == 0.9
    assert s == 0.9

    # parallel
    A = [[-9, 1], [1, 1]]
    B = [[-1, 0], [9, 0]]
    for A_, B_ in [[A, B], [A[::-1], B], [A, B[::-1]]]:
        ret = intersect_segments(*A_, *B_)
        assert ret is None
        ret = intersect_segments(*B_, *A_)
        assert ret is None

    # o---o
    #     o----o
    A = [[-2, 0], [0, 0]]
    B = [[0, 0], [2, 0]]
    P, t, s = intersect_segments(*A, *B)
    assert np.all(P == [0, 0])
    assert t == 1.0
    assert s == 0.0
    P, t, s = intersect_segments(*A[::-1], *B)
    assert np.all(P == [0, 0])
    assert t == 0.0
    assert s == 0.0
    P, t, s = intersect_segments(*A, *B[::-1])
    assert np.all(P == [0, 0])
    assert t == 1.0
    assert s == 1.0
    P, t, s = intersect_segments(*A[::-1], *B[::-1])
    assert np.all(P == [0, 0])
    assert t == 0.0
    assert s == 1.0
    P, t, s = intersect_segments(*B, *A)
    assert np.all(P == [0, 0])
    assert t == 0.0
    assert s == 1.0

    # o-----------o
    #    o----o
    A = [[-5, 0], [5, 0]]
    B = [[-1, 0], [3, 0]]
    P, t, s = intersect_segments(*A, *B)
    assert np.all(P == [1, 0])
    assert t == 0.6
    assert s == 0.5
    P, t, s = intersect_segments(*A[::-1], *B)
    assert np.all(P == [1, 0])
    assert t == 0.4
    assert s == 0.5
    P, t, s = intersect_segments(*A[::-1], *B[::-1])
    assert np.all(P == [1, 0])
    assert t == 0.4
    assert s == 0.5
    P, t, s = intersect_segments(*A, *B[::-1])
    assert np.all(P == [1, 0])
    assert t == 0.6
    assert s == 0.5


def test_intersections_duplicates():
    A = [[-5, 0], [5, 0]]
    B = A
    P, t, s = intersect_segments(*A, *B)
    assert np.all(P == [0, 0]) and t == 0.5 and s == 0.5

    # A o
    # B o----o
    A = [[0, 0], [0, 0]]
    B = [[0, 0], [1, 0]]
    P, t, s = intersect_segments(*A, *B)
    assert np.all(P == [0, 0]) and t in (0.0, 0.5) and s == 0.0
    P, t, s = intersect_segments(*B, *A)
    assert np.all(P == [0, 0]) and t == 0.0 and s in (0.0, 0.5)
    P, t, s = intersect_segments(*A, *B[::-1])
    assert np.all(P == [0, 0]) and t in (0.0, 0.5) and s == 1.0

    # A         o
    # B                 o---------o
    A = [[0, 0], [0, 0]]
    B = [[1, 0], [2, 0]]
    ret = intersect_segments(*A, *B)
    assert ret is None

    # A         o
    # B    o---------o
    A = [[0, 0], [0, 0]]
    B = [[-1, 0], [1, 0]]
    P, t, s = intersect_segments(*A, *B)
    assert np.all(P == [0, 0]) and t in (0.0, 0.5) and s == 0.5
    assert ret is None

    # A         o
    # B         o
    A = [[0, 0], [0, 0]]
    B = [[0, 0], [0, 0]]
    P, t, s = intersect_segments(*A, *B)
    assert np.all(P == [0, 0]) and t in (0.5, 0.0) and s in (0.0, 0.5)

    A = [[0, 0], [0, 0]]
    B = [[1, 0], [1, 0]]
    ret = intersect_segments(*A, *B)
    assert ret is None


def test_cheap_ruler_k():
    k = tf.cheap_ruler_k(50.0)
    eps = np.abs(k - [71695.753616003, 111229.06398856241, 1.0]).sum()
    assert eps < 1e-15


def test_polyline_ruler():
    ruler = PolylineRuler([[0, 0, 0], [10, 0, 0], [10, 10, 0], [100, 10, 0]])
    assert np.all(ruler.ranges() == [0, 10, 20, 110])
    assert ruler.length() == 110.0

    for along in [ruler.along, ruler.extended_along]:
        assert np.all(along(0.0) == [0, 0, 0])
        assert np.all(along(10.0) == [10, 0, 0])
        assert np.all(along(18.0) == [10, 8, 0])
        assert np.all(along(21.0) == [11, 10, 0])
        assert np.all(along(100.0) == [90, 10, 0])
        assert np.all(along(110.0) == [100, 10, 0])

    assert np.all(ruler.along(-1.0) == [0, 0, 0])
    assert np.all(ruler.along(111.0) == [100, 10, 0])
    assert np.all(ruler.extended_along(-1.0) == [-1, 0, 0])
    assert np.all(ruler.extended_along(111.0) == [101, 10, 0])

    dirs = ruler.dirs()
    assert dirs.shape == (3, 3)
    assert np.all(dirs == [[1, 0, 0], [0, 1, 0], [1, 0, 0]])

    dir1 = ruler.dir(range=10.0)
    np.testing.assert_allclose(dir1, [np.sqrt(1 / 2), np.sqrt(1 / 2), 0.0], atol=1e-9)
    dir2 = ruler.dir(range=10.0, smooth_joint=False)
    assert np.all(dir2 == [0, 1, 0])  # change to new direction at pt (inclusive)

    xyz, dir = ruler.arrow(10.0, smooth_joint=False)
    assert np.all(xyz == [10, 0, 0])
    assert np.all(dir == dir2)
    xyz, dir = ruler.arrow(-1.0)
    assert np.all(xyz == [-1, 0, 0])
    assert np.all(dir == [1, 0, 0])
    xyz, dir = ruler.arrow(111)
    assert np.all(xyz == [101, 10, 0])
    assert np.all(dir == [1, 0, 0])

    xyz, dir = ruler.arrow(index=0, t=0.2)
    assert np.all(xyz == [2, 0, 0])
    assert np.all(dir == [1, 0, 0])

    ranges, xyzs, dirs = ruler.arrows([-1, 10, 111])
    assert len(ranges) == len(xyzs) == len(dirs)
    ranges, xyzs, dirs = ruler.arrows(10.0)
    assert len(ranges) == 12 and ranges[-1] == 110
    ranges, xyzs, dirs = ruler.arrows(10.0 - 1e-9)
    assert len(ranges) == 13 and ranges[-1] == 110

    ruler = PolylineRuler([[0, 0, 0], [1, 0, 0], [1, 1, 0]])
    assert np.all(ruler.dirs() == [[1, 0, 0], [0, 1, 0]])
    np.testing.assert_allclose(ruler.dir(range=0.0), [1, 0, 0], atol=1e-9)
    np.testing.assert_allclose(ruler.dir(range=0.5), [1, 0, 0], atol=1e-9)
    np.testing.assert_allclose(
        ruler.dir(range=1.0), [np.sqrt(1 / 2), np.sqrt(1 / 2), 0.0], atol=1e-9
    )
    np.testing.assert_allclose(ruler.dir(range=1.5), [0, 1, 0], atol=1e-9)


def test_polyline_ruler_dir():
    ruler = PolylineRuler([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    assert np.all(ruler.dir(point_index=0) == [1, 0, 0])
    assert np.all(ruler.dir(point_index=1) == [0, 1, 0])
    assert np.all(ruler.dir(point_index=2) == [-1, 0, 0])
    assert np.all(ruler.dir(point_index=3) == [-1, 0, 0])


def test_polyline_ruler_duplicates():
    ruler = PolylineRuler([[0, 0, 0], [10, 0, 0], [10, 0, 0], [100, 0, 0]])
    assert np.all(ruler.ranges() == [0, 10, 10, 100])
    assert np.all(ruler.dirs() == [[1, 0, 0], [1, 0, 0], [1, 0, 0]])


def test_polyline_ruler_at():
    ruler = PolylineRuler([[0, 0, 0], [10, 0, 0], [10, 0, 0], [100, 0, 0]])
    assert np.all(ruler.ranges() == [0, 10, 10, 100])
    xyz = ruler.at(range=2.0)
    assert np.all(xyz == [2, 0, 0])
    xyz = ruler.at(segment_index=2)
    assert np.all(xyz == [10, 0, 0])
    xyz = ruler.at(segment_index=2, t=0.5)
    assert np.all(xyz == [55, 0, 0])

    assert ruler.segment_index(-1) == 0
    assert ruler.segment_index(9) == 0
    assert ruler.segment_index(10) == 2
    assert ruler.segment_index(10) == 2
    assert ruler.segment_index(100) == 2
    assert ruler.segment_index(200) == 2

    np.testing.assert_allclose(ruler.segment_index_t(-1), [0, -0.1], atol=1e-9)
    np.testing.assert_allclose(ruler.segment_index_t(9), [0, 0.9], atol=1e-9)
    np.testing.assert_allclose(ruler.segment_index_t(10), [2, 0.0], atol=1e-9)
    np.testing.assert_allclose(ruler.segment_index_t(100), [2, 1.0], atol=1e-9)
    np.testing.assert_allclose(ruler.segment_index_t(190), [2, 2.0], atol=1e-9)


def test_douglas():
    # Nx2
    assert douglas_simplify([[1, 1], [2, 2], [3, 3], [4, 4]], epsilon=1e-9).shape == (
        2,
        2,
    )
    assert douglas_simplify([[0, 0], [5, 1 + 1e-3], [10, 0]], epsilon=1).shape == (3, 2)
    assert douglas_simplify([[0, 0], [5, 1 - 1e-3], [10, 0]], epsilon=1).shape == (2, 2)

    # Nx3
    assert douglas_simplify(
        [[1, 1, 0], [2, 2, 0], [3, 3, 0], [4, 4, 0]], epsilon=1e-9
    ).shape == (
        2,
        3,
    )

    # return mask
    mask = douglas_simplify_mask(
        [[1, 1, 0], [2, 2, 0], [3, 3, 0], [4, 4, 0]], epsilon=1e-9
    )
    assert np.all(mask == [1, 0, 0, 1])
    # return indexes
    indexes = douglas_simplify_indexes(
        [[1, 1, 0], [2, 2, 0], [3, 3, 0], [4, 4, 0]],
        epsilon=1e-9,
    )
    assert np.all(indexes == [0, 3])


def test_cheap_ruler():
    assert CheapRuler.RE
    assert CheapRuler.FE
    assert CheapRuler.E2
    assert CheapRuler.RAD
    print(CheapRuler.Unit.__members__)
    assert CheapRuler.Unit.Meters == CheapRuler.Unit.Metres
    print(CheapRuler.Unit.Kilometers)
    assert str(CheapRuler.Unit.Kilometers) == "Unit.Kilometers"
    assert int(CheapRuler.Unit.Kilometers) == 0
    k1 = CheapRuler._k(20.0)
    k2 = CheapRuler._k(20.0, unit=CheapRuler.Unit.Kilometers)
    assert np.linalg.norm(k1 - k2 * 1000) < 1e-8

    ruler = CheapRuler(45.0)
    np.testing.assert_allclose(ruler.k(), [78846.8350939781, 111131.7774141756, 1.0])

    CheapRuler._fromTile(10, 32)
    ruler.squareDistance([120, 34, 5], [121, 34, 5])
    assert (
        ruler.distance([120, 34, 5], [121, 34, 5])
        == ruler.delta([120, 34, 5], [121, 34, 5])[0]
    )

    assert ruler.bearing([120, 34, 5], [121, 34, 5]) == 90.0
    assert ruler.bearing([122, 34, 5], [121, 34, 5]) == -90.0
    assert ruler.bearing([120, 34, 5], [120, 33, 5]) == 180.0

    ruler.destination([120, 34, 5], 100, 0)
    ruler.destination([120, 34, 5], 100, 90)

    pt = ruler.offset([120, 34, 5], 300, 400)
    assert abs(ruler.distance([120, 34, 5], pt) - 500) < 1e-6
    dist = ruler.lineDistance(
        [
            [120, 34, 5],
            [120, 35, 5],
        ]
    )
    assert dist == ruler.k()[1]


def test_snap_onto():
    P, dist, t = snap_onto_2d([13, 4], [0, 0], [10, 0])
    assert P.tolist() == [10, 0]
    assert dist == 5.0
    assert t == 1.0
