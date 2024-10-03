"""

cubao/polyline-ruler is more than mapbox/cheap-ruler
----------------------------------------------------

.. currentmodule:: polyline_ruler

.. autosummary::
   :toctree: _generate

   TODO

"""

from __future__ import annotations
import numpy
import typing
from . import tf

__all__ = [
    "CheapRuler",
    "LineSegment",
    "PolylineRuler",
    "douglas_simplify",
    "douglas_simplify_indexes",
    "douglas_simplify_mask",
    "intersect_segments",
    "snap_onto_2d",
    "tf",
]

class CheapRuler:
    """

    A class for fast distance calculations and geometric operations.

    CheapRuler provides methods for various geometric calculations
    optimized for speed and simplicity, sacrificing some accuracy
    for performance.

    """
    class Unit:
        """

                Enumeration of supported distance units.


        Members:

          Kilometers : Kilometers

          Miles : Miles

          NauticalMiles : Nautical Miles

          Meters : Meters

          Metres : Metres (alias for Meters)

          Yards : Yards

          Feet : Feet

          Inches : Inches
        """

        Feet: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Feet: 5>
        Inches: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Inches: 6>
        Kilometers: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Kilometers: 0>
        Meters: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Meters: 3>
        Metres: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Meters: 3>
        Miles: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Miles: 1>
        NauticalMiles: typing.ClassVar[
            CheapRuler.Unit
        ]  # value = <Unit.NauticalMiles: 2>
        Yards: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Yards: 4>
        __members__: typing.ClassVar[
            dict[str, CheapRuler.Unit]
        ]  # value = {'Kilometers': <Unit.Kilometers: 0>, 'Miles': <Unit.Miles: 1>, 'NauticalMiles': <Unit.NauticalMiles: 2>, 'Meters': <Unit.Meters: 3>, 'Metres': <Unit.Meters: 3>, 'Yards': <Unit.Yards: 4>, 'Feet': <Unit.Feet: 5>, 'Inches': <Unit.Inches: 6>}
        def __eq__(self, other: typing.Any) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: typing.Any) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        def __str__(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def value(self) -> int: ...

    E2: typing.ClassVar[float] = 0.0066943799901413165
    FE: typing.ClassVar[float] = 0.0033528106647474805
    Feet: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Feet: 5>
    Inches: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Inches: 6>
    Kilometers: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Kilometers: 0>
    Meters: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Meters: 3>
    Metres: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Meters: 3>
    Miles: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Miles: 1>
    NauticalMiles: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.NauticalMiles: 2>
    RAD: typing.ClassVar[float] = 0.017453292519943295
    RE: typing.ClassVar[float] = 6378.137
    Yards: typing.ClassVar[CheapRuler.Unit]  # value = <Unit.Yards: 4>
    @staticmethod
    def _fromTile(x: int, y: int) -> CheapRuler:
        """
        Create a CheapRuler from tile coordinates (x, y).
        """
    @staticmethod
    def _insideBBox(
        p: numpy.ndarray[numpy.float64[3, 1]],
        bbox: tuple[
            numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
        ],
        *,
        cheak_z: bool = False,
    ) -> bool:
        """
        Check if a point is inside a bounding box.
        """
    @staticmethod
    def _interpolate(
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
        t: float,
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Interpolate linearly between two points.
        """
    @staticmethod
    def _k(
        latitude: float, *, unit: CheapRuler.Unit = ...
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the unit conversion factor for a given latitude and unit.
        """
    @staticmethod
    def _longDiff(a: float, b: float) -> float:
        """
        Calculate the difference between two longitudes.
        """
    def __init__(self, latitude: float, *, unit: CheapRuler.Unit = ...) -> None:
        """
        Initialize a CheapRuler object with a given latitude and unit.
        """
    def along(
        self,
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        dist: float,
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Calculate a point at a specified distance along the line.
        """
    def area(
        self, ring: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous]
    ) -> float:
        """
        Calculate the area of a polygon.
        """
    def bearing(
        self,
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float:
        """
        Calculate the bearing between two points.
        """
    def bufferBBox(
        self,
        bbox: tuple[
            numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
        ],
        buffer: float,
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]]:
        """
        Create a bounding box around another bounding box.
        """
    def bufferPoint(
        self, p: numpy.ndarray[numpy.float64[3, 1]], buffer: float
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]]:
        """
        Create a bounding box around a point.
        """
    def delta(
        self,
        lla0: numpy.ndarray[numpy.float64[3, 1]],
        lla1: numpy.ndarray[numpy.float64[3, 1]],
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Calculate the distance between two points in the x, y plane.
        """
    def destination(
        self, origin: numpy.ndarray[numpy.float64[3, 1]], dist: float, bearing: float
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Calculate the destination point given origin, distance, and bearing.
        """
    def distance(
        self,
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float:
        """
        Calculate the distance between two points.
        """
    def k(self) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the ruler's unit conversion factor.
        """
    def lineDistance(
        self,
        points: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
    ) -> float:
        """
        Calculate the total distance of a line (an array of points).
        """
    def lineSlice(
        self,
        start: numpy.ndarray[numpy.float64[3, 1]],
        stop: numpy.ndarray[numpy.float64[3, 1]],
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
    ) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Get a part of the line between the start and stop points.
        """
    def lineSliceAlong(
        self,
        start: float,
        stop: float,
        line: numpy.ndarray[
            numpy.float64[m, 3],
            numpy.ndarray.flags.writeable,
            numpy.ndarray.flags.c_contiguous,
        ],
    ) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Get a part of the line between the start and stop distances along the line.
        """
    def offset(
        self,
        origin: numpy.ndarray[numpy.float64[3, 1]],
        dx: float,
        dy: float,
        dz: float = 0.0,
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Calculate a new point given origin and offsets.
        """
    def pointOnLine(
        self,
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        p: numpy.ndarray[numpy.float64[3, 1]],
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], int, float]:
        """
        Calculate the closest point on a line to the given point.
        """
    def pointToSegmentDistance(
        self,
        p: numpy.ndarray[numpy.float64[3, 1]],
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float:
        """
        Calculate the distance from a point to a line segment.
        """
    def squareDistance(
        self,
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float:
        """
        Calculate the squared distance between two points.
        """

class LineSegment:
    def __init__(
        self,
        A: numpy.ndarray[numpy.float64[3, 1]],
        B: numpy.ndarray[numpy.float64[3, 1]],
    ) -> None:
        """
        Initialize a LineSegment with two 3D points.
        """
    def distance(self, P: numpy.ndarray[numpy.float64[3, 1]]) -> float:
        """
        Calculate the distance from a point to the line segment.
        """
    def distance2(self, P: numpy.ndarray[numpy.float64[3, 1]]) -> float:
        """
        Calculate the squared distance from a point to the line segment.
        """
    def intersects(
        self, other: LineSegment
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], float, float, float] | None:
        """
        Check if this line segment intersects with another.
        """
    @property
    def A(self) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the start point of the line segment.
        """
    @property
    def AB(self) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the vector from A to B.
        """
    @property
    def B(self) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the end point of the line segment.
        """
    @property
    def length(self) -> float:
        """
        Get the length of the line segment.
        """
    @property
    def length2(self) -> float:
        """
        Get the squared length of the line segment.
        """

class PolylineRuler:
    @staticmethod
    def _along(
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        dist: float,
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Find a point at a specified distance along a polyline.
        """
    @staticmethod
    def _dirs(
        polyline: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Calculate direction vectors for each segment of a polyline.
        """
    @staticmethod
    def _distance(
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> float:
        """
        Calculate the distance between two points.
        """
    @staticmethod
    def _interpolate(
        A: numpy.ndarray[numpy.float64[3, 1]],
        B: numpy.ndarray[numpy.float64[3, 1]],
        *,
        t: float,
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Interpolate between two points.
        """
    @staticmethod
    def _lineDistance(
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> float:
        """
        Calculate the total length of a polyline.
        """
    @staticmethod
    def _lineSlice(
        start: numpy.ndarray[numpy.float64[3, 1]],
        stop: numpy.ndarray[numpy.float64[3, 1]],
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Extract a portion of a polyline between two points.
        """
    @staticmethod
    def _lineSliceAlong(
        start: float,
        stop: float,
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Extract a portion of a polyline between two distances along it.
        """
    @staticmethod
    def _pointOnLine(
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        P: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], int, float]:
        """
        Find the closest point on a polyline to a given point.
        """
    @staticmethod
    def _pointToSegmentDistance(
        P: numpy.ndarray[numpy.float64[3, 1]],
        A: numpy.ndarray[numpy.float64[3, 1]],
        B: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> float:
        """
        Calculate the distance from a point to a line segment.
        """
    @staticmethod
    def _ranges(
        polyline: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 1]]:
        """
        Calculate cumulative distances along a polyline.
        """
    @staticmethod
    def _squareDistance(
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> float:
        """
        Calculate the squared distance between two points.
        """
    def N(self) -> int:
        """
        Get the number of points in the polyline.
        """
    def __init__(
        self,
        coords: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> None:
        """
        Initialize a PolylineRuler with coordinates and coordinate system.
        """
    def along(self, dist: float) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Find a point at a specified distance along the polyline.
        """
    @typing.overload
    def arrow(
        self, *, index: int, t: float
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]]:
        """
        Get the arrow (point and direction) at a specific segment index and interpolation factor.
        """
    @typing.overload
    def arrow(
        self, range: float, *, smooth_joint: bool = True
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]]:
        """
        Get the arrow (point and direction) at a specific cumulative distance.
        """
    @typing.overload
    def arrows(
        self, ranges: numpy.ndarray[numpy.float64[m, 1]], *, smooth_joint: bool = True
    ) -> tuple[
        numpy.ndarray[numpy.float64[m, 1]],
        numpy.ndarray[numpy.float64[m, 3]],
        numpy.ndarray[numpy.float64[m, 3]],
    ]:
        """
        Get arrows (points and directions) at multiple cumulative distances.
        """
    @typing.overload
    def arrows(
        self, step: float, *, with_last: bool = True, smooth_joint: bool = True
    ) -> tuple[
        numpy.ndarray[numpy.float64[m, 1]],
        numpy.ndarray[numpy.float64[m, 3]],
        numpy.ndarray[numpy.float64[m, 3]],
    ]:
        """
        Get arrows (points and directions) at regular intervals along the polyline.
        """
    @typing.overload
    def at(self, *, range: float) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the point on the polyline at a specific cumulative distance.
        """
    @typing.overload
    def at(self, *, segment_index: int) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the point on the polyline at a specific segment index.
        """
    @typing.overload
    def at(self, *, segment_index: int, t: float) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the point on the polyline at a specific segment index and interpolation factor.
        """
    @typing.overload
    def dir(self, *, point_index: int) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the direction vector at a specific point index.
        """
    @typing.overload
    def dir(
        self, *, range: float, smooth_joint: bool = True
    ) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the direction vector at a specific cumulative distance.
        """
    def dirs(self) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Get direction vectors for each segment of the polyline.
        """
    def extended_along(self, range: float) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the extended cumulative distance along the polyline.
        """
    def is_wgs84(self) -> bool:
        """
        Check if the coordinate system is WGS84.
        """
    def k(self) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
        Get the scale factor for distance calculations.
        """
    def length(self) -> float:
        """
        Get the total length of the polyline.
        """
    def lineDistance(self) -> float:
        """
        Get the total length of the polyline.
        """
    def lineSlice(
        self,
        start: numpy.ndarray[numpy.float64[3, 1]],
        stop: numpy.ndarray[numpy.float64[3, 1]],
    ) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Extract a portion of the polyline between two points.
        """
    def lineSliceAlong(
        self, start: float, stop: float
    ) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Extract a portion of the polyline between two distances along it.
        """
    def local_frame(
        self, range: float, *, smooth_joint: bool = True
    ) -> numpy.ndarray[numpy.float64[4, 4]]:
        """
        Get the local coordinate frame at a specific cumulative distance.
        """
    def pointOnLine(
        self, P: numpy.ndarray[numpy.float64[3, 1]]
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], int, float]:
        """
        Find the closest point on the polyline to a given point.
        """
    def polyline(self) -> numpy.ndarray[numpy.float64[m, 3]]:
        """
        Get the polyline coordinates.
        """
    @typing.overload
    def range(self, segment_index: int) -> float:
        """
        Get the cumulative distance at a specific segment index.
        """
    @typing.overload
    def range(self, *, segment_index: int, t: float) -> float:
        """
        Get the cumulative distance at a specific segment index and interpolation factor.
        """
    def ranges(self) -> numpy.ndarray[numpy.float64[m, 1]]:
        """
        Get cumulative distances along the polyline.
        """
    def scanline(
        self, range: float, *, min: float, max: float, smooth_joint: bool = True
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]]:
        """
        Generate a scanline perpendicular to the polyline at a specific cumulative distance.
        """
    def segment_index(self, range: float) -> int:
        """
        Get the segment index for a given cumulative distance.
        """
    def segment_index_t(self, range: float) -> tuple[int, float]:
        """
        Get the segment index and interpolation factor for a given cumulative distance.
        """

@typing.overload
def douglas_simplify(
    coords: numpy.ndarray[numpy.float64[m, 3]],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.float64[m, 3]]:
    """
    Simplify a polyline using the Douglas-Peucker algorithm.
    """

@typing.overload
def douglas_simplify(
    coords: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.float64[m, 2]]:
    """
    Simplify a 2D polyline using the Douglas-Peucker algorithm.
    """

@typing.overload
def douglas_simplify_indexes(
    coords: numpy.ndarray[numpy.float64[m, 3]],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]:
    """
    Get indexes of points to keep when simplifying a polyline using the Douglas-Peucker algorithm.
    """

@typing.overload
def douglas_simplify_indexes(
    coords: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]:
    """
    Get indexes of points to keep when simplifying a 2D polyline using the Douglas-Peucker algorithm.
    """

@typing.overload
def douglas_simplify_mask(
    coords: numpy.ndarray[numpy.float64[m, 3]],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]:
    """
    Get a mask of points to keep when simplifying a polyline using the Douglas-Peucker algorithm.
    """

@typing.overload
def douglas_simplify_mask(
    coords: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]:
    """
    Get a mask of points to keep when simplifying a 2D polyline using the Douglas-Peucker algorithm.
    """

@typing.overload
def intersect_segments(
    a1: numpy.ndarray[numpy.float64[2, 1]],
    a2: numpy.ndarray[numpy.float64[2, 1]],
    b1: numpy.ndarray[numpy.float64[2, 1]],
    b2: numpy.ndarray[numpy.float64[2, 1]],
) -> tuple[numpy.ndarray[numpy.float64[2, 1]], float, float] | None:
    """
    Intersect two 2D line segments.
    """

@typing.overload
def intersect_segments(
    a1: numpy.ndarray[numpy.float64[3, 1]],
    a2: numpy.ndarray[numpy.float64[3, 1]],
    b1: numpy.ndarray[numpy.float64[3, 1]],
    b2: numpy.ndarray[numpy.float64[3, 1]],
) -> tuple[numpy.ndarray[numpy.float64[3, 1]], float, float, float] | None:
    """
    Intersect two 3D line segments.
    """

def snap_onto_2d(
    P: numpy.ndarray[numpy.float64[2, 1]],
    A: numpy.ndarray[numpy.float64[2, 1]],
    B: numpy.ndarray[numpy.float64[2, 1]],
) -> tuple[numpy.ndarray[numpy.float64[2, 1]], float, float]:
    """
    Snap P onto line segment AB
    """

__version__: str = "0.0.6"
