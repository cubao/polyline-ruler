// should sync
// -
// https://github.com/cubao/polyline-ruler/blob/master/src/pybind11_cheap_ruler.hpp
// -
// https://github.com/cubao/headers/tree/main/include/cubao/pybind11_cheap_ruler.hpp

#pragma once

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "cubao_inline.hpp"
#include "cheap_ruler.hpp"

namespace cubao
{
namespace py = pybind11;
using namespace pybind11::literals;
using rvp = py::return_value_policy;

CUBAO_INLINE void bind_cheap_ruler(py::module &m)
{
    py::class_<CheapRuler> cheap_ruler(m, "CheapRuler", py::module_local());

    py::enum_<CheapRuler::Unit>(cheap_ruler, "Unit")
        .value("Kilometers", CheapRuler::Unit::Kilometers)
        .value("Miles", CheapRuler::Unit::Miles)
        .value("NauticalMiles", CheapRuler::Unit::NauticalMiles)
        .value("Meters", CheapRuler::Unit::Meters)
        .value("Metres", CheapRuler::Unit::Metres)
        .value("Yards", CheapRuler::Unit::Yards)
        .value("Feet", CheapRuler::Unit::Feet)
        .value("Inches", CheapRuler::Unit::Inches)
        .export_values();

    cheap_ruler //
        .def("k", py::overload_cast<>(&CheapRuler::k, py::const_),
             "Get the ruler's unit conversion factor.")
        .def_static(
            "_k", py::overload_cast<double, CheapRuler::Unit>(&CheapRuler::k),
            "Get the unit conversion factor for a given latitude and unit.",
            "latitude"_a, py::kw_only(), "unit"_a = CheapRuler::Unit::Meters)

        .def_readonly_static("RE", &CheapRuler::RE, "Earth's equatorial radius in meters.")
        .def_readonly_static("FE", &CheapRuler::FE, "Earth's flattening.")
        .def_readonly_static("E2", &CheapRuler::E2, "Square of Earth's eccentricity.")
        .def_readonly_static("RAD", &CheapRuler::RAD, "Conversion factor from degrees to radians.")
        //
        .def(py::init<double, CheapRuler::Unit>(),
             "Initialize a CheapRuler object with a given latitude and unit.",
             "latitude"_a, py::kw_only(), "unit"_a = CheapRuler::Unit::Meters)
        //
        .def_static("_fromTile", &CheapRuler::fromTile,
                    "Create a CheapRuler from tile coordinates (x, y).",
                    "x"_a, "y"_a)
        .def("delta", &CheapRuler::delta,
             "Calculate the distance between two points in the x, y plane.",
             "lla0"_a, "lla1"_a)
        .def("squareDistance", &CheapRuler::squareDistance,
             "Calculate the squared distance between two points.",
             "a"_a, "b"_a)
        .def("distance", &CheapRuler::distance,
             "Calculate the distance between two points.",
             "a"_a, "b"_a)
        .def("bearing", &CheapRuler::bearing,
             "Calculate the bearing between two points.",
             "a"_a, "b"_a)
        .def("destination", &CheapRuler::destination,
             "Calculate the destination point given origin, distance, and bearing.",
             "origin"_a, "dist"_a, "bearing"_a)
        .def("offset", &CheapRuler::offset,
             "Calculate a new point given origin and offsets.",
             "origin"_a, "dx"_a, "dy"_a, "dz"_a = 0.0)
        .def("lineDistance", &CheapRuler::lineDistance,
             "Calculate the total distance of a line (an array of points).",
             "points"_a)
        .def("area", &CheapRuler::area,
             "Calculate the area of a polygon.",
             "ring"_a)
        .def("along", &CheapRuler::along,
             "Calculate a point at a specified distance along the line.",
             "line"_a, "dist"_a)
        .def("pointToSegmentDistance", &CheapRuler::pointToSegmentDistance,
             "Calculate the distance from a point to a line segment.",
             "p"_a, "a"_a, "b"_a)
        .def("pointOnLine", &CheapRuler::pointOnLine,
             "Calculate the closest point on a line to the given point.",
             "line"_a, "p"_a)
        .def("lineSlice", &CheapRuler::lineSlice,
             "Get a part of the line between the start and stop points.",
             "start"_a, "stop"_a, "line"_a)
        .def("lineSliceAlong", &CheapRuler::lineSliceAlong,
             "Get a part of the line between the start and stop distances along the line.",
             "start"_a, "stop"_a, "line"_a)
        .def("bufferPoint", &CheapRuler::bufferPoint,
             "Create a bounding box around a point.",
             "p"_a, "buffer"_a)
        .def("bufferBBox", &CheapRuler::bufferBBox,
             "Create a bounding box around another bounding box.",
             "bbox"_a, "buffer"_a)
        .def_static("_insideBBox", &CheapRuler::insideBBox,
                    "Check if a point is inside a bounding box.",
                    "p"_a, "bbox"_a, py::kw_only(), "cheak_z"_a = false)
        .def_static("_interpolate", &CheapRuler::interpolate,
                    "Interpolate linearly between two points.",
                    "a"_a, "b"_a, "t"_a)
        .def_static("_longDiff", &CheapRuler::longDiff,
                    "Calculate the difference between two longitudes.",
                    "a"_a, "b"_a);
}
} // namespace cubao
