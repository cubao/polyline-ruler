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
    "tf",
]

class CheapRuler:
    class Unit:
        """
        Members:

          Kilometers

          Miles

          NauticalMiles

          Meters

          Metres

          Yards

          Feet

          Inches
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
    def _fromTile(x: int, y: int) -> CheapRuler: ...
    @staticmethod
    def _insideBBox(
        p: numpy.ndarray[numpy.float64[3, 1]],
        bbox: tuple[
            numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
        ],
        *,
        cheak_z: bool = False,
    ) -> bool: ...
    @staticmethod
    def _interpolate(
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
        t: float,
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @staticmethod
    def _k(
        latitude: float, *, unit: CheapRuler.Unit = ...
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @staticmethod
    def _longDiff(a: float, b: float) -> float: ...
    def __init__(self, latitude: float, *, unit: CheapRuler.Unit = ...) -> None: ...
    def along(
        self,
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        dist: float,
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def area(
        self, ring: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous]
    ) -> float: ...
    def bearing(
        self,
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float: ...
    def bufferBBox(
        self,
        bbox: tuple[
            numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
        ],
        buffer: float,
    ) -> tuple[
        numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
    ]: ...
    def bufferPoint(
        self, p: numpy.ndarray[numpy.float64[3, 1]], buffer: float
    ) -> tuple[
        numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
    ]: ...
    def delta(
        self,
        lla0: numpy.ndarray[numpy.float64[3, 1]],
        lla1: numpy.ndarray[numpy.float64[3, 1]],
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def destination(
        self, origin: numpy.ndarray[numpy.float64[3, 1]], dist: float, bearing: float
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def distance(
        self,
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float: ...
    def k(self) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def lineDistance(
        self,
        points: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
    ) -> float: ...
    def lineSlice(
        self,
        start: numpy.ndarray[numpy.float64[3, 1]],
        stop: numpy.ndarray[numpy.float64[3, 1]],
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
    ) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    def lineSliceAlong(
        self,
        start: float,
        stop: float,
        line: numpy.ndarray[
            numpy.float64[m, 3],
            numpy.ndarray.flags.writeable,
            numpy.ndarray.flags.c_contiguous,
        ],
    ) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    def offset(
        self,
        origin: numpy.ndarray[numpy.float64[3, 1]],
        dx: float,
        dy: float,
        dz: float = 0.0,
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def pointOnLine(
        self,
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        p: numpy.ndarray[numpy.float64[3, 1]],
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], int, float]: ...
    def pointToSegmentDistance(
        self,
        p: numpy.ndarray[numpy.float64[3, 1]],
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float: ...
    def squareDistance(
        self,
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
    ) -> float: ...

class LineSegment:
    def __init__(
        self,
        A: numpy.ndarray[numpy.float64[3, 1]],
        B: numpy.ndarray[numpy.float64[3, 1]],
    ) -> None: ...
    def distance(self, P: numpy.ndarray[numpy.float64[3, 1]]) -> float: ...
    def distance2(self, P: numpy.ndarray[numpy.float64[3, 1]]) -> float: ...
    def intersects(
        self, other: LineSegment
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], float, float, float] | None: ...
    @property
    def A(self) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @property
    def AB(self) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @property
    def B(self) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @property
    def length(self) -> float: ...
    @property
    def length2(self) -> float: ...

class PolylineRuler:
    @staticmethod
    def _along(
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        dist: float,
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @staticmethod
    def _dirs(
        polyline: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    @staticmethod
    def _distance(
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> float: ...
    @staticmethod
    def _interpolate(
        A: numpy.ndarray[numpy.float64[3, 1]],
        B: numpy.ndarray[numpy.float64[3, 1]],
        *,
        t: float,
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @staticmethod
    def _lineDistance(
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> float: ...
    @staticmethod
    def _lineSlice(
        start: numpy.ndarray[numpy.float64[3, 1]],
        stop: numpy.ndarray[numpy.float64[3, 1]],
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    @staticmethod
    def _lineSliceAlong(
        start: float,
        stop: float,
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    @staticmethod
    def _pointOnLine(
        line: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        P: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], int, float]: ...
    @staticmethod
    def _pointToSegmentDistance(
        P: numpy.ndarray[numpy.float64[3, 1]],
        A: numpy.ndarray[numpy.float64[3, 1]],
        B: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> float: ...
    @staticmethod
    def _ranges(
        polyline: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> numpy.ndarray[numpy.float64[m, 1]]: ...
    @staticmethod
    def _squareDistance(
        a: numpy.ndarray[numpy.float64[3, 1]],
        b: numpy.ndarray[numpy.float64[3, 1]],
        *,
        is_wgs84: bool = False,
    ) -> float: ...
    def N(self) -> int: ...
    def __init__(
        self,
        coords: numpy.ndarray[numpy.float64[m, 3], numpy.ndarray.flags.c_contiguous],
        *,
        is_wgs84: bool = False,
    ) -> None: ...
    def along(self, dist: float) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @typing.overload
    def arrow(
        self, *, index: int, t: float
    ) -> tuple[
        numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
    ]: ...
    @typing.overload
    def arrow(
        self, range: float, *, smooth_joint: bool = True
    ) -> tuple[
        numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
    ]: ...
    @typing.overload
    def arrows(
        self, ranges: numpy.ndarray[numpy.float64[m, 1]], *, smooth_joint: bool = True
    ) -> tuple[
        numpy.ndarray[numpy.float64[m, 1]],
        numpy.ndarray[numpy.float64[m, 3]],
        numpy.ndarray[numpy.float64[m, 3]],
    ]: ...
    @typing.overload
    def arrows(
        self, step: float, *, with_last: bool = True, smooth_joint: bool = True
    ) -> tuple[
        numpy.ndarray[numpy.float64[m, 1]],
        numpy.ndarray[numpy.float64[m, 3]],
        numpy.ndarray[numpy.float64[m, 3]],
    ]: ...
    @typing.overload
    def at(self, *, range: float) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @typing.overload
    def at(self, *, segment_index: int) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @typing.overload
    def at(
        self, *, segment_index: int, t: float
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @typing.overload
    def dir(self, *, point_index: int) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    @typing.overload
    def dir(
        self, *, range: float, smooth_joint: bool = True
    ) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def dirs(self) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    def extended_along(self, range: float) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def is_wgs84(self) -> bool: ...
    def k(self) -> numpy.ndarray[numpy.float64[3, 1]]: ...
    def length(self) -> float: ...
    def lineDistance(self) -> float: ...
    def lineSlice(
        self,
        start: numpy.ndarray[numpy.float64[3, 1]],
        stop: numpy.ndarray[numpy.float64[3, 1]],
    ) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    def lineSliceAlong(
        self, start: float, stop: float
    ) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    def local_frame(
        self, range: float, *, smooth_joint: bool = True
    ) -> numpy.ndarray[numpy.float64[4, 4]]: ...
    def pointOnLine(
        self, P: numpy.ndarray[numpy.float64[3, 1]]
    ) -> tuple[numpy.ndarray[numpy.float64[3, 1]], int, float]: ...
    def polyline(self) -> numpy.ndarray[numpy.float64[m, 3]]: ...
    @typing.overload
    def range(self, segment_index: int) -> float: ...
    @typing.overload
    def range(self, *, segment_index: int, t: float) -> float: ...
    def ranges(self) -> numpy.ndarray[numpy.float64[m, 1]]: ...
    def scanline(
        self, range: float, *, min: float, max: float, smooth_joint: bool = True
    ) -> tuple[
        numpy.ndarray[numpy.float64[3, 1]], numpy.ndarray[numpy.float64[3, 1]]
    ]: ...
    def segment_index(self, range: float) -> int: ...
    def segment_index_t(self, range: float) -> tuple[int, float]: ...

@typing.overload
def douglas_simplify(
    coords: numpy.ndarray[numpy.float64[m, 3]],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.float64[m, 3]]: ...
@typing.overload
def douglas_simplify(
    coords: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.float64[m, 2]]: ...
@typing.overload
def douglas_simplify_indexes(
    coords: numpy.ndarray[numpy.float64[m, 3]],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]: ...
@typing.overload
def douglas_simplify_indexes(
    coords: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]: ...
@typing.overload
def douglas_simplify_mask(
    coords: numpy.ndarray[numpy.float64[m, 3]],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]: ...
@typing.overload
def douglas_simplify_mask(
    coords: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    epsilon: float,
    *,
    is_wgs84: bool = False,
    recursive: bool = True,
) -> numpy.ndarray[numpy.int32[m, 1]]: ...
@typing.overload
def intersect_segments(
    a1: numpy.ndarray[numpy.float64[2, 1]],
    a2: numpy.ndarray[numpy.float64[2, 1]],
    b1: numpy.ndarray[numpy.float64[2, 1]],
    b2: numpy.ndarray[numpy.float64[2, 1]],
) -> tuple[numpy.ndarray[numpy.float64[2, 1]], float, float] | None: ...
@typing.overload
def intersect_segments(
    a1: numpy.ndarray[numpy.float64[3, 1]],
    a2: numpy.ndarray[numpy.float64[3, 1]],
    b1: numpy.ndarray[numpy.float64[3, 1]],
    b2: numpy.ndarray[numpy.float64[3, 1]],
) -> tuple[numpy.ndarray[numpy.float64[3, 1]], float, float, float] | None: ...

__version__: str = "0.0.5"
