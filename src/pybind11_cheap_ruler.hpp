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
        .def("k", py::overload_cast<>(&CheapRuler::k, py::const_))
        .def_static(
            "_k", py::overload_cast<double, CheapRuler::Unit>(&CheapRuler::k),
            "latitude"_a, py::kw_only(), "unit"_a = CheapRuler::Unit::Meters)

        .def_readonly_static("RE", &CheapRuler::RE)
        .def_readonly_static("FE", &CheapRuler::FE)
        .def_readonly_static("E2", &CheapRuler::E2)
        .def_readonly_static("RAD", &CheapRuler::RAD)
        //
        ;
}
} // namespace cubao
