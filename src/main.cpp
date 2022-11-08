// https://github.com/microsoft/vscode-cpptools/issues/9692
#if __INTELLISENSE__
#undef __ARM_NEON
#undef __ARM_NEON__
#endif

#include <Eigen/Core>

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "cheap_ruler.hpp"
#include "crs_transform.hpp"
#include "eigen_helpers.hpp"
#include "polyline_ruler.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using rvp = py::return_value_policy;
using namespace pybind11::literals;

namespace pybind11
{
namespace detail
{
template <typename T>
struct type_caster<tl::optional<T>> : optional_caster<tl::optional<T>>
{
};
} // namespace detail
} // namespace pybind11

// clang-format off
#if (__cplusplus >= 201703L && __has_include(<optional>))
// C++17, for ubuntu 20.04 gcc9, should `set(CMAKE_CXX_STANDARD 17)` in CMakeLists.txt
#include <optional>
#define CUBAO_ARGV_DEFAULT_NONE(argv) py::arg_v(#argv, std::nullopt, "None")
#elif (__has_include(<experimental/optional>) && !__has_include(<optional>))
// C++14, for ubuntu 16.04 gcc5
#include <experimental/optional>
#define CUBAO_ARGV_DEFAULT_NONE(argv) py::arg_v(#argv, std::experimental::nullopt, "None")
#else
// fallback, sadly, explicit None is needed
#define CUBAO_ARGV_DEFAULT_NONE(argv) #argv##_a
#endif
// clang-format on

PYBIND11_MODULE(polyline_ruler, m)
{
    m.doc() = R"pbdoc(
        cubao/polyline-ruler is more than mapbox/cheap-ruler
        ----------------------------------------------------

        .. currentmodule:: polyline_ruler

        .. autosummary::
           :toctree: _generate

           TODO
    )pbdoc";

    using namespace cubao;

    auto tf = m.def_submodule("tf");
    tf //
       // ecef <-> lla
        .def("ecef2lla", py::overload_cast<double, double, double>(ecef2lla),
             "x"_a, "y"_a, "z"_a)
        .def("ecef2lla",
             py::overload_cast<const Eigen::Ref<const RowVectors> &>(ecef2lla),
             "ecefs"_a)
        .def("lla2ecef", py::overload_cast<double, double, double>(lla2ecef),
             "lon"_a, "lat"_a, "alt"_a)
        .def("lla2ecef",
             py::overload_cast<const Eigen::Ref<const RowVectors> &>(lla2ecef),
             "llas"_a)
        // lla <-> enu
        .def("lla2enu", &lla2enu, "llas"_a, py::kw_only(), //
             CUBAO_ARGV_DEFAULT_NONE(anchor_lla), "cheap_ruler"_a = true)
        .def("enu2lla", &enu2lla, "enus"_a, py::kw_only(), //
             "anchor_lla"_a, "cheap_ruler"_a = true)
        // enu <-> ecef
        .def("enu2ecef", &enu2ecef, "enus"_a, py::kw_only(), //
             "anchor_lla"_a, "cheap_ruler"_a = false)
        .def("ecef2enu", &ecef2enu, "ecefs"_a, py::kw_only(), //
             CUBAO_ARGV_DEFAULT_NONE(anchor_lla), "cheap_ruler"_a = false)
        // T_ecef_enu
        .def("R_ecef_enu", &R_ecef_enu, "lon"_a, "lat"_a)
        .def("T_ecef_enu",
             py::overload_cast<double, double, double>(&T_ecef_enu), //
             "lon"_a, "lat"_a, "alt"_a)
        .def("T_ecef_enu",
             py::overload_cast<const Eigen::Vector3d &>(&T_ecef_enu), "lla"_a)
        // apply transform
        .def("apply_transform", &apply_transform, "T"_a, "coords"_a)
        .def("apply_transform_inplace", &apply_transform_inplace, //
             "T"_a, "coords"_a, py::kw_only(), "batch_size"_a = 1000)
        //
        ;

    m
        //
        .def(
            "intersect_segments",
            py::overload_cast<const Eigen::Vector2d &, const Eigen::Vector2d &,
                              const Eigen::Vector2d &, const Eigen::Vector2d &>(
                &intersect_segments), //
            "a1"_a, "a2"_a, "b1"_a, "b2"_a)
        .def(
            "intersect_segments",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              const Eigen::Vector3d &, const Eigen::Vector3d &>(
                &intersect_segments), //
            "a1"_a, "a2"_a, "b1"_a, "b2"_a)
        //
        ;

    py::class_<LineSegment>(m, "LineSegment", py::module_local())      //
        .def(py::init<const Eigen::Vector3d, const Eigen::Vector3d>(), //
             "A"_a, "B"_a)
        .def("distance", &LineSegment::distance, "P"_a)
        .def("distance2", &LineSegment::distance2, "P"_a)
        .def("intersects", &LineSegment::intersects, "other"_a)
        //
        ;

    py::class_<PolylineRuler>(m, "PolylineRuler", py::module_local()) //
        .def(py::init<const Eigen::Ref<const RowVectors> &, bool>(),  //
             "coords"_a, py::kw_only(), "is_wgs84"_a = false)
        //
        .def("polyline", &PolylineRuler::polyline, rvp::reference_internal)
        .def("N", &PolylineRuler::N)
        .def("is_wgs84", &PolylineRuler::is_wgs84)
        //
        .def_static(
            "_ranges",
            py::overload_cast<const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::ranges),
            "polyline"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("ranges", py::overload_cast<>(&PolylineRuler::ranges, py::const_),
             rvp::reference_internal)
        //
        .def("length", &PolylineRuler::length)
        //
        .def_static(
            "_dirs",
            py::overload_cast<const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::dirs),
            "polyline"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("dirs", py::overload_cast<>(&PolylineRuler::dirs, py::const_),
             rvp::reference_internal)
        //
        .def("dir",
             py::overload_cast<double, bool>(&PolylineRuler::dir, py::const_),
             "range"_a, py::kw_only(), "smooth_joint"_a = true)
        .def("extented_along", &PolylineRuler::extended_along, "range"_a)
        .def("arrow", &PolylineRuler::arrow, "range"_a, //
             py::kw_only(), "smooth_joint"_a = true)
        .def("arrows",
             py::overload_cast<const Eigen::Ref<const Eigen::VectorXd> &, bool>(
                 &PolylineRuler::arrows, py::const_),
             "ranges"_a, //
             py::kw_only(), "smooth_joint"_a = true)
        .def("arrows",
             py::overload_cast<double, bool, bool>(&PolylineRuler::arrows,
                                                   py::const_),
             "step"_a, //
             py::kw_only(), "with_last"_a = true, "smooth_joint"_a = true)
        .def("scanline", &PolylineRuler::scanline, "range"_a, //
             py::kw_only(), "min"_a, "max"_a, "smooth_joint"_a = true)
        //
        .def("local_frame", &PolylineRuler::local_frame, "range"_a,
             py::kw_only(), "smooth_joint"_a = true)
        //
        .def_static(
            "_squareDistance",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              bool>(&PolylineRuler::squareDistance),
            "a"_a, "b"_a, py::kw_only(), "is_wgs84"_a = false)
        .def_static(
            "_distance",
            py::overload_cast<const Eigen::Vector3d &, const Eigen::Vector3d &,
                              bool>(&PolylineRuler::distance),
            "a"_a, "b"_a, py::kw_only(), "is_wgs84"_a = false)
        .def_static(
            "_lineDistance",
            py::overload_cast<const Eigen::Ref<const RowVectors> &, bool>(
                &PolylineRuler::lineDistance),
            "line"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("lineDistance",
             py::overload_cast<>(&PolylineRuler::lineDistance, py::const_))
        .def_static("_along",
                    py::overload_cast<const Eigen::Ref<const RowVectors> &,
                                      double, bool>(&PolylineRuler::along),
                    "line"_a, "dist"_a, py::kw_only(), "is_wgs84"_a = false)
        .def("along",
             py::overload_cast<double>(&PolylineRuler::along, py::const_),
             "dist"_a)
        //
        ;

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
