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

    py::class_<LineSegment>(m, "LineSegment", py::module_local())      //
        .def(py::init<const Eigen::Vector3d, const Eigen::Vector3d>(), //
             "A"_a, "B"_a)
        .def("distance", &LineSegment::distance, "P"_a)
        .def("distance2", &LineSegment::distance2, "P"_a)
        //
        ;

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
