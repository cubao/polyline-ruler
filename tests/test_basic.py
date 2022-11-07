from polyline_ruler import LineSegment


def test_segment():
    seg = LineSegment([0, 0, 0], [10, 0, 0])
    assert 4.0 == seg.distance([5.0, 4.0, 0.0])
    assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
    assert 5.0 == seg.distance([14.0, 3.0, 0.0])
    seg = LineSegment([0, 0, 0], [0, 0, 0])
    assert 5.0 == seg.distance([3.0, 4.0, 0.0])
    assert 5.0 == seg.distance([-4.0, 3.0, 0.0])
    assert 13.0 == seg.distance([5.0, 12.0, 0.0])
