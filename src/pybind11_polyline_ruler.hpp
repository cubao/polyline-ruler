// should sync
// -
// https://github.com/cubao/polyline-ruler/blob/master/src/pybind11_polyline_ruler.hpp
// -
// https://github.com/cubao/headers/tree/main/include/cubao/pybind11_polyline_ruler.hpp

#pragma once

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "cubao_inline.hpp"
#include "polyline_ruler.hpp"

namespace cubao
{
namespace py = pybind11;
using namespace pybind11::literals;
using rvp = py::return_value_policy;

CUBAO_INLINE void bind_polyline_ruler(py::module &m)
{
    m
        //
        .def(
            "intersect_segments",
            py::overload_cast<const Eigen::Vector2d &, const Eigen::Vector2d &,
                              const Eigen::Vector2d &, const Eigen::Vector2d &>(
                &intersect_segments), //
            "Intersect two 2D line segments.",
            "a1"_a, "a2"_a, "b1"_a, "b2"_a)
        .def(
            "intersect_segments",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              const Eigen::Vector3d &, const Eigen::Vector3d &>(
                &intersect_segments), //
            "Intersect two 3D line segments.",
            "a1"_a, "a2"_a, "b1"_a, "b2"_a)
        //
        ;

    py::class_<LineSegment>(m, "LineSegment", py::module_local())      //
        .def(py::init<const Eigen::Vector3d, const Eigen::Vector3d>(), //
             "Initialize a LineSegment with two 3D points.",
             "A"_a, "B"_a)
        .def("distance", &LineSegment::distance, 
             "Calculate the distance from a point to the line segment.",
             "P"_a)
        .def("distance2", &LineSegment::distance2, 
             "Calculate the squared distance from a point to the line segment.",
             "P"_a)
        .def("intersects", &LineSegment::intersects, 
             "Check if this line segment intersects with another.",
             "other"_a)
        .def_property_readonly(
            "length",
            [](const LineSegment &self) { return std::sqrt(self.len2); },
            "Get the length of the line segment.")
        .def_property_readonly(
            "length2", [](const LineSegment &self) { return self.len2; },
            "Get the squared length of the line segment.")
        .def_property_readonly(
            "A",
            [](const LineSegment &self) -> const Eigen::Vector3d & {
                return self.A;
            },
            "Get the start point of the line segment.",
            rvp::reference_internal)
        .def_property_readonly(
            "B",
            [](const LineSegment &self) -> const Eigen::Vector3d & {
                return self.B;
            },
            "Get the end point of the line segment.",
            rvp::reference_internal)
        .def_property_readonly(
            "AB",
            [](const LineSegment &self) -> const Eigen::Vector3d & {
                return self.AB;
            },
            "Get the vector from A to B.",
            rvp::reference_internal)
        //
        ;

    py::class_<PolylineRuler>(m, "PolylineRuler", py::module_local()) //
        .def(py::init<const Eigen::Ref<const RowVectors> &, bool>(),  //
             "coords"_a, py::kw_only(), "is_wgs84"_a = false,
             "Initialize a PolylineRuler with coordinates and coordinate system.")
        //
        .def("polyline", &PolylineRuler::polyline, 
             rvp::reference_internal,
             "Get the polyline coordinates.")
        .def("N", &PolylineRuler::N, 
             "Get the number of points in the polyline.")
        .def("is_wgs84", &PolylineRuler::is_wgs84, 
             "Check if the coordinate system is WGS84.")
        .def("k", &PolylineRuler::k, 
             "Get the scale factor for distance calculations.")
        //
        .def_static(
            "_ranges",
            py::overload_cast<const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::ranges),
            "Calculate cumulative distances along a polyline.",
            "polyline"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("ranges", py::overload_cast<>(&PolylineRuler::ranges, py::const_),
             "Get cumulative distances along the polyline.",
             rvp::reference_internal)
        .def("range", py::overload_cast<int>(&PolylineRuler::range, py::const_),
             "Get the cumulative distance at a specific segment index.",
             "segment_index"_a)
        .def("range",
             py::overload_cast<int, double>(&PolylineRuler::range, py::const_),
             "Get the cumulative distance at a specific segment index and interpolation factor.",
             py::kw_only(), "segment_index"_a, "t"_a)
        //
        .def("segment_index", &PolylineRuler::segment_index, 
             "Get the segment index for a given cumulative distance.",
             "range"_a)
        .def("segment_index_t", &PolylineRuler::segment_index_t, 
             "Get the segment index and interpolation factor for a given cumulative distance.",
             "range"_a)
        //
        .def("length", &PolylineRuler::length, 
             "Get the total length of the polyline.")
        //
        .def_static(
            "_dirs",
            py::overload_cast<const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::dirs),
            "Calculate direction vectors for each segment of a polyline.",
            "polyline"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("dirs", py::overload_cast<>(&PolylineRuler::dirs, py::const_),
             "Get direction vectors for each segment of the polyline.",
             rvp::reference_internal)
        //
        .def("dir", py::overload_cast<int>(&PolylineRuler::dir, py::const_),
             "Get the direction vector at a specific point index.",
             py::kw_only(), "point_index"_a)
        .def("dir",
             py::overload_cast<double, bool>(&PolylineRuler::dir, py::const_),
             "Get the direction vector at a specific cumulative distance.",
             py::kw_only(), "range"_a, "smooth_joint"_a = true)
        .def("extended_along", &PolylineRuler::extended_along, 
             "Get the extended cumulative distance along the polyline.",
             "range"_a)
        .def("at", py::overload_cast<double>(&PolylineRuler::at, py::const_),
             "Get the point on the polyline at a specific cumulative distance.",
             py::kw_only(), "range"_a)
        .def("at", py::overload_cast<int>(&PolylineRuler::at, py::const_),
             "Get the point on the polyline at a specific segment index.",
             py::kw_only(), "segment_index"_a)
        .def("at",
             py::overload_cast<int, double>(&PolylineRuler::at, py::const_),
             "Get the point on the polyline at a specific segment index and interpolation factor.",
             py::kw_only(), "segment_index"_a, "t"_a)
        .def("arrow",
             py::overload_cast<int, double>(&PolylineRuler::arrow, py::const_),
             "Get the arrow (point and direction) at a specific segment index and interpolation factor.",
             py::kw_only(), "index"_a, "t"_a)
        .def("arrow",
             py::overload_cast<double, bool>(&PolylineRuler::arrow, py::const_),
             "Get the arrow (point and direction) at a specific cumulative distance.",
             "range"_a, //
             py::kw_only(), "smooth_joint"_a = true)
        .def("arrows",
             py::overload_cast<const Eigen::Ref<const Eigen::VectorXd> &, bool>(
                 &PolylineRuler::arrows, py::const_),
             "Get arrows (points and directions) at multiple cumulative distances.",
             "ranges"_a, //
             py::kw_only(), "smooth_joint"_a = true)
        .def("arrows",
             py::overload_cast<double, bool, bool>(&PolylineRuler::arrows,
                                                   py::const_),
             "Get arrows (points and directions) at regular intervals along the polyline.",
             "step"_a, //
             py::kw_only(), "with_last"_a = true, "smooth_joint"_a = true)
        .def("scanline", &PolylineRuler::scanline, 
             "Generate a scanline perpendicular to the polyline at a specific cumulative distance.",
             "range"_a, //
             py::kw_only(), "min"_a, "max"_a, "smooth_joint"_a = true)
        //
        .def("local_frame", &PolylineRuler::local_frame, 
             "Get the local coordinate frame at a specific cumulative distance.",
             "range"_a,
             py::kw_only(), "smooth_joint"_a = true)
        //
        .def_static(
            "_squareDistance",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              bool>(&PolylineRuler::squareDistance),
            "Calculate the squared distance between two points.",
            "a"_a, "b"_a, py::kw_only(), "is_wgs84"_a = false)
        .def_static(
            "_distance",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              bool>(&PolylineRuler::distance),
            "Calculate the distance between two points.",
            "a"_a, "b"_a, py::kw_only(), "is_wgs84"_a = false)
        .def_static(
            "_lineDistance",
            py::overload_cast<const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::lineDistance),
            "Calculate the total length of a polyline.",
            "line"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("lineDistance",
             py::overload_cast<>(&PolylineRuler::lineDistance, py::const_),
             "Get the total length of the polyline.")
        .def_static("_along",
                    py::overload_cast<const Eigen::Ref<const RowVectors> &,
                                      double, bool>(&PolylineRuler::along),
            "Find a point at a specified distance along a polyline.",
            "line"_a, "dist"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("along",
             py::overload_cast<double>(&PolylineRuler::along, py::const_),
             "Find a point at a specified distance along the polyline.",
             "dist"_a)
        //
        .def_static(
            "_pointToSegmentDistance",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              const Eigen::Vector3d &, bool>(
                &PolylineRuler::pointToSegmentDistance),
            "Calculate the distance from a point to a line segment.",
            "P"_a, "A"_a, "B"_a, py::kw_only(), "is_wgs84"_a = false)
        .def_static("_pointOnLine",
                    py::overload_cast<const Eigen::Ref<const RowVectors> &,
                                      const Eigen::Vector3d &, bool>(
                        &PolylineRuler::pointOnLine),
            "Find the closest point on a polyline to a given point.",
            "line"_a, "P"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("pointOnLine",
             py::overload_cast<const Eigen::Vector3d &>(
                 &PolylineRuler::pointOnLine, py::const_),
             "Find the closest point on the polyline to a given point.",
             "P"_a)
        .def_static(
            "_lineSlice",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::lineSlice),
            "Extract a portion of a polyline between two points.",
            "start"_a, "stop"_a, "line"_a, //
            py::kw_only(), "is_wgs84"_a = false)
        .def(
            "lineSlice",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &>(
                &PolylineRuler::lineSlice, py::const_),
            "Extract a portion of the polyline between two points.",
            "start"_a, "stop"_a)
        //
        .def_static(
            "_lineSliceAlong",
            py::overload_cast<double, double,
                              const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::lineSliceAlong),
            "Extract a portion of a polyline between two distances along it.",
            "start"_a, "stop"_a, "line"_a, //
            py::kw_only(), "is_wgs84"_a = false)
        .def("lineSliceAlong",
             py::overload_cast<double, double>(&PolylineRuler::lineSliceAlong,
                                               py::const_),
             "Extract a portion of the polyline between two distances along it.",
             "start"_a, "stop"_a)
        .def_static("_interpolate", &PolylineRuler::interpolate, //
                    "A"_a, "B"_a, py::kw_only(), "t"_a,
                    "Interpolate between two points.")
        //
        ;

    m.def("douglas_simplify",
          py::overload_cast<const RowVectors &, double, bool,
                            bool>(&douglas_simplify), //
          "Simplify a polyline using the Douglas-Peucker algorithm.",
          "coords"_a, "epsilon"_a,                    //
          py::kw_only(),                              //
          "is_wgs84"_a = false,                       //
          "recursive"_a = true);
    m.def(
        "douglas_simplify",
        py::overload_cast<const Eigen::Ref<const RowVectorsNx2> &, double, bool,
                          bool>(&douglas_simplify), //
        "Simplify a 2D polyline using the Douglas-Peucker algorithm.",
        "coords"_a, "epsilon"_a,                    //
        py::kw_only(),                              //
        "is_wgs84"_a = false,                       //
        "recursive"_a = true);
    m.def("douglas_simplify_mask",
          py::overload_cast<const RowVectors &, double, bool,
                            bool>(&douglas_simplify_mask), //
          "Get a mask of points to keep when simplifying a polyline using the Douglas-Peucker algorithm.",
          "coords"_a, "epsilon"_a, py::kw_only(),          //
          "is_wgs84"_a = false,                            //
          "recursive"_a = true);
    m.def(
        "douglas_simplify_mask",
        py::overload_cast<const Eigen::Ref<const RowVectorsNx2> &, double, bool,
                          bool>(&douglas_simplify_mask), //
        "Get a mask of points to keep when simplifying a 2D polyline using the Douglas-Peucker algorithm.",
        "coords"_a, "epsilon"_a, py::kw_only(),          //
        "is_wgs84"_a = false,                            //
        "recursive"_a = true);
    m.def("douglas_simplify_indexes",
          py::overload_cast<const RowVectors &, double, bool,
                            bool>(&douglas_simplify_indexes), //
          "Get indexes of points to keep when simplifying a polyline using the Douglas-Peucker algorithm.",
          "coords"_a, "epsilon"_a, py::kw_only(),             //
          "is_wgs84"_a = false,                               //
          "recursive"_a = true);
    m.def(
        "douglas_simplify_indexes",
        py::overload_cast<const Eigen::Ref<const RowVectorsNx2> &, double, bool,
                          bool>(&douglas_simplify_indexes), //
        "Get indexes of points to keep when simplifying a 2D polyline using the Douglas-Peucker algorithm.",
        "coords"_a, "epsilon"_a, py::kw_only(),             //
        "is_wgs84"_a = false,                               //
        "recursive"_a = true);
}
} // namespace cubao
